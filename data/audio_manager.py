import os
import wave
import struct
import math
import pygame

click_sound = None

def generate_assets():
    os.makedirs("assets/audio", exist_ok=True)
    
    
    click_path = "assets/audio/click.wav"
    if not os.path.exists(click_path):
        sample_rate = 22050
        duration = 0.08
        frequency = 1200.0
        
        with wave.open(click_path, 'w') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            
            num_samples = int(duration * sample_rate)
            for i in range(num_samples):
                decay = (num_samples - i) / num_samples
                val = int(12000 * math.sin(2 * math.pi * frequency * i / sample_rate) * decay)
                data = struct.pack('<h', val)
                w.writeframesraw(data)
                
 
    music_path = "assets/audio/music.wav"
    if not os.path.exists(music_path):
        sample_rate = 22050
        notes = [261.63, 329.63, 392.00, 493.88, 523.25, 493.88, 392.00, 329.63]
        note_duration = 0.5
        
        with wave.open(music_path, 'w') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            
           
            for _ in range(4):
                for freq in notes:
                    num_samples = int(note_duration * sample_rate)
                    for i in range(num_samples):
                        decay = (num_samples - i) / num_samples
                        val = int(6000 * math.sin(2 * math.pi * freq * i / sample_rate) * decay)
                        data = struct.pack('<h', val)
                        w.writeframesraw(data)

def init(game_data):
    global click_sound
    
    
    generate_assets()
    
  
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        
 
    if os.path.exists("assets/audio/click.wav"):
        click_sound = pygame.mixer.Sound("assets/audio/click.wav")

    if os.path.exists("assets/audio/music.wav"):
        pygame.mixer.music.load("assets/audio/music.wav")
        pygame.mixer.music.play(-1) 
        
    update_music_state(game_data)

def play_click(game_data):
    global click_sound
    if click_sound and game_data.get("sound_enabled", True):
        click_sound.play()

def update_music_state(game_data):
    if not pygame.mixer.get_init():
        return
        
    if game_data.get("music_enabled", True):
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
