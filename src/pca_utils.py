import numpy as np
from sklearn.decomposition import PCA
from random import uniform
import enums
import objects.PCASliderComponent

NUM_PCA_COMPONENTS = 100
NUM_INCREMENTS = 500


def convert_pca_components_to_random_decoder_input(name):
    pca = get_pca(np.load(enums.get_encoded_samples_filepath(name)))
    encoded_samples = np.load(enums.get_encoded_samples_filepath(name))
    random_input = []
    slider_components = []

    for i in range(NUM_PCA_COMPONENTS):
        random_input, slider_components = generate_random_number_between_pca_limits(pca, encoded_samples,
                                                                                    random_input,
                                                                                    slider_components, i)

    if enums.EnvVars.DEBUG_MODE:
        print('pca mean: ')
        print(pca.mean_)

    return pca.inverse_transform(random_input), slider_components


def get_decoder_input_from_slider_configs(name, randomise_on_screen_sliders, randomise_off_screen_sliders,
                                          pca_slider_components):
    pca = get_pca(np.load(enums.get_encoded_samples_filepath(name)))
    encoded_samples = np.load(enums.get_encoded_samples_filepath(name))
    specified_decoder_input = []
    slider_components = []

    for i in range(10):
        if randomise_on_screen_sliders:
            specified_decoder_input, slider_components = generate_random_number_between_pca_limits(pca, encoded_samples,
                                                                                                   specified_decoder_input,
                                                                                                   slider_components, i)
        else:
            specified_decoder_input.append(pca_slider_components[i].number)
            slider_components.append(pca_slider_components[i])

    for i in range(10, NUM_PCA_COMPONENTS):
        if randomise_off_screen_sliders:
            specified_decoder_input, slider_components = generate_random_number_between_pca_limits(pca, encoded_samples,
                                                                                                   specified_decoder_input,
                                                                                                   slider_components, i)
        else:
            specified_decoder_input.append(pca_slider_components[i].number)
            slider_components.append(pca_slider_components[i])

    if enums.EnvVars.DEBUG_MODE:
        print('pca mean: ')
        print(pca.mean_)

    return pca.inverse_transform(specified_decoder_input), slider_components


def generate_random_number_between_pca_limits(pca, encoded_samples, decoder_input, slider_components, current_slider):
    bottom_limit = np.percentile(pca.transform(encoded_samples), 5, axis=0)[current_slider]
    top_limit = np.percentile(pca.transform(encoded_samples), 95, axis=0)[current_slider]
    increment_value_between_limits = (top_limit - bottom_limit) / NUM_INCREMENTS
    random_number_between_limits = uniform(bottom_limit, top_limit)

    decoder_input.append(random_number_between_limits)
    slider_components.append(
        objects.PCASliderComponent.define_pca_slider_component(bottom_limit, top_limit, increment_value_between_limits,
                                                               random_number_between_limits))

    if enums.EnvVars.DEBUG_MODE:
        print('bottom limit: ' + str(bottom_limit) + ' top limit: ' + str(top_limit))

    return decoder_input, slider_components


def get_pca(samples):
    pca = PCA(n_components=NUM_PCA_COMPONENTS)
    pca.fit(samples)
    return pca
