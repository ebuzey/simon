# test_sound.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
import sys
import os

def main():
    app = QApplication(sys.argv)
    sound = QSoundEffect()
    sounds_path = os.path.join(os.path.dirname(__file__), 'sounds')
    sound_file = os.path.join(sounds_path, 'up.wav')
    if os.path.exists(sound_file):
        sound.setSource(QUrl.fromLocalFile(sound_file))
        sound.setVolume(0.5)  # Volumen entre 0.0 y 1.0
        sound.play()
        print(f"Reproduciendo sonido: {sound_file}")
    else:
        print(f"Archivo de sonido no encontrado: {sound_file}")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
