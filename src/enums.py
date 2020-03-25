# DEBUG MODE ENABLED
DEBUG_MODE = False

# LIVE SONG OUTPUTS DIRECTORY
LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH = '../../outputs/live/'

# MODELS
AUTOENCODER_2000_FILEPATH = '../../saved models/autoencoder 2000.h5'
ENCODER_2000_FILEPATH = '../../saved models/encoder autoencoder 2000.h5'
DECODER_2000_FILEPATH = '../../saved models/decoder autoencoder 2000.h5'

# MODEL WEIGHTS
AUTOENCODER_2000_WEIGHTS_FILEPATH = '../../saved models/autoencoder 2000 weights.h5'

# SAMPLES
ALL_SAMPLES_FILEPATH = '../../samples/samples.npy'
ENCODED_SAMPLES_DIRECTORY_FILEPATH = '../../samples/encoded samples/'

# CONFIG
AZURE_CONFIG_DIRECTORY_FILEPATH = '../../config/azure-config.json'


def get_encoded_samples_filepath(name):
    return ENCODED_SAMPLES_DIRECTORY_FILEPATH + name + ' encoded samples.npy'
