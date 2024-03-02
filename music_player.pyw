import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame
from mutagen.mp3 import MP3
import time
import random

class MusicPlayer:
    def __init__(self, root, startup_volume=10):
        self.root = root
        self.root.title("mufi's shitbox")
        self.root.geometry("365x175")

        self.playlist = []
        self.current_track = 0
        self.music_playing = False  # Set default state to paused
        self.last_position = 0
        self.shuffle_enabled = False
        self.loop_enabled = False  # Initialize loop status
        
        # Initialize update IDs for timer and progress bar
        self.song_timer_update_id = None
        self.progress_bar_update_id = None

        self.create_ui()
        pygame.init()
        pygame.mixer.init()  # Initialize mixer
        pygame.mixer.music.set_volume(startup_volume / 100)

    def create_ui(self):
        # Create UI elements
        self.playlist_label = tk.Label(self.root, text="Playlist:")
        self.playlist_label.place(x=10, y=10)

        self.playlist_name_label = tk.Label(self.root, text="", width=25, anchor="w")
        self.playlist_name_label.place(x=60, y=10)

        self.track_label = tk.Label(self.root, text="Now Playing:")
        self.track_label.place(x=10, y=35)

        self.track_name_label = tk.Label(self.root, text="", width=25, anchor="w")
        self.track_name_label.place(x=90, y=35)

        self.back_button = tk.Button(self.root, text="Back", command=self.rewind)
        self.back_button.place(x=60, y=70)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_stop)
        self.play_button.place(x=110, y=70)

        self.skip_button = tk.Button(self.root, text="Skip", command=self.skip)
        self.skip_button.place(x=160, y=70)

        self.shuffle_checkbox = ttk.Checkbutton(self.root, text="Shuffle", command=self.toggle_shuffle, state="selected")
        self.shuffle_checkbox.place(x=210, y=65)
        
        self.loop_checkbox = ttk.Checkbutton(self.root, text="Loop", command=self.toggle_loop)
        self.loop_checkbox.place(x=210, y=85)

        self.playlist_button = tk.Button(self.root, text="Select Playlist", command=self.load_playlist)
        self.playlist_button.place(x=275, y=10)

        self.volume_scale = ttk.Scale(self.root, from_=10, to=0, command=self.set_volume, orient=tk.VERTICAL)
        self.volume_scale.place(x=305, y=50)
        self.volume_scale.set(10)  # Set default volume to 100%

        # Song timer
        self.song_timer_label = tk.Label(self.root, text="00:00 / 00:00")
        self.song_timer_label.place(x=115, y=110)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=250, mode='determinate')
        self.progress_bar.place(x=25, y=130)

        # Set up event to handle end of music playback
        self.root.after(1000, self.check_music_end)

    def load_playlist(self):
        # Load playlist from user-selected directory
        directory = filedialog.askdirectory()
        if directory:
            pygame.mixer.music.stop()
            self.playlist = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.mp3')]
            self.current_track = 0
            self.update_track_label()
            self.update_playlist_label(directory)

    def update_playlist_label(self, directory):
        if directory:
            playlist_name = os.path.basename(directory)
            if len(playlist_name) > 16:
                playlist_name = playlist_name[:16] + "..."
            self.playlist_name_label.config(text=playlist_name)

    def update_track_label(self):
        if self.playlist:
            track_path = self.playlist[self.current_track]
            track_name = os.path.basename(os.path.splitext(track_path)[0])
            if len(track_name) > 26:
                track_name = track_name[:25] + "..."
            self.track_name_label.config(text=track_name)
    
    def play_stop(self):
        if self.music_playing:
            pygame.mixer.music.pause()
            self.last_position = pygame.mixer.music.get_pos() // 1000  # Store current position in seconds
            self.play_button.config(text="Play")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.load(self.playlist[self.current_track])
                pygame.mixer.music.play(start=self.last_position)  # Resume from stored position
            self.play_button.config(text="Stop")

        # Always schedule timer and progress bar updates
        self.update_song_timer()
        self.update_progress_bar()

        self.music_playing = not self.music_playing










    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled

    def skip(self):
        if self.playlist:
            if self.shuffle_enabled:
                next_track = self.current_track
                while next_track == self.current_track:
                    next_track = random.randint(0, len(self.playlist) - 1)
                self.current_track = next_track
            else:
                self.current_track = (self.current_track + 1) % len(self.playlist)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.update_track_label()
            self.play_button.config(text="Stop")  # Update button text
            self.music_playing = True
    
    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled

    def rewind(self):
        if self.playlist:

            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.update_track_label()
            self.play_button.config(text="Stop")  # Update button text
            self.music_playing = True

    def check_music_end(self):
        if self.playlist:
            self.update_song_timer()
            self.update_progress_bar()
            if self.music_playing and not pygame.mixer.music.get_busy():
                if self.loop_enabled:
                    # If loop is enabled, play the current track again
                    pygame.mixer.music.load(self.playlist[self.current_track])
                    pygame.mixer.music.play()
                else:
                    # If loop is not enabled, skip to the next track
                    self.skip()
        self.root.after(1000, self.check_music_end)

    def set_volume(self, value):
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            volume = float(value) / 100  # Scale the value correctly
            pygame.mixer.music.set_volume(volume)


    def update_song_timer(self):
        if self.playlist and self.music_playing:
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos() / 1000
                total_time = MP3(self.playlist[self.current_track]).info.length
                current_time_str = time.strftime("%M:%S", time.gmtime(current_time))
                total_time_str = time.strftime("%M:%S", time.gmtime(total_time))
                self.song_timer_label.config(text=f"{current_time_str} / {total_time_str}")

    def update_progress_bar(self):
        if self.playlist and self.music_playing:
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos() / 1000
                total_time = MP3(self.playlist[self.current_track]).info.length
                progress = (current_time / total_time) * 100
                self.progress_bar["value"] = progress


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Prevent resizing in both directions
    music_player = MusicPlayer(root)
    root.mainloop()
