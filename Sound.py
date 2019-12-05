from threading import Thread
from playsound import playsound


class Sound(Thread):

    def __init__(self, musicpath, stop=False):
        """
        Initialise le chemin de la musique et active le mode daemon pour forcer le lien avec le processus père lors
        de sa mort
         @param musicpath: chemin de la musique
         @param stop: si le doit être ponctuel
        """
        Thread.__init__(self)
        self.daemon = True
        self.stopnext = stop
        self.musicpath = musicpath

    def run(self):
        """
        Boucle infinie qui joue le son
        @return:
        """
        while True:
            playsound(self.musicpath)
            if self.stopnext:
                break
