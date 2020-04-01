from mido import MidiFile, Message, MidiTrack
from midi2audio import FluidSynth
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import os
import enums
import objects.Note

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
    # Determine time signature(s) for midi file to ensure sample parsing is completed correctly
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.is_meta:
                if msg.type == time_signature:
                    new_ticks_per_bar = (ticks_per_beat * msg.numerator) * (default_beats_per_bar / msg.denominator)
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
            # Determine when to change the time signature for sample parsing in the song
            if has_multiple_time_signatures and change_ticks_per_bar and len(song_ticks_per_bar_change_times) > 1:
                song_ticks_per_bar_index += 1
                ticks_until_ticks_per_bar_change = song_ticks_per_bar_change_times[0]
                del song_ticks_per_bar_change_times[0]
                break

            # If a note is played or silenced, add it
            if not msg.is_meta:
                delta_time_in_samples = msg.time * (samples_per_bar / song_ticks_per_bar[song_ticks_per_bar_index])

                if not msg.type == note_on:
                    sample_position_of_note_in_bar += int(delta_time_in_samples)
                    continue

                # Create a new empty 2d boolean array to represent a bar
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

                # Add a true value to the boolean array at the time a note is played against the pitch of the note
                sample_position_of_note_in_bar += int(delta_time_in_samples)
                if 16 < msg.note < 96:
                    bar_notes[msg.note][sample_position_of_note_in_bar] = True
                    if type(ticks_until_ticks_per_bar_change) is int and ticks_until_ticks_per_bar_change <= 0:
                        change_ticks_per_bar = True
                        continue

        # Most MIDI files have 2 tracks (usually one for left hand one for right hand), so we need to analyse all tracks
        if len(track_bars) > 0:
            song_bar_tracks.append(track_bars)
            sample_position_of_note_in_bar = 0
            bar_notes = np.full((number_of_notes, samples_per_bar), False, dtype=bool)
            track_bars = []

    # Return 16 bars of song to keep the learning uniform.
    if len(song_bar_tracks) == 1:
        if len(song_bar_tracks[0]) > number_of_bars:
            return song_bar_tracks[0][:number_of_bars]
        # If the song is shorter than 16 bars, add the first bar to the end until it has 16 bars, then return it
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


def samples_to_midi(samples, instrument_number, note_length, song_name, certainty_for_note_to_be_played):
    boolean_matrix = samples_to_boolean_matrix(samples, song_name, certainty_for_note_to_be_played)
    boolean_matrix_to_midi(boolean_matrix, instrument_number, note_length, song_name)


def samples_to_boolean_matrix(samples, song_name, certainty_for_note_to_be_played):
    output_midi_array = np.full((number_of_bars, number_of_notes, samples_per_bar), False, dtype=bool)
    output_midi_array_image = np.full((number_of_bars, number_of_notes, samples_per_bar), False, dtype=bool)
    if enums.EnvVars.DEBUG_MODE:
        output_directory = '../outputs/' + song_name
    else:
        output_directory = enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH
    if not os.path.exists(output_directory):
        print("Directory doesn't exist. Creating directory " + output_directory)
        os.makedirs(output_directory)

    for bar_index in range(number_of_bars):
        upper_quartile_certainty = np.percentile(samples[0, bar_index, :, :], certainty_for_note_to_be_played)
        for tick_index in range(samples_per_bar):
            for note_index in range(number_of_notes):
                if samples[0, bar_index, note_index, tick_index] > upper_quartile_certainty:
                    output_midi_array[bar_index, note_index, tick_index] = True
                    output_midi_array_image[bar_index, ((number_of_notes - 1) - note_index), tick_index] = True
        plt.imsave(output_directory + '/' + str(bar_index) + '.png', output_midi_array_image[bar_index], cmap=cm.gray)

    return output_midi_array


def boolean_matrix_to_midi(boolean_matrix, instrument_number, note_length, song_name):
    mid = MidiFile()
    track = MidiTrack()
    track.append(Message('program_change', program=instrument_number, time=0))

    ticks_per_sample = int(round(((mid.ticks_per_beat * default_beats_per_bar) / samples_per_bar)))

    notes_to_turn_off = []

    previous_message_bar_index = 0
    previous_message_sample_index = 0
    for bar_index in range(number_of_bars):
        for sample_index in range(samples_per_bar):
            # Turn off notes
            for note in notes_to_turn_off:
                if note.absolute_sample_index + note_length == (sample_index + (samples_per_bar * bar_index)):
                    delta_time = calculate_delta_time(sample_index, bar_index, previous_message_sample_index, previous_message_bar_index, ticks_per_sample)

                    track.append(Message(note_off, note=note.note, velocity=0, time=delta_time))
                    previous_message_sample_index = sample_index
                    previous_message_bar_index = bar_index
            # Turn on notes
            for note_index in range(number_of_notes):
                if boolean_matrix[bar_index, note_index, sample_index]:
                    delta_time = calculate_delta_time(sample_index, bar_index, previous_message_sample_index, previous_message_bar_index, ticks_per_sample)

                    track.append(Message(note_on, note=note_index + 16, velocity=100, time=delta_time))
                    current_note = objects.Note.define_note(note_index + 16, (sample_index + (samples_per_bar * bar_index)))
                    previous_message_sample_index = sample_index
                    previous_message_bar_index = bar_index

                    notes_to_turn_off.append(current_note)

    mid.tracks.append(track)

    if enums.EnvVars.DEBUG_MODE:
        mid.save('../outputs//' + song_name + '/' + song_name + '.mid')
    else:
        mid.save(enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.mid')
        # using the default sound font in 44100 Hz sample rate
        # fs = FluidSynth()
        # fs.midi_to_audio(enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.mid', enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.wav')
        #
        # # FLAC, a lossless codec, is supported as well (and recommended to be used)
        # fs.midi_to_audio(enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.mid', enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.flac')


def calculate_delta_time(sample_index, bar_index, previous_message_sample_index, previous_message_bar_index, ticks_per_sample):
    return (((sample_index + (samples_per_bar * bar_index)) -
             (previous_message_sample_index + (samples_per_bar * previous_message_bar_index))) * ticks_per_sample)
