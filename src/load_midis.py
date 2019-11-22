import midi_preprocessing
import os

midi_filepath = r"C:\Users\Jonny\Downloads\Uni project\midis\vgmusic"
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
        except:
            print('ERROR ', path)
            continue
