import os
import json
import errno

from typing import *

class AudioTranscript:
    _path     : List[str] = []
    _duration : List[str] = []
    _label    : List[str] = []

    def __init__(
        self,
        path     : List[str],
        duration : List[str],
        label    : List[str]
    ):
        """
        The default constructor

        PARAMETERS
        ----------
        path : List[str]
            The list containing all the path of the transcript
        duration : List[str]
            The list containing all the duration of the transcript
        label : List[str]
            The list containing all the label of the transcript
        """

        self._path     = path
        self._duration = duration
        self._label    = label

    def get_path(self) -> List[str]:
        """
        Returns all the path of the transcript

        RETURN
        ------
        self._path : List[str]
            The list containing all the path of the transcript
        """
        return self._path

    def get_duration(self) -> List[str]:
        """
        Returns all the duration of the transcript

        RETURN
        ------
        self._duration : List[str]
            The list containing all the duration of the transcript
        """
        return self._duration

    def get_label(self) -> List[str]:
        """
        Returns all the label of the transcript

        RETURN
        ------
        self._label : List[str]
            The list containing all the label of the transcript
        """
        return self._label

class Transcript:
    _transcript : List[str] = []

    def __init__(
        self,
        path : str
    ):
        """
        The default constructor

        PARAMETERS
        ----------
        path : str
            The path of the transcript
        """
        if not os.path.exists (path):
            raise FileNotFoundError (
                errno.ENOENT,
                os.strerror (errno.ENOENT),
                path
            )

        path_file = open (path)
        _transcript = [line for line in path_file.readlines()]
        path_file.close()

    def to_audio_transcript(self) -> AudioTranscript:
        """
        Converts this object into an AudioTranscript object
        """
        path     : List[str] = []
        label    : List[str] = []
        duration : List[str] = []

        for line in self._transcript:
            data = json.loads(line)
            path.append (data['path'])
            label.append (data['label'])
            duration.append (data['duration'])

        return AudioTranscript(path, duration, label)

if __name__ == "__main__":
    print ("F")
