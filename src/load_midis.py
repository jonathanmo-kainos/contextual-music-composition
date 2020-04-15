import midi_preprocessing
import music21
import os
import numpy as np
import logging

midi_filepath = r"MIDI FILEPATH HERE"

all_samples = []
major_samples = []
minor_samples = []

print('Loading midis')
for root, subdirs, files in os.walk(midi_filepath):
    for file in files:
        path = root + "\\" + file
        if not (path.endswith('.mid') or path.endswith('.midi')):
            continue
        try:
            score = music21.converter.parse(path)
            key = score.analyze('key')

            samples = midi_preprocessing.midi_to_samples(path)
            if key.mode == 'major':
                major_samples.append(samples)
            elif key.mode == 'minor':
                minor_samples.append(samples)

        except Exception as e:
            print('ERROR ', path)
            logging.exception("message")
            continue

np.save('major samples.npy', major_samples)
np.save('minor samples.npy', minor_samples)
