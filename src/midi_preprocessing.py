from mido import MidiFile
import numpy as np

samples_per_bar = 96
samples_per_tick = 0
quarter_notes_per_bar = 4
time_signature = 'time_signature'
note_on = 'note_on'
note_off = 'note_off'

def midi_to_samples(midi_file_name):
    mid = MidiFile(midi_file_name)

    has_time_signature = False
    ticks_per_beat = mid.ticks_per_beat
    default_ticks_per_bar = quarter_notes_per_bar * ticks_per_beat

    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.is_meta and msg.type == time_signature:
                new_ticks_per_bar = (ticks_per_beat * msg.numerator) * (quarter_notes_per_bar / msg.denominator)
                if has_time_signature and new_ticks_per_bar != ticks_per_bar:
                    has_multiple_time_signatures = True
                else:
                    ticks_per_bar = new_ticks_per_bar
                    samples_per_tick = (samples_per_bar / ticks_per_bar)
                    has_time_signature = True
    if has_multiple_time_signatures:
        print(midi_file_name + 'has multiple time signatures')

    song_bars = []
    bar_notes = np.zeros((128, 96))
    sample_position_of_note_per_bar = 0
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if not msg.is_meta:
                if msg.type == note_on and msg.velocity != 0:
                    note = msg.note
                    delta_time = msg.time * samples_per_tick
                    if delta_time >= samples_per_bar - sample_position_of_note_per_bar:
                        song_bars.append(bar_notes)
                        bar_notes = np.zeros((128, 96))
                        delta_time -= (samples_per_bar - sample_position_of_note_per_bar)
                        while delta_time >= samples_per_bar:
                            delta_time -= samples_per_bar
                    sample_position_of_note_per_bar += int(delta_time)
                    bar_notes[msg.note][sample_position_of_note_per_bar] = 1

    print('hello')