# sound.py

import wave
import math
import struct
import os

def generate_tone(filename, duration=0.5, freq=440.0, volume=0.5, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as wav_file:
        n_channels = 1
        sampwidth = 2
        framerate = sample_rate
        n_frames = n_samples
        comptype = "NONE"
        compname = "not compressed"
        wav_file.setparams((n_channels, sampwidth, framerate, n_frames, comptype, compname))
        
        for i in range(n_samples):
            sample = volume * math.sin(2 * math.pi * freq * i / sample_rate)
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

def main():
    # Definir la carpeta de sonidos
    sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    
    # Crear la carpeta si no existe
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
        print(f"Directorio creado: {sounds_dir}")
    else:
        print(f"Directorio existente: {sounds_dir}")
    
    # Definir los tonos para cada tecla
    tones = {
        'up.wav': 523.25,        # C5
        'left.wav': 329.63,      # E4
        'right.wav': 659.25,     # E5
        'down.wav': 392.00,      # G4
        'start.wav': 880.00,     # A5 (Opcional)
        'game_over.wav': 196.00  # G3 (Opcional)
    }
    
    # Generar los tonos
    for filename, freq in tones.items():
        filepath = os.path.join(sounds_dir, filename)
        generate_tone(filepath, freq=freq)
        print(f"Sonido generado: {filepath}")

if __name__ == "__main__":
    main()
