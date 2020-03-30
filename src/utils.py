from tensorflow.compat.v1.keras.models import load_model
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Sequential
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
    encoder_model.load_weights(enums.EnvVars.AUTOENCODER_2000_WEIGHTS_FILEPATH, by_name=True)
    encoder_model.save(enums.EnvVars.ENCODER_2000_FILEPATH)


def create_decoder_model_from_trained_autoencoder(model):
    decoder_model = Sequential()
    decoder_model.add(Input(shape=120, name='input'))
    for layer in model.layers[6:]:
        decoder_model.add(layer)

    print(decoder_model.summary())
    decoder_model.load_weights(enums.EnvVars.AUTOENCODER_2000_WEIGHTS_FILEPATH, by_name=True)
    decoder_model.save(enums.EnvVars.DECODER_2000_FILEPATH)


def generate_and_save_samples_encoded(samples, name):
    encoder_model = load_model(enums.EnvVars.ENCODER_2000_FILEPATH)
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


# model = load_model(enums.AUTOENCODER_2000_FILEPATH)
# split_autoencoder_trained_model_into_encoder_and_decoder_models(model)

# generate_and_save_samples_encoded(np.load(enums.MAJOR_SAMPLES_FILEPATH), MAJOR)
# generate_and_save_samples_encoded(np.load(enums.MINOR_SAMPLES_FILEPATH), MINOR)
