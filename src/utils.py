from tensorflow.compat.v1.keras.models import load_model
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Sequential
from sklearn.decomposition import PCA
from random import uniform
import numpy as np
import enums

ALL = 'all'
MAJOR = 'major'
MINOR = 'minor'


def split_autoencoder_trained_model_into_encoder_and_decoder_models(model):
    create_encoder_model_from_trained_autoencoder(model)
    create_decoder_model_from_trained_autoencoder(model)


def create_encoder_model_from_trained_autoencoder(model):
    encoder_model = Sequential()
    for layer in model.layers[:6]:
        encoder_model.add(layer)

    print(encoder_model.summary())
    encoder_model.load_weights(enums.AUTOENCODER_2000_WEIGHTS_FILEPATH, by_name=True)
    encoder_model.save(enums.ENCODER_2000_FILEPATH)


def create_decoder_model_from_trained_autoencoder(model):
    decoder_model = Sequential()
    decoder_model.add(Input(shape=120, name='input'))
    for layer in model.layers[6:]:
        decoder_model.add(layer)

    print(decoder_model.summary())
    decoder_model.load_weights(enums.AUTOENCODER_2000_WEIGHTS_FILEPATH, by_name=True)
    decoder_model.save(enums.DECODER_2000_FILEPATH)


def generate_and_save_samples_encoded(samples, name):
    encoder_model = load_model(enums.ENCODER_2000_FILEPATH)
    encoded_samples = []

    print('encoding ' + name + ' samples')
    for i in range(samples.shape[0]):
        midi_matrix = samples[i].reshape(1, 16, 96, 96)
        sample = encoder_model.predict(midi_matrix)
        encoded_samples.append(sample[0])
        if i % 1000 == 0:
            print(str(i) + ' samples encoded so far...')

    print(str(len(encoded_samples)) + ' samples encoded')
    np.save(enums.get_encoded_samples_filepath(name), encoded_samples)


def save_pca_components_of_samples(name):
    pca = get_pca(np.load(enums.get_encoded_samples_filepath(name)))
    print('Performing PCA on ' + name + ' samples')
    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)
    np.save(enums.get_pca_component_variance_filepath(name), pca.explained_variance_ratio_)
    np.save(enums.get_pca_component_values_filepath(name), pca.singular_values_)


def convert_pca_components_to_random_decoder_input(name):
    pca = get_pca(np.load(enums.get_encoded_samples_filepath(name)))
    encoded_samples = np.load(enums.get_encoded_samples_filepath(name))

    random_input = []
    for i in range(20):
        bottom_limit = np.percentile(pca.transform(encoded_samples), 5, axis=0)[i]
        top_limit = np.percentile(pca.transform(encoded_samples), 95, axis=0)[i]
        print('bottom limit: ' + str(bottom_limit) + ' top limit: ' + str(top_limit))
        random_input.append(uniform(bottom_limit, top_limit))
    print('pca mean: ')
    print(pca.mean_)
    return pca.inverse_transform(random_input)


def get_pca(samples):
    pca = PCA(n_components=20)
    pca.fit(samples)
    return pca


# model = load_model(enums.AUTOENCODER_2000_FILEPATH)
# split_autoencoder_trained_model_into_encoder_and_decoder_models(model)

# generate_and_save_samples_encoded(np.load('../samples/test samples/scom.npy'), 'soop')
# save_pca_components_of_samples('soop')
# generate_and_save_samples_encoded(np.load(enums.MAJOR_SAMPLES_FILEPATH), MAJOR)
# generate_and_save_samples_encoded(np.load(enums.MINOR_SAMPLES_FILEPATH), MINOR)
#
# save_pca_components_of_samples(ALL)
# save_pca_components_of_samples(MAJOR)
# save_pca_components_of_samples(MINOR)
