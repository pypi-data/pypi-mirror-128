import os
from typing import Optional

from neuralogic import get_neuralogic
from neuralogic.core.builder import Sample
from neuralogic.core.settings import Settings, SettingsProxy

from py4j.java_gateway import set_field


def get_drawing_settings(img_type: str = "png") -> SettingsProxy:
    """Returns the default settings instance for drawing with a specified image type.

    :param img_type:
    :return:
    """
    settings = Settings().create_proxy()

    set_field(settings.settings, "drawing", False)
    set_field(settings.settings, "storeNotShow", True)
    set_field(settings.settings, "imgType", img_type)

    return settings


def get_template_drawer(settings: SettingsProxy):
    namespace = get_neuralogic().cz.cvut.fel.ida.pipelines.debugging.drawing

    return namespace.TemplateDrawer(settings.settings)


def get_sample_drawer(settings: SettingsProxy):
    namespace = get_neuralogic().cz.cvut.fel.ida.pipelines.debugging.drawing

    return namespace.NeuralNetDrawer(settings.settings)


# todo gusta: + groundingDrawer, pipelineDrawer...


def draw(drawer, obj, filename: Optional[str] = None, draw_ipython=True, img_type="png", *args, **kwargs):
    if filename is not None:
        drawer.drawIntoFile(obj, os.path.abspath(filename))

        return

    data = drawer.drawIntoBytes(obj)

    if draw_ipython:
        from IPython.display import Image, SVG

        if img_type == "svg":
            return SVG(data, *args, **kwargs)
        return Image(data, *args, **kwargs)
    return data


def to_dot_source(drawer, obj) -> str:
    return drawer.getGraphSource(obj)


def draw_model(model, filename: Optional[str] = None, draw_ipython=True, img_type="png", *args, **kwargs):
    """Draws model either as an image of type img_type either into:
        * a file - if filename is specified),
        * an IPython Image - if draw_ipython is True
        * or bytes otherwise

    :param model:
    :param filename:
    :param draw_ipython:
    :param img_type:
    :param args:
    :param kwargs:
    :return:
    """
    if model.need_sync:
        model.sync_template()

    template = model.template
    template_drawer = get_template_drawer(get_drawing_settings(img_type=img_type))

    return draw(template_drawer, template, filename, draw_ipython, img_type, *args, **kwargs)


def draw_sample(sample, filename: Optional[str] = None, draw_ipython=True, img_type="png", *args, **kwargs):
    """Draws sample either as an image of type img_type either into:
        * a file - if filename is specified),
        * an IPython Image - if draw_ipython is True
        * or bytes otherwise

    :param sample:
    :param filename:
    :param draw_ipython:
    :param img_type:
    :param args:
    :param kwargs:
    :return:
    """
    draw_object = sample
    if isinstance(draw_object, Sample):
        draw_object = draw_object.java_sample

    sample_drawer = get_sample_drawer(get_drawing_settings(img_type=img_type))

    return draw(sample_drawer, draw_object, filename, draw_ipython, img_type, *args, **kwargs)


def model_to_dot_source(model) -> str:
    """Renders the model into its dot source representation.

    :param model:
    :return:
    """
    if model.need_sync:
        model.sync_template()

    template = model.template
    template_drawer = get_template_drawer(get_drawing_settings())

    return to_dot_source(template_drawer, template)


def sample_to_dot_source(sample) -> str:
    """Renders the sample into its dot source representation.

    :param sample:
    :return:
    """
    sample_drawer = get_sample_drawer(get_drawing_settings())

    return to_dot_source(sample_drawer, sample)
