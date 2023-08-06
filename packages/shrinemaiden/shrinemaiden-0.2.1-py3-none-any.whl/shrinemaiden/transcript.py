import os
import json
import errno
import random
import librosa

from typing import *
from shrinemaiden.transcript_class import *

def create_transcript (
    path: str,
    output: str,
) -> None:
    """
    Creates a transcript file for LibriSpeech dataset

    PARAMETERS
    ----------
    path : str
        The path to the folder containing LibreSpeech files
    output : str
        The path to the output transcript file
    """
    output_file = open(output, 'w');

    # Iterates through each group
    for group in os.listdir(path):
        speaker_path = os.path.join(path, group)

        # Iterates through each speaker in the group
        for speaker in os.listdir(speaker_path):
            audio_root_path = os.path.join(speaker_path, speaker);
            speaker_transcript = os.path.join (
                audio_root_path,
                '{}-{}.trans.txt'.format (group, speaker)
            )

            # Iterate through each line in the speaker's
            # transcript
            for line in open(speaker_transcript):
                line_split = line.strip().split()
                file_id    = line_split[0]
                label      = ' '.join(line_split[1:]).lower()
                audio_file = os.path.join (
                    audio_root_path,
                    file_id
                )
                audio_file = audio_file + '.flac'

                time_series, sampling_rate = librosa.load(audio_file)
                duration = librosa.get_duration(time_series, sampling_rate)

                # Writes the new transcript to the output
                # file
                output_line = json.dumps(
                    {
                        'path'     : audio_file,
                        'duration' : duration,
                        'text'     : label
                    }
                )

                output_file.write (output_line + "\n");

    output_file.close();

def create_train_test_from_transcript(
    transcript_path : str,
    train_ratio : float = 0.8,
    output_train : str = "train.txt",
    output_test : str = "test.txt",
    shuffle : bool = False
) -> None:
    """
    Creates train and test transcripts from the transcript

    PARAMETERS
    ----------
    transcript_path : str
        The path to the transcript file
    train_ratio : float
        The ratio of the training set
    output_train : str
        The path to output the train transcript
    output_test : str
        The path to output the test transcript
    shuffle : bool
        Whether to shuffle the data or not
    """
    if not os.path.exists(transcript_path):
        raise FileNotFoundError (
            errno.ENOENT,
            os.strerror (errno.ENOENT),
            transcript_path
        )

    transcript = open(transcript_path, "r")
    transcript_lines = [line for line in transcript.readlines()]
    transcript.close()

    transcript_amount = len(transcript_lines)

    if shuffle:
        random.shuffle (transcript_lines)

    train_lines = transcript_lines[:int(train_ratio * transcript_amount)]
    test_lines  = transcript_lines[int(train_ratio * transcript_amount):]

    train = open(output_train, "w")
    for line in train_lines:
        train.write(line)
    train.close()

    test = open(output_test, "w")
    for line in test_lines:
        test.write(line)
    test.close()

def read_transcript(transcript_path : str) -> AudioTranscript:
    """
    Reads the transcript and returns relevant information

    PARAMETERS
    ----------
    path : str
        The path to the transcript

    RETURN
    ------
    output_transcript : AudioTranscript
        An object that contains all the path, duration, and
        label of the transcript.
    """

    if not os.path.exists (transcript_path):
        raise FileNotFoundError (
            errno.ENOENT,
            os.strerror (errno.ENOENT),
            transcript_path
        )

    path     = []
    label    = []
    duration = []

    transcript = open(transcript_path, "r")
    for line in transcript.readlines():
        data = json.loads(line)
        path.append (data['path'])
        duration.append (data['duration'])
        label.append (data['text'])

    output_transcript = AudioTranscript(path, duration, label)

    return output_transcript
