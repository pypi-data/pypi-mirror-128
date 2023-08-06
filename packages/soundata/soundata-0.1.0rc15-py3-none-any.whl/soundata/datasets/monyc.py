"""MONYC Dataset Loader

.. admonition:: Dataset Info
    :class: dropdown

    Created By
    ----------

    Magdalena Fuentes*, Danielle Zhao*, Vincent Lostanlen^, Mark Cartwright+, Charlie Mydlarz* and Juan Pablo Bello*
    * New York University, USA
    ^ CNRS, Laboratoire des Sciences du Numerique de Nantes (LS2N), France
    + New Jersey Institute of Technology, USA
    https://steinhardt.nyu.edu/marl
    http://cusp.nyu.edu/

    Version 0.1.0


    Description
    -----------

    The MONYC dataset contains 1587 labeled 10-second sound excerpts of music recorded in urban settings. It provides
    examples of how music manifests itself in a real-world setting among social interactions in an urban context, with
    variant signal-to-noise-ratio and interfering sources.
    MONYC was created using a combination of urban sound tagging; self-supervised learning; point process
    modeling; and human labeling. It conveys rich metadata including timestamps and spatial location of clips,
    along with binary scene descriptors to assess models in different conditions (e.g. high interference of non-musical
    sources).

    The audio was recorded from the `SONYC <https://wp.nyu.edu/sonyc/>`_ acoustic sensor network. Four annotators tagged
    the music genre of the recordings. Each clip has annotations from two annotators. A final stage of agreement was
    performed and the tags were refined to a final taxonomy. Both the refined and individual annotations are released.

    The following article provides a detailed description of the dataset and how it was compiled:

    .. code-block:: latex
        M. Fuentes, D. Zhao, V. Lostanlen, M. Cartwright, C. Mydlarz and J. P. Bello, "MONYC: Music of New York City
        Dataset", Workshop on Detection and Classification of Acoustic Scenes and Events, Nov. 2021.

    In addition to the sound excerpts, a CSV file containing metadata about each excerpt is also provided.


    Audio Files Included
    --------------------

    1587 10-second clips of music recorded from the SONYC acoustic network in urban settings in WAV format, 48kHz, mono.

    Meta-data Files Included
    ------------------------

    monyc.csv

    This file contains meta-data information about every audio file in the dataset, including:

    * filename:
    The name of the audio file. The name takes the following format: [fsID]-[classID]-[occurrenceID]-[sliceID].wav, where:
    [fsID] = the Freesound ID of the recording from which this excerpt (slice) is taken
    [classID] = a numeric identifier of the sound class (see description of classID below for further details)
    [occurrenceID] = a numeric identifier to distinguish different occurrences of the sound within the original recording
    [sliceID] = a numeric identifier to distinguish different slices taken from the same occurrence

    * genres:
    The list of music genres present in the clip ordered by agreement. The first tag is agreed among annotators,
    the following ones are genres provided by each annotator.


    * annotators_id
    The list of the annotators id (two per clip).

    * live:
    Boolean indicating if the music is played live.

    * single_instrument:
    Boolean indicating if there is only one instrument present (True) or if there are multiple (False).

    * loud:
    Boolean indicating if the music is perceived to be loud in the recording.

    * classID:
    A numeric identifier of the sound class:

    * class:
    The class name: air_conditioner, car_horn, children_playing, dog_bark, drilling, engine_idling, gun_shot, jackhammer,
    siren, street_music.


    Please Acknowledge MONYC in Academic Research
    ----------------------------------------------------

    When MONYC is used for academic research, we would highly appreciate it if scientific publications of works
    partly based on the MONYC dataset cite the following publication:

    .. code-block:: latex
        M. Fuentes, D. Zhao, V. Lostanlen, M. Cartwright, C. Mydlarz and J. P. Bello, "MONYC: Music of New York City
        Dataset", Workshop on Detection and Classification of Acoustic Scenes and Events, Nov. 2021.


    Conditions of Use
    -----------------

    Dataset compiled by Magdalena Fuentes, Danielle Zhao, Vincent Lostanlen, Mark Cartwright, Charlie Mydlarz and Juan
    Pablo Bello. All files are recordings from the `SONYC <https://wp.nyu.edu/sonyc/>`_ acoustic sensor network.

    The MONYC dataset is offered free of charge for non-commercial use only under the terms of the Creative Commons
    Attribution 4.0 International (CC-BY 4.0): https://creativecommons.org/licenses/by/4.0/

    The dataset and its contents are made available on an "as is" basis and without warranties of any kind, including
    without limitation satisfactory quality and conformity, merchantability, fitness for a particular purpose, accuracy or
    completeness, or absence of errors. Subject to any liability that may not be excluded or limited by law, NYU is not
    liable for, and expressly excludes, all liability for loss or damage however and whenever caused to anyone by any use of
    the MONYC dataset or any part of it.


    Feedback
    --------

    Please help us improve MONYC by sending your feedback to: mfuentesn@nyu.edu
    In case of a problem report please include as many details as possible.

"""

import os
from typing import BinaryIO, Optional, TextIO, Tuple

import librosa
import numpy as np
import csv

from soundata import download_utils
from soundata import jams_utils
from soundata import core
from soundata import annotations
from soundata import io

