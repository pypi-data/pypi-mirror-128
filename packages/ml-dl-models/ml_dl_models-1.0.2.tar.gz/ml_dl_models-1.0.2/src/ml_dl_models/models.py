import requests
import pickle
import json

class MelodyGenerator:
    url = 'https://ml-dl-models.herokuapp.com/api/melodygenerator/'

    def generate_melody(self, data, path='melody.mp3'):
        """
        This is Function creates melody in the given path. 
        If path is not specified it create melody with name melody.mp3 in the directory where the python file is executed.
        Args:
            data (dict): It should dictionary with keys = ['keys','default'] where 'keys' is assigned with the notes of music 
            and default is assigned Boolean Value which is True if octave number is not mentioned in notes provided in keys 
            else assigned False. 

            path = path to save melody, default value = 'melody.mp3'.
            
        """
        json_loaded = requests.post(url=self.url, data = data).json()
        byte = json_loaded.encode(encoding = 'latin1')
        stream = pickle.loads(byte)
        stream.write('midi',path)

    def get_cached_notes(self):
        """
        This function return list of cached notes.

        return:
            cached_data (list): list of cached notes.
        """
        cached_data = requests.get(url=self.url).json()
        return cached_data
