class Note(object):
    note = 0
    absolute_sample_index = 0

    def __init__(self, note, absolute_sample_index):
        self.note = note
        self.absolute_sample_index = absolute_sample_index


def define_note(note, absolute_sample_index):
    return Note(note, absolute_sample_index)
