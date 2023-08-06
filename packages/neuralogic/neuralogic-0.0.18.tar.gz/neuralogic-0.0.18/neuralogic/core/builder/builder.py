from neuralogic import get_neuralogic, get_gateway
from neuralogic.core.builder.components import Weight, Sample
from neuralogic.core.enums import Backend
from neuralogic.core.settings import SettingsProxy
from neuralogic.core.sources import Sources

from typing import List, Optional
from py4j.java_gateway import get_field


def stream_to_list(stream) -> List:
    return list(stream.collect(get_gateway().jvm.java.util.stream.Collectors.toList()))


class Builder:
    def __init__(self, settings: SettingsProxy):
        self.settings = settings
        self.example_builder = Builder.get_builders(settings)
        self.builder = Builder.get_builders(settings)

    def build_template_from_file(self, settings: SettingsProxy, filename: str):
        args = [
            "-t",
            filename,
            "-q",
            filename,
        ]

        sources = Sources.from_args(args, settings)
        template = self.builder.buildTemplate(sources.sources)

        return template

    def from_sources(self, parsed_template, sources: Sources, backend: Backend):
        if backend == Backend.JAVA:
            source_pipeline = self.example_builder.buildPipeline(parsed_template, sources.sources)
            source_pipeline.execute(None if sources is None else sources.sources)
            java_model = source_pipeline.get()

            logic_samples = get_field(java_model, "s")
            return logic_samples.collect(get_neuralogic().java.util.stream.Collectors.toList())

        return Builder.build(self.example_builder.buildPipeline(parsed_template, sources.sources), sources)

    def from_logic_samples(self, parsed_template, logic_samples, backend: Backend):
        if backend == Backend.JAVA:
            source_pipeline = self.example_builder.buildPipeline(parsed_template, logic_samples)
            source_pipeline.execute(None)
            java_model = source_pipeline.get()

            logic_samples = get_field(java_model, "s")
            return logic_samples.collect(get_neuralogic().java.util.stream.Collectors.toList())

        return Builder.build(self.example_builder.buildPipeline(parsed_template, logic_samples), None)

    def build_model(self, parsed_template, backend: Backend, settings: SettingsProxy):
        namespace = get_neuralogic().cz.cvut.fel.ida.neural.networks.computation.training

        neural_model = namespace.NeuralModel(parsed_template.getAllWeights(), settings.settings)

        if backend == Backend.JAVA:
            return neural_model

        dummy_weight = Weight.get_unit_weight()
        weights: List = [dummy_weight] * len(parsed_template.getAllWeights())

        for x in parsed_template.getAllWeights():
            weight = Weight(x)

            if weight.index >= len(weights):
                weights.extend([dummy_weight] * (weight.index - len(weights) + 1))
            weights[weight.index] = weight
        return weights

    @staticmethod
    def get_builders(settings: SettingsProxy):
        namespace = get_neuralogic().cz.cvut.fel.ida.pipelines.building
        builder = namespace.PythonBuilder(settings.settings)

        return builder

    @staticmethod
    def build(source_pipeline, sources: Optional[Sources]):
        source_pipeline.execute(None if sources is None else sources.sources)
        java_model = source_pipeline.get()

        logic_samples = get_field(java_model, "s")
        serializer = get_neuralogic().cz.cvut.fel.ida.neural.networks.structure.export.NeuralSerializer()
        logic_samples = stream_to_list(logic_samples)

        return [Sample(serializer.serialize(x), x) for x in logic_samples]
