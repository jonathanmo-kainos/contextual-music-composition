from mido import MidiFile, Message, MidiTrack
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import os

samples_per_bar = 96
number_of_notes = 96
number_of_bars = 16

samples_per_tick = 0
default_beats_per_bar = 4
default_time_signature_numerator = 4
default_time_signature_denominator = 4

time_signature = 'time_signature'
note_on = 'note_on'
note_off = 'note_off'


def midi_to_samples(midi_file_name):
    mid = MidiFile(midi_file_name, clip=True)

    has_time_signature = False
    has_multiple_time_signatures = False
    ticks_per_beat = mid.ticks_per_beat
    ticks_per_bar = 0
    new_ticks_per_bar = (ticks_per_beat * default_time_signature_numerator) * (
                default_beats_per_bar / default_time_signature_denominator)

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
                    new_ticks_per_bar = (ticks_per_beat * msg.numerator) * (default_beats_per_bar / msg.denominator)
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

        if not has_time_signature:
            song_ticks_per_bar.append(new_ticks_per_bar)
    if has_multiple_time_signatures:
        print(midi_file_name, ' has multiple time signatures')

    for i, track in enumerate(mid.tracks):
        for msg in track:

            if has_multiple_time_signatures and change_ticks_per_bar and len(song_ticks_per_bar_change_times) > 1:
                song_ticks_per_bar_index += 1
                ticks_until_ticks_per_bar_change = song_ticks_per_bar_change_times[0]
                del song_ticks_per_bar_change_times[0]
                break

            if not msg.is_meta:
                delta_time_in_samples = msg.time * (samples_per_bar / song_ticks_per_bar[song_ticks_per_bar_index])
                if not msg.type == note_on:
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
                if 16 < msg.note < 96:
                    bar_notes[msg.note][sample_position_of_note_in_bar] = True
                    if type(ticks_until_ticks_per_bar_change) is int and ticks_until_ticks_per_bar_change <= 0:
                        change_ticks_per_bar = True
                        continue

        if len(track_bars) > 0:
            song_bar_tracks.append(track_bars)
            sample_position_of_note_in_bar = 0
            bar_notes = np.full((number_of_notes, samples_per_bar), False, dtype=bool)
            track_bars = []

    if len(song_bar_tracks) == 1:
        if len(song_bar_tracks[0]) > number_of_bars:
            return song_bar_tracks[0][:number_of_bars]
        while len(song_bar_tracks[0]) < number_of_bars:
            song_bar_tracks[0].append(song_bar_tracks[0][0])
        return song_bar_tracks[0]

    for bar_index in range(min(len(song_bar_tracks[0]), len(song_bar_tracks[1]))):
        joint_bar = song_bar_tracks[0][bar_index] | song_bar_tracks[1][bar_index]
        song_bars.append(joint_bar)
        if bar_index == 15:
            break

    while len(song_bars) != number_of_bars:
        song_bars.append(song_bars[0])

    return song_bars


def samples_to_midi(samples, instrument_number, song_name):
    boolean_matrix = samples_to_boolean_matrix(samples, song_name)
    boolean_matrix_to_midi(boolean_matrix, instrument_number, song_name)


def samples_to_boolean_matrix(samples, song_name):
    output_midi_array = np.full((number_of_bars, number_of_notes, samples_per_bar), False, dtype=bool)
    output_midi_array_image = np.full((number_of_bars, number_of_notes, samples_per_bar), False, dtype=bool)
    directory = r'..\outputs\\' + song_name
    if not os.path.exists(directory):
        print("Directory doesn't exist. Creating directory " + directory)
        os.makedirs(directory)

    for bar_index in range(number_of_bars):
        upper_quartile_certainty = np.percentile(samples[0, bar_index, :, :], 99.9)
        for tick_index in range(samples_per_bar):
            for note_index in range(number_of_notes):
                if samples[0, bar_index, note_index, tick_index] > upper_quartile_certainty:
                    output_midi_array[bar_index, note_index, tick_index] = True
                    output_midi_array_image[bar_index, (number_of_notes - note_index), tick_index] = True

        plt.imsave(directory + r'\\' + str(bar_index) + '.png', output_midi_array_image[bar_index], cmap=cm.gray)

    return output_midi_array


def boolean_matrix_to_midi(boolean_matrix, instrument_number, song_name):
    mid = MidiFile()
    track = MidiTrack()
    track.append(Message('program_change', program=instrument_number, time=0))

    ticks_per_sample = int(round(((mid.ticks_per_beat * default_beats_per_bar) / samples_per_bar)))

    for bar_index in range(number_of_bars):
        previous_active_sample_index = 0
        for sample_index in range(samples_per_bar):
            for note_index in range(number_of_notes):
                if boolean_matrix[bar_index, note_index, sample_index]:
                    delta_time = (sample_index * ticks_per_sample) - (previous_active_sample_index * ticks_per_sample)
                    track.append(Message(note_on, note=note_index + 16, velocity=100, time=delta_time))

                    previous_active_sample_index = sample_index

    mid.tracks.append(track)

    mid.save(r'..\outputs\\' + song_name + '.mid')
