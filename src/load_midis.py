import midi_preprocessing
import os

patterns = {}
midi_dir = r"C:\Users\Jonny\Downloads\Uni project\midis\bigbutt"
all_samples = []
all_lens = []
print
"Loading Songs..."
for root, subdirs, files in os.walk(midi_dir):
    for file in files:
        path = root + "\\" + file
        if not (path.endswith('.mid') or path.endswith('.midi')):
            continue
        try:
            samples = midi_preprocessing.midi_to_samples(path)
        except:
            print
            "ERROR ", path
            continue