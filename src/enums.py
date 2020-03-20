# MODELS
AUTOENCODER_300_FILEPATH = '../saved models/test models/autoencoder 300.h5'
AUTOENCODER_2000_FILEPATH = '../saved models/autoencoder 2000.h5'
ENCODER_2000_FILEPATH = '../saved models/encoder autoencoder 2000.h5'
DECODER_2000_FILEPATH = '../saved models/decoder autoencoder 2000.h5'

# MODEL WEIGHTS
AUTOENCODER_2000_WEIGHTS_FILEPATH = '../saved models/autoencoder 2000 weights.h5'

# SAMPLES
ALL_SAMPLES_FILEPATH = '../samples/samples.npy'
MAJOR_SAMPLES_FILEPATH = '../samples/major samples.npy'
MINOR_SAMPLES_FILEPATH = '../samples/minor samples.npy'
ENCODED_SAMPLES_DIRECTORY_FILEPATH = '../samples/encoded samples/'

# PCA COMPONENTS
PCA_COMPONENT_VALUES_FILEPATH = '../samples/pca samples/'

# RANDOM INPUTS
RANDOM_INPUT_FILEPATH = '../inputs/randomInput.npy'


def get_encoded_samples_filepath(name):
    return ENCODED_SAMPLES_DIRECTORY_FILEPATH + name + '/encoded samples.npy'


def get_pca_component_values_filepath(name):
    return PCA_COMPONENT_VALUES_FILEPATH + name + '/pca component values.npy'


def get_pca_component_variance_filepath(name):
    return PCA_COMPONENT_VALUES_FILEPATH + name + '/pca component variance.npy'
