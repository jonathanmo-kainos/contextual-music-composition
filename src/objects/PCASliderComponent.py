class PCASliderComponent(object):
    bottom_limit = 0
    top_limit = 0
    increment_value = 0
    random_number = 0

    def __init__(self, bottom_limit, top_limit, increment_value, random_number):
        self.bottom_limit = bottom_limit
        self.top_limit = top_limit
        self.increment_value = increment_value
        self.random_number = random_number


def define_pca_slider_component(bottom_limit, top_limit, increment_value, random_number):
    return PCASliderComponent(bottom_limit, top_limit, increment_value, random_number)


def serialize(self):
    return {
        'bottomLimit': self.bottom_limit,
        'topLimit': self.top_limit,
        'incrementValue': self.increment_value,
        'randomNumber': self.random_number
    }
