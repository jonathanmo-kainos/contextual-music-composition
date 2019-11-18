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
    song_length_in_ticks = mid.length
    ticks_per_bar = 0

    song_ticks_per_bar_change_times = []
    song_ticks_per_bar = []
    song_bars = []
    bar_notes = np.zeros((128, 96), dtype=np.uint8)
    sample_position_of_note_per_bar = 0

    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.is_meta:
                if msg.type == 'track_name':
                    print(msg.name)
                if msg.type == 'set_tempo':
                    print(msg.tempo)
                if msg.type == time_signature:
                    new_ticks_per_bar = (ticks_per_beat * msg.numerator) * (quarter_notes_per_bar / msg.denominator)
                    print(msg.numerator, '/', msg.denominator, ' ', msg.time)
                    if has_time_signature and new_ticks_per_bar != ticks_per_bar:
                        has_multiple_time_signatures = True
                        song_ticks_per_bar.append(new_ticks_per_bar)
                        song_ticks_per_bar_change_times.append(msg.time)
                    else:
                        has_time_signature = True
                        song_ticks_per_bar.append(new_ticks_per_bar)
                        song_ticks_per_bar_change_times.append(msg.time)
        for index, ticks_per_bar in song_ticks_per_bar:
            current_ticks_per_bar = song_ticks_per_bar[index]
            if len(song_ticks_per_bar_change_times) != 1:
                time_until_ticks_per_bar_change = song_ticks_per_bar_change_times[index]
            for msg in track:
                if not msg.is_meta:
                    if msg.type == note_on and msg.velocity != 0:
                        note = msg.note
                        samples_per_tick = (samples_per_bar / ticks_per_bar)
                        delta_time = msg.time * samples_per_tick
                        if delta_time >= samples_per_bar - sample_position_of_note_per_bar:
                            song_bars.append(bar_notes)
                            bar_notes = np.zeros((128, 96))
                            delta_time -= (samples_per_bar - sample_position_of_note_per_bar)
                            while delta_time >= samples_per_bar:
                                delta_time -= samples_per_bar
                        sample_position_of_note_per_bar += int(delta_time)
                        bar_notes[msg.note][sample_position_of_note_per_bar] = 1

        if has_multiple_time_signatures:
            print(midi_file_name, ' has multiple time signatures')


    print('hello')