BIBTEX = """
@inproceedings{fuentes2021monyc,
  title={MONYC: Music of New York City Dataset},
  author={Fuentes, Magdalena and Zhao, Danielle and Lostanlen, Vincent and Cartwright, Mark and Mydlarz, Charlie and Bello, Juan P},
  booktitle={Workshop on Detection and Classification of Acoustic Scenes and Events},
  year={2021},
  series = {DCASE},
}


	
"""
REMOTES = {
    "all": download_utils.RemoteFileMetadata(
        filename="",
        url="",
        checksum="",
        unpack_directories=[""],
    )
}

LICENSE_INFO = "Creative Commons Attribution 4.0 International (CC-BY 4.0)"


class Clip(core.Clip):
    """monyc Clip class

    Args:
        clip_id (str): id of the clip

    Attributes:
        tags (soundata.annotation.Tags): tag (label) of the clip + confidence. In UrbanSound8K every clip has one tag.
        audio_path (str): path to the audio file
        slice_file_name (str): The name of the audio file. The name takes the following format: [fsID]-[classID]-[occurrenceID]-[sliceID].wav.
            Please see the Dataset Info in the soundata documentation for further details.
        freesound_id (str): ID of the freesound.org recording from which this clip was taken.
        freesound_start_time (float): start time in seconds of the clip in the original freesound recording.
        freesound_end_time (float): end time in seconds of the clip in the original freesound recording.
        salience (int): annotator estimate of class sailence in the clip: 1 = foreground, 2 = background.
        fold (int): fold number (1-10) to which this clip is allocated. Use these folds for cross validation.
        class_id (int): integer representation of the class label (0-9). See Dataset Info in the documentation for mapping.
        class_label (str): string class name: air_conditioner, car_horn, children_playing, dog_bark, drilling, engine_idling, gun_shot, jackhammer, siren, street_music.
        clip_id (str): clip id

    """

    def __init__(self, clip_id, data_home, dataset_name, index, metadata):
        super().__init__(clip_id, data_home, dataset_name, index, metadata)

        self.audio_path = self.get_path("audio")

    @property
    def audio(self) -> Optional[Tuple[np.ndarray, float]]:
        """The clip's audio

        Returns:
            * np.ndarray - audio signal
            * float - sample rate

        """
        return load_audio(self.audio_path)

    @property
    def slice_file_name(self):
        return self._clip_metadata.get("slice_file_name")

    @property
    def freesound_id(self):
        return self._clip_metadata.get("freesound_id")

    @property
    def freesound_start_time(self):
        return self._clip_metadata.get("freesound_start_time")

    @property
    def freesound_end_time(self):
        return self._clip_metadata.get("freesound_end_time")

    @property
    def salience(self):
        return self._clip_metadata.get("salience")

    @property
    def fold(self):
        return self._clip_metadata.get("fold")

    @property
    def class_id(self):
        return self._clip_metadata.get("class_id")

    @property
    def class_label(self):
        return self._clip_metadata.get("class_label")

    @property
    def tags(self):
        return annotations.Tags(
            [self._clip_metadata.get("class_label")], "open", np.array([1.0])
        )

    def to_jams(self):
        """Get the clip's data in jams format

        Returns:
            jams.JAMS: the clip's data in jams format

        """
        return jams_utils.jams_converter(
            audio_path=self.audio_path, tags=self.tags, metadata=self._clip_metadata
        )


@io.coerce_to_bytes_io
def load_audio(fhandle: BinaryIO, sr=44100) -> Tuple[np.ndarray, float]:
    """Load a UrbanSound8K audio file.

    Args:
        fhandle (str or file-like): File-like object or path to audio file
        sr (int or None): sample rate for loaded audio, 44100 Hz by default.
            If different from file's sample rate it will be resampled on load.
            Use None to load the file using its original sample rate (sample rate
            varies from file to file).

    Returns:
        * np.ndarray - the mono audio signal
        * float - The sample rate of the audio file

    """
    audio, sr = librosa.load(fhandle, sr=sr, mono=True)
    return audio, sr


@core.docstring_inherit(core.Dataset)
class Dataset(core.Dataset):
    """
    The urbansound8k dataset
    """

    def __init__(self, data_home=None):
        super().__init__(
            data_home,
            name="urbansound8k",
            clip_class=Clip,
            bibtex=BIBTEX,
            remotes=REMOTES,
            license_info=LICENSE_INFO,
        )

    @core.copy_docs(load_audio)
    def load_audio(self, *args, **kwargs):
        return load_audio(*args, **kwargs)

    @core.cached_property
    def _metadata(self):

        metadata_path = os.path.join(self.data_home, "metadata", "UrbanSound8K.csv")

        if not os.path.exists(metadata_path):
            raise FileNotFoundError("Metadata not found. Did you run .download()?")

        with open(metadata_path, "r") as fhandle:
            reader = csv.reader(fhandle, delimiter=",")
            raw_data = []
            for line in reader:
                if line[0] != "slice_file_name":
                    raw_data.append(line)

        metadata_index = {}
        for line in raw_data:
            clip_id = line[0].replace(".wav", "")

            metadata_index[clip_id] = {
                "slice_file_name": line[0],
                "freesound_id": line[1],
                "freesound_start_time": float(line[2]),
                "freesound_end_time": float(line[3]),
                "salience": int(line[4]),
                "fold": int(line[5]),
                "class_id": int(line[6]),
                "class_label": line[7],
            }

        return metadata_index
