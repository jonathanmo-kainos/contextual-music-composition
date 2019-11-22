import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input,Conv2D,MaxPooling2D,UpSampling2D,TimeDistributed,BatchNormalization,ConvLSTM2D,Conv3D
from tensorflow.keras.optimizers import RMSprop

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

midi_matrices = np.load('samples.npy')
print(midi_matrices.shape)
midi_matrices = np.expand_dims(midi_matrices, axis=4)
midi_matrix = Input(shape=(128, 96, 1))
print(midi_matrices.shape)

# def autoencoder(midi_matrix):
seq = Sequential()
seq.add(ConvLSTM2D(filters=20, kernel_size=(3, 3),
                   input_shape=(16, 128, 96, 1),
                   padding='same', return_sequences = True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=20, kernel_size=(3, 3),
                   padding='same', return_sequences = True))
seq.add(BatchNormalization())

# seq.add(ConvLSTM2D(filters=20, kernel_size=(3, 3),
#                    padding='same', return_sequences = True))
# seq.add(BatchNormalization())
#
# seq.add(ConvLSTM2D(filters=20, kernel_size=(3, 3),
#                    padding='same', return_sequences = True))
# seq.add(BatchNormalization())

seq.add(Conv3D(filters=1, kernel_size=(3, 3, 3),
               activation='sigmoid',
padding ='same', data_format ='channels_last'))
seq.compile(loss='binary_crossentropy', optimizer ='adadelta')

seq.fit(midi_matrices, midi_matrices, batch_size=5, epochs=150, validation_split=0.05)
    # #encoder
    # #input = 128 x 96 x 1 (wide and thin)
    # conv1 = Conv2D(32, (6, 6), activation='relu', padding='same')(midi_matrix) #128 x 96 x 32
    # print(conv1.shape)
    # pool1 = MaxPooling2D(pool_size=(2, 2))(conv1) #64 x 48 x 64
    # print(pool1.shape)
    # pool1 = TimeDistributed(BatchNormalization(momentum=0.9))(pool1)
    # print(pool1.shape)
    # conv2 = TimeDistributed(Conv2D(64, (6, 6), activation='relu', padding='same'))(pool1) #64 x 48 x 64
    # print(conv2.shape)
    # pool2 = MaxPooling2D(pool_size=(2, 2))(conv2) #32 x 24 x 128
    # print(pool2.shape)
    # pool2 = TimeDistributed(BatchNormalization(momentum=0.9))(pool2)
    # print(pool2.shape)
    # conv3 = Conv2D(128, (6, 6), activation='relu', padding='same')(pool2) #32 x 24 x 128 (small and thick)
    # print(conv3.shape)
    #
    # #decoder
    # conv4 = TimeDistributed(Conv2D(128, (6, 6), activation='relu', padding='same'))(conv3) #32 x 24 x 128
    # up1 = UpSampling2D((2,2))(conv4) # 14 x 14 x 128
    # up1 = TimeDistributed(BatchNormalization(momentum=0.9))(up1)
    # conv5 = TimeDistributed(Conv2D(64, (6, 6), activation='relu', padding='same'))(up1) # 64 x 48 x 64
    # up2 = UpSampling2D((2,2))(conv5) # 28 x 28 x 64
    # up2 = TimeDistributed(BatchNormalization(momentum=0.9))(up2)
    # decoded = Conv2D(1, (6, 6), activation='sigmoid', padding='same')(up2) # 28 x 28 x 1
    # return decoded

# autoencoder = Model(midi_matrix, autoencoder(midi_matrix))
# autoencoder.compile(loss='mean_squared_error', optimizer=RMSprop())
# print(autoencoder.summary())

# autoencoder_train = autoencoder.fit(midi_matrices, midi_matrices, batch_size=128, epochs=30, verbose=1, validation_split=0.1)
seq.save(r"C:\Users\Jonny\Downloads\Uni project\midis\butthole\convlstm2d.h5")