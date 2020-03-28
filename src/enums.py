class EnvVars:
    # ENVIRONMENT VARIABLES
    DEBUG_MODE = False
    LOCAL_MODE = True

    # HOME DIRECTORY
    PROD_HOME_DIRECTORY = '/home/jonnymoore/contextual-music-composition/'

    # LIVE SONG OUTPUTS DIRECTORY
    LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH = PROD_HOME_DIRECTORY + 'outputs/live/'

    # MODELS
    AUTOENCODER_2000_FILEPATH = PROD_HOME_DIRECTORY + 'saved models/autoencoder 2000.h5'
    ENCODER_2000_FILEPATH = PROD_HOME_DIRECTORY + 'saved models/encoder autoencoder 2000.h5'
    DECODER_2000_FILEPATH = PROD_HOME_DIRECTORY + 'saved models/decoder autoencoder 2000.h5'

    # MODEL WEIGHTS
    AUTOENCODER_2000_WEIGHTS_FILEPATH = PROD_HOME_DIRECTORY + 'saved models/autoencoder 2000 weights.h5'

    # SAMPLES
    ALL_SAMPLES_FILEPATH = PROD_HOME_DIRECTORY + 'samples/samples.npy'
    ENCODED_SAMPLES_DIRECTORY_FILEPATH = PROD_HOME_DIRECTORY + 'samples/encoded samples/'

    # CONFIG
    AZURE_CONFIG_DIRECTORY_FILEPATH = PROD_HOME_DIRECTORY + 'config/azure-config.json'


def init_env_vars():
    if EnvVars.LOCAL_MODE:
        EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH = '../outputs/live/'
        EnvVars.AUTOENCODER_2000_FILEPATH = '../saved models/autoencoder 2000.h5'
        EnvVars.ENCODER_2000_FILEPATH = '../saved models/encoder autoencoder 2000.h5'
        EnvVars.DECODER_2000_FILEPATH = '../saved models/decoder autoencoder 2000.h5'
        EnvVars.AUTOENCODER_2000_WEIGHTS_FILEPATH = '../saved models/autoencoder 2000 weights.h5'
        EnvVars.ALL_SAMPLES_FILEPATH = '../samples/samples.npy'
        EnvVars.ENCODED_SAMPLES_DIRECTORY_FILEPATH = '../samples/encoded samples/'
        EnvVars.AZURE_CONFIG_DIRECTORY_FILEPATH = '../config/azure-config.json'
    else:
        EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'outputs/live/'
        EnvVars.AUTOENCODER_2000_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'saved models/autoencoder 2000.h5'
        EnvVars.ENCODER_2000_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'saved models/encoder autoencoder 2000.h5'
        EnvVars.DECODER_2000_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'saved models/decoder autoencoder 2000.h5'
        EnvVars.AUTOENCODER_2000_WEIGHTS_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'saved models/autoencoder 2000 weights.h5'
        EnvVars.ALL_SAMPLES_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'samples/samples.npy'
        EnvVars.ENCODED_SAMPLES_DIRECTORY_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'samples/encoded samples/'
        EnvVars.AZURE_CONFIG_DIRECTORY_FILEPATH = EnvVars.PROD_HOME_DIRECTORY + 'config/azure-config.json'


def get_encoded_samples_filepath(name):
    return EnvVars.ENCODED_SAMPLES_DIRECTORY_FILEPATH + name + ' encoded samples.npy'


init_env_vars()
