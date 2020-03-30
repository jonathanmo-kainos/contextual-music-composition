import numpy as np
from sklearn.decomposition import PCA
from random import uniform
import enums
import objects.PCASliderComponent

NUM_PCA_COMPONENTS = 20


def convert_pca_components_to_random_decoder_input(name):
    pca = get_pca(np.load(enums.get_encoded_samples_filepath(name)))
    encoded_samples = np.load(enums.get_encoded_samples_filepath(name))
    random_input = []
    slider_components = []

    for i in range(NUM_PCA_COMPONENTS):
        bottom_limit = np.percentile(pca.transform(encoded_samples), 5, axis=0)[i]
        top_limit = np.percentile(pca.transform(encoded_samples), 95, axis=0)[i]
        increment_value_between_limits = (top_limit - bottom_limit) / 500

        random_number_between_limits = uniform(bottom_limit, top_limit)
        random_input.append(random_number_between_limits)

        slider_components.append(objects.PCASliderComponent.define_pca_slider_component(bottom_limit, top_limit, increment_value_between_limits, random_number_between_limits))

        if enums.EnvVars.DEBUG_MODE:
            print('bottom limit: ' + str(bottom_limit) + ' top limit: ' + str(top_limit))

    if enums.EnvVars.DEBUG_MODE:
        print('pca mean: ')
        print(pca.mean_)

    return pca.inverse_transform(random_input), slider_components


def convert_specified_slider_values_to_decoder_input(name, user_slider_values):
    pca = get_pca(np.load(enums.get_encoded_samples_filepath(name)))
    encoded_samples = np.load(enums.get_encoded_samples_filepath(name))
    specified_decoder_input = []

    for i in range(10):
        specified_decoder_input.append(user_slider_values[i])

    for i in range(10, NUM_PCA_COMPONENTS):
        bottom_limit = np.percentile(pca.transform(encoded_samples), 5, axis=0)[i]
        top_limit = np.percentile(pca.transform(encoded_samples), 95, axis=0)[i]

        random_number_between_limits = uniform(bottom_limit, top_limit)
        specified_decoder_input.append(random_number_between_limits)

        if enums.EnvVars.DEBUG_MODE:
            print('bottom limit: ' + str(bottom_limit) + ' top limit: ' + str(top_limit))

    if enums.EnvVars.DEBUG_MODE:
        print('pca mean: ')
        print(pca.mean_)

    return pca.inverse_transform(specified_decoder_input)


def get_pca(samples):
    pca = PCA(n_components=NUM_PCA_COMPONENTS)
    pca.fit(samples)
    return pca
