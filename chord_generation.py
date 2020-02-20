import itertools
import os
import json
import music21

class Chord_progression_generator:
    """A class responsible for brute forcing the generation of all possible chord sequences."""

    def __init__(self):
        """Constructor for the class. """

        # fundamental major/minor chord templates indicated in pitch classes
        self.major_chord_template = [0, 4, 7]
        self.minor_chord_template = [0, 3, 7]

        C4 = 48 # midi note for C on 4th octave
        B4 = 59 # midi note for B on 4th octave

        # list comprising 24 minor/major chord templates starting from C
        self.chord_templates = [[pc+i for pc in self.major_chord_template] for i in range(C4, B4+1)] + \
                               [[pc+i for pc in self.minor_chord_template] for i in range(C4, B4+1)]


    def generate_chord_progressions(self, num_chords):
        """Generates all possible chord sequences for a specified number of chords.

        :param: num_chords (int): Number of chords in the sequence
        :return chord_progressions (list of list): List containing all possible chord progressions
        """
        chord_progressions = []

        # use cartesian product to brute force the generation of all possible chord progressions
        args = [self.chord_templates for _ in range(num_chords)]
        for chord_progression in itertools.product(*args):
            chord_progressions.append(list(chord_progression))
        print("Brute forced all possible progressions for sequences containing {} chords!\n".format(num_chords))

        return chord_progressions


    def save_chord_progressions(self, chord_progressions, dir_path, file_type="midi"):
        """Saves all chord progressions to midi file.

        :param chord_progressions (list of list): List containing chord progressions to save
        :param dir_path (str): Path to directory where to save file
        :param file_type (str): File format that should be used to save chord_sequences. Detaults to "midi". Other
                                options is "xml", for musicXML and "json"
        """
        tot_chord_sequences = len(chord_progressions)

        # manage saving with midi or xml type of file
        if file_type == "midi" or file_type == "xml":

            # loop through all chord progressions and save them to file
            for i, chord_progression in enumerate(chord_progressions):

                    # file name is based on index of chord progression
                    file_name = str(i) + "." + file_type
                    file_path = os.path.join(dir_path, file_name)
                    self._save_chord_progression(chord_progression, file_path, file_type)

                    if (i + 1) % 100 == 0:
                        print("Saved {} chord progression out of {}".format(i + 1, tot_chord_sequences))

        # manage saving to json file
        elif file_type == "json":
            file_path = os.path.join(dir_path, "chord_progressions.json")
            with open(file_path, "w") as fp:
                json.dump(chord_progressions, fp, indent=4)

        print("Successfully saved chord progressions at {}\n".format(file_path))


    def _save_chord_progression(self, chord_progression, file_path, file_type="midi"):
        """Saves a chord progression to file using music21.

        :param chord_progression (list): Chord progression to save
        :param file_path (str): Path where to save file
        :param file_type (str): File format that should be used to save chord_sequences. Detaults to "midi". Other option is
                                "xml", for musicXML
        """

        # create music21 stream
        stream = music21.stream.Stream()

        # convert chords from midi note format to music21 chords
        music21_chords = []
        for c in chord_progression:
            music21_chords.append(music21.chord.Chord(c))

        # create a music21 part and append chords in the part
        part = music21.stream.Part()
        for c in music21_chords:
            part.append(c)

        # insert part in the music21 stream and save it to file
        stream.insert(part)
        stream.write(file_type, fp=file_path)


if __name__ == "__main__":

    # instantiate a chord progression generator
    csg = Chord_progression_generator()

    # generate all chord sequences with 4 chords
    chord_progressions = csg.generate_chord_progressions(4)

    # save chord sequences to json file
    csg.save_chord_progressions(chord_progressions, ".", file_type="json")

    csg.save_chord_progressions(chord_progressions, "chord_sequences2", file_type="midi")




