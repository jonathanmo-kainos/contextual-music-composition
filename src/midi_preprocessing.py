from mido import MidiFile
import numpy as np

samples_per_bar = 96
number_of_notes = 128

samples_per_tick = 0
quarter_notes_per_bar = 4
time_signature = 'time_signature'
note_on = 'note_on'
note_off = 'note_off'

def midi_to_samples(midi_file_name):
    mid = MidiFile(midi_file_name)

    has_time_signature = False
    has_multiple_time_signatures = False
    ticks_per_beat = mid.ticks_per_beat
    ticks_per_bar = 0

    song_ticks_per_bar_change_times = []
    song_ticks_per_bar = []

    song_bars = []
    song_bar_tracks = []
    track_bars = []
    bar_notes = np.full((number_of_notes, samples_per_bar), False, dtype=bool)

    sample_position_of_note_in_bar = 0
    ticks_until_ticks_per_bar_change = None
    change_ticks_per_bar = False
    song_ticks_per_bar_index = 0

    print(midi_file_name)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.is_meta:
                if msg.type == time_signature:
                    new_ticks_per_bar = (ticks_per_beat * msg.numerator) * (quarter_notes_per_bar / msg.denominator)
                    print(msg.numerator, '/', msg.denominator, ' ', msg.time)
                    if has_time_signature and new_ticks_per_bar != ticks_per_bar:
                        has_multiple_time_signatures = True
                        song_ticks_per_bar.append(new_ticks_per_bar)
                        song_ticks_per_bar_change_times.append(msg.time)
                    else:
                        ticks_per_bar = new_ticks_per_bar
                        has_time_signature = True
                        song_ticks_per_bar.append(new_ticks_per_bar)
                        song_ticks_per_bar_change_times.append(msg.time)

        if has_multiple_time_signatures:
            print(midi_file_name, ' has multiple time signatures')

    for i, track in enumerate(mid.tracks):
        for msg in track:

            if has_multiple_time_signatures and change_ticks_per_bar and len(song_ticks_per_bar_change_times) > 1:
                song_ticks_per_bar_index += 1
                ticks_until_ticks_per_bar_change = song_ticks_per_bar_change_times[0]
                del song_ticks_per_bar_change_times[0]
                break

            if not msg.is_meta and msg.type == note_on:
                delta_time_in_samples = msg.time * (samples_per_bar / song_ticks_per_bar[song_ticks_per_bar_index])
                if msg.velocity == 0:
                    sample_position_of_note_in_bar += int(delta_time_in_samples)
                    continue
                if delta_time_in_samples >= samples_per_bar - sample_position_of_note_in_bar:
                    track_bars.append(bar_notes)
                    bar_notes = np.full((number_of_notes, samples_per_bar), False, dtype=bool)
                    delta_time_in_samples -= (samples_per_bar - sample_position_of_note_in_bar)
                    sample_position_of_note_in_bar = 0
                    while delta_time_in_samples >= samples_per_bar:
                        delta_time_in_samples -= samples_per_bar
                        if type(ticks_until_ticks_per_bar_change) is int:
                            ticks_until_ticks_per_bar_change -= samples_per_bar
                            if ticks_until_ticks_per_bar_change <= 0:
                                change_ticks_per_bar = True
                                break
                    if change_ticks_per_bar:
                        continue
                sample_position_of_note_in_bar += int(delta_time_in_samples)
                bar_notes[msg.note][sample_position_of_note_in_bar] = True
                if type(ticks_until_ticks_per_bar_change) is int and ticks_until_ticks_per_bar_change <= 0:
                    change_ticks_per_bar = True
                    continue

        if len(track_bars) > 0:
            song_bar_tracks.append(track_bars)
            sample_position_of_note_in_bar = 0
            bar_notes = np.full((number_of_notes, samples_per_bar), False, dtype=bool)
            track_bars = []

    for bar_index in range(len(song_bar_tracks[0])):
        joint_bar = song_bar_tracks[0][bar_index] | song_bar_tracks[1][bar_index]
        song_bars.append(joint_bar)

    return song_bars
