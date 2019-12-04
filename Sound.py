import random

import sys

from threading import Thread

import time

from playsound import playsound


class Sound(Thread):


    """Thread chargé simplement d'afficher une lettre dans la console."""


    def __init__(self,musicpath,stop=False ):

        Thread.__init__(self)
        self.stopnext = stop
        self.musicpath = musicpath


    def run(self):

        """Code à exécuter pendant l'exécution du thread."""
        while True:
            playsound(self.musicpath)
            if self.stopnext:
                break

    def stop(self):
        self.stopnext = True
           

        
