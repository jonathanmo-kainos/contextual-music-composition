class PCASliderComponent(object):
    bottom_limit = 0
    top_limit = 0
    increment_value = 0
    number = 0

    def __init__(self, bottom_limit, top_limit, increment_value, number):
        self.bottom_limit = bottom_limit
        self.top_limit = top_limit
        self.increment_value = increment_value
        self.number = number


def define_pca_slider_component(bottom_limit, top_limit, increment_value, number):
    return PCASliderComponent(bottom_limit, top_limit, increment_value, number)


def serialize(slider_components):
    serialized_slider_components = []
    for slider_component in slider_components:
        serialized_slider_components.append({
            'bottomLimit': slider_component.bottom_limit,
            'topLimit': slider_component.top_limit,
            'incrementValue': slider_component.increment_value,
            'number': slider_component.number
        })
    return serialized_slider_components


def deserialize(slider_components):
    deserialized_slider_components = []
    for slider_component in slider_components:
        deserialized_slider_components.append(define_pca_slider_component(slider_component.get('bottomLimit'),
                                                                          slider_component.get('topLimit'),
                                                                          slider_component.get('incrementValue'),
                                                                          slider_component.get('number')))
    return deserialized_slider_components
