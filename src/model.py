import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input,Conv2D,MaxPooling2D,UpSampling2D
from tensorflow.compat.v1.keras.models import Model,load_model
from tensorflow.keras.optimizers import RMSprop

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

midi_matrices = np.load('samples.npy', allow_pickle=True)
midi_matrices = np.expand_dims(midi_matrices[0], axis=3)
midi_matrix = Input(shape=(128, 96, 1))
print(midi_matrices.shape)

def autoencoder(midi_matrix):
    #encoder
    #input = 128 x 96 x 1 (wide and thin)
    conv1 = Conv2D(32, (6, 6), activation='relu', padding='same')(midi_matrix) #128 x 96 x 32
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1) #64 x 48 x 64
    conv2 = Conv2D(64, (6, 6), activation='relu', padding='same')(pool1) #64 x 48 x 64
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2) #32 x 24 x 128
    conv3 = Conv2D(128, (6, 6), activation='relu', padding='same')(pool2) #32 x 24 x 128 (small and thick)

    #decoder
    conv4 = Conv2D(128, (6, 6), activation='relu', padding='same')(conv3) #32 x 24 x 128
    up1 = UpSampling2D((2,2))(conv4) # 14 x 14 x 128
    conv5 = Conv2D(64, (6, 6), activation='relu', padding='same')(up1) # 64 x 48 x 64
    up2 = UpSampling2D((2,2))(conv5) # 28 x 28 x 64
    decoded = Conv2D(1, (6, 6), activation='sigmoid', padding='same')(up2) # 28 x 28 x 1
    return decoded

autoencoder = Model(midi_matrix, autoencoder(midi_matrix))
autoencoder.compile(loss='mean_squared_error', optimizer=RMSprop())
print(autoencoder.summary())

autoencoder_train = autoencoder.fit(midi_matrices, midi_matrices, batch_size=128, epochs=30, verbose=1, validation_split=0.1)
autoencoder.save(r"C:\Users\Jonny\Downloads\Uni project\midis\automan.h5")

model = load_model(r"C:\Users\Jonny\Downloads\Uni project\midis\automan.h5")

a = model.predict(midi_matrices)
print(a.shape)

plt.imshow(a[0, :, :, 0], cmap='gray')
plt.show()
print()