import numpy
import numpy as np
from py4j.java_gateway import get_field, set_field
from typing import Optional, Iterable, Sequence
from py4j.java_collections import ListConverter

from neuralogic import get_neuralogic, get_gateway
from neuralogic.core.settings import SettingsProxy, Settings


class JavaFactory:
    def __init__(self, settings: Optional[SettingsProxy] = None):
        from neuralogic.core.constructs.rule import Rule
        from neuralogic.core.constructs.atom import WeightedAtom

        if settings is None:
            settings = Settings().create_proxy()

        neuralogic_jvm = get_neuralogic()

        self.weighted_atom_type = WeightedAtom
        self.rule_type = Rule

        namespace = neuralogic_jvm.cz.cvut.fel.ida.logic.constructs.building
        self.settings = settings

        self.namespace = neuralogic_jvm.cz.cvut.fel.ida.logic.constructs.template.components
        self.value_namespace = neuralogic_jvm.cz.cvut.fel.ida.algebra.values
        self.example_namespace = neuralogic_jvm.cz.cvut.fel.ida.logic.constructs.example

        self.builder = namespace.TemplateBuilder(settings.settings)

        self.constant_factory = get_field(self.builder, "constantFactory")
        self.predicate_factory = get_field(self.builder, "predicateFactory")
        self.weight_factory = get_field(self.builder, "weightFactory")

        self.predicate_metadata = neuralogic_jvm.cz.cvut.fel.ida.logic.constructs.template.metadata.PredicateMetadata
        self.rule_metadata = neuralogic_jvm.cz.cvut.fel.ida.logic.constructs.template.metadata.RuleMetadata

        self.unit_weight = neuralogic_jvm.cz.cvut.fel.ida.algebra.weights.Weight.unitWeight
        self.variable_factory = self.get_variable_factory()

        self.list_converter = ListConverter()

    @staticmethod
    def get_variable_factory():
        namespace = get_neuralogic().cz.cvut.fel.ida.logic.constructs.building.factories
        variable_factory = namespace.VariableFactory()

        return variable_factory

    def get_term(self, term, variable_factory):
        if isinstance(term, str):
            if term[0].islower() or term.isnumeric():
                return self.constant_factory.construct(term)
            elif term[0].isupper():
                return variable_factory.construct(term)
            else:
                raise NotImplementedError
        if isinstance(term, (int, float)):
            return self.constant_factory.construct(str(term))
        raise NotImplementedError

    def atom_to_clause(self, atom):
        namespace = get_neuralogic().cz.cvut.fel.ida.logic

        terms = self.list_converter.convert(
            [self.get_term(term, self.variable_factory) for term in atom.terms], get_gateway()._gateway_client
        )

        predicate_name = f"@{atom.predicate.name}" if atom.predicate.special else atom.predicate.name
        literal = namespace.Literal(predicate_name, atom.negated, terms)
        return namespace.Clause(self.list_converter.convert([literal], get_gateway()._gateway_client))

    def get_generic_atom(self, atom_class, atom, variable_factory, default_weight=None, is_example=False):
        predicate = self.get_predicate(atom.predicate)

        weight = None
        if isinstance(atom, self.weighted_atom_type):
            weight = self.get_weight(atom.weight, atom.weight_name, atom.is_fixed or is_example)
        elif default_weight is not None:
            weight = self.get_weight(default_weight, None, True)

        term_list = self.list_converter.convert(
            [self.get_term(term, variable_factory) for term in atom.terms], get_gateway()._gateway_client
        )

        java_atom = atom_class(predicate, term_list, atom.negated, weight)
        set_field(java_atom, "originalString", atom.to_str())

        return java_atom

    def get_metadata(self, metadata, metadata_class):
        if metadata is None:
            return None

        if (
            metadata.aggregation is None
            and metadata.activation is None
            and metadata.offset is None
            and metadata.learnable is None
        ):
            return None

        map = get_gateway().jvm.java.util.LinkedHashMap()

        if metadata.aggregation is not None:
            map.put("aggregation", self.value_namespace.StringValue(metadata.aggregation.value.lower()))
        if metadata.activation is not None:
            map.put("activation", self.value_namespace.StringValue(metadata.activation.value.lower()))
        # if metadata.offset is not None:
        #     _, value = self.get_value(metadata.offset)
        #     map.put("offset", self.weight_factory.construct(value))
        if metadata.learnable is not None:
            map.put("learnable", self.value_namespace.StringValue(str(metadata.learnable).lower()))

        return metadata_class(get_field(self.builder, "settings"), map)

    def get_query(self, query):
        variable_factory = self.get_variable_factory()

        if not isinstance(query, self.rule_type):
            if not isinstance(query, Iterable):
                query = [query]
            return None, self.get_conjunction(query, variable_factory, 1.0, True)
        return self.get_atom(query.head, variable_factory, True), self.get_conjunction(
            query.body, variable_factory, is_example=True
        )

    def get_lifted_example(self, example):
        gateway_client = get_gateway()._gateway_client

        conjunctions = []
        rules = self.list_converter.convert([], gateway_client)
        label_conjunction = None

        variabel_factory = self.get_variable_factory()

        if not isinstance(example, self.rule_type):
            if not isinstance(example, Iterable):
                example = [example]
            conjunctions.append(self.get_conjunction(example, variabel_factory, is_example=True))
        else:
            label_conjunction = self.get_conjunction([example.head], variabel_factory, is_example=True)
            conjunctions.append(self.get_conjunction(example.body, variabel_factory, is_example=True))

        lifted_example = self.example_namespace.LiftedExample(
            self.list_converter.convert(conjunctions, gateway_client), rules
        )
        return label_conjunction, lifted_example

    def get_conjunction(self, atoms, variable_factory, default_weight=None, is_example=False):
        namespace = get_neuralogic().cz.cvut.fel.ida.logic.constructs
        valued_facts = [self.get_valued_fact(atom, variable_factory, default_weight, is_example) for atom in atoms]

        return namespace.Conjunction(self.list_converter.convert(valued_facts, get_gateway()._gateway_client))

    def get_predicate_metadata_pair(self, predicate_metadata):
        namespace = get_neuralogic().cz.cvut.fel.ida.utils.generic

        return namespace.Pair(
            self.get_predicate(predicate_metadata.predicate),
            self.get_metadata(predicate_metadata.metadata, self.predicate_metadata),
        )

    def get_valued_fact(self, atom, variable_factory, default_weight=None, is_example=False):
        return self.get_generic_atom(
            self.example_namespace.ValuedFact,
            atom,
            variable_factory,
            default_weight,
            is_example,
        )

    def get_atom(self, atom, variable_factory, is_example=False):
        return self.get_generic_atom(self.namespace.BodyAtom, atom, variable_factory, is_example=is_example)

    def get_rule(self, rule):
        java_rule = self.namespace.WeightedRule()
        java_rule.setOriginalString(str(rule))

        variable_factory = self.get_variable_factory()

        head_atom = self.get_atom(rule.head, variable_factory)
        weight = head_atom.getConjunctWeight()

        if weight is None:
            java_rule.setWeight(self.unit_weight)
        else:
            java_rule.setWeight(weight)

        body_atoms = [self.get_atom(atom, variable_factory) for atom in rule.body]
        body_atom_list = self.list_converter.convert(body_atoms, get_gateway()._gateway_client)

        java_rule.setHead(self.namespace.HeadAtom(head_atom))
        java_rule.setBody(body_atom_list)

        offset = None  # TODO: Implement

        java_rule.setOffset(offset)
        java_rule.setMetadata(self.get_metadata(rule.metadata, self.rule_metadata))

        return java_rule

    def get_predicate(self, predicate):
        return self.predicate_factory.construct(predicate.name, predicate.arity, predicate.special, predicate.hidden)

    def get_weight(self, weight, name, fixed):
        initialized, value = self.get_value(weight)

        if name is None:
            return self.weight_factory.construct(value, fixed, initialized)
        return self.weight_factory.construct(name, value, fixed, initialized)

    def get_value(self, weight):
        if isinstance(weight, (int, float)):
            value = self.value_namespace.ScalarValue(float(weight))
            initialized = True
        elif isinstance(weight, tuple):
            if len(weight) == 1:
                if weight[0] == 1:
                    value = self.value_namespace.ScalarValue()
                else:
                    value = self.value_namespace.VectorValue(weight[0])
            elif len(weight) == 2:
                if weight[0] == 1:
                    value = self.value_namespace.VectorValue(weight[1])
                    set_field(value, "rowOrientation", True)
                elif weight[1] == 1:
                    value = self.value_namespace.VectorValue(weight[0])
                    set_field(value, "rowOrientation", False)
                else:
                    value = self.value_namespace.MatrixValue(weight[0], weight[1])
            else:
                raise NotImplementedError
            initialized = False
        elif isinstance(weight, Sequence):
            initialized = True
            if len(weight) == 0:
                raise NotImplementedError
            if isinstance(weight[0], (int, float, np.number)):
                vector = self.list_converter.convert([float(w) for w in weight], get_gateway()._gateway_client)
                value = self.value_namespace.VectorValue(vector)
            elif isinstance(weight[0], (Sequence, numpy.ndarray)):
                matrix = []

                if len(weight) == 1:
                    vector = self.list_converter.convert([float(w) for w in weight[0]], get_gateway()._gateway_client)
                    value = self.value_namespace.VectorValue(vector)
                    set_field(value, "rowOrientation", True)
                else:
                    try:
                        for weights in weight:
                            values = [float(w) for w in weights]
                            matrix.append(self.list_converter.convert(values, get_gateway()._gateway_client))

                        matrix = self.list_converter.convert(matrix, get_gateway()._gateway_client)
                        value = self.value_namespace.MatrixValue(matrix)
                    except TypeError:
                        vector = self.list_converter.convert([float(w) for w in weight], get_gateway()._gateway_client)
                        value = self.value_namespace.VectorValue(vector)
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return initialized, value

    def get_new_weight_factory(self):
        builder = get_neuralogic().cz.cvut.fel.ida.logic.constructs.building.ExamplesBuilder(self.settings.settings)

        return get_field(builder, "weightFactory")
