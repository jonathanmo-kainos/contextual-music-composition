import midi_preprocessing
import os
import numpy as np
import logging

midi_filepath = r"C:\Users\Jonny\Downloads\Uni project\midis"
all_samples = []
print('Loading midis')
for root, subdirs, files in os.walk(midi_filepath):
    for file in files:
        path = root + "\\" + file
        if not (path.endswith('.mid') or path.endswith('.midi')):
            continue
        try:
            samples = midi_preprocessing.midi_to_samples(path)
            all_samples.append(samples)
        except Exception as e:
            print('ERROR ', path)
            logging.exception("message")
            continue

np.save('samples bool.npy', all_samples)
