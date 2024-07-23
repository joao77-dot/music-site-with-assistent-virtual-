import tkinter as tk
from tkinter import ttk, filedialog
import pygame
import os
import speech_recognition as sr
import threading
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Caminho para o arquivo de música
rock_mp3_path = r"C:\Users\joaoz\Desktop\music\songs\rock.mp3"  # Atualizado para .mp3

# Funções para controle de música
def load_music():
    file_paths = filedialog.askopenfilenames(filetypes=[("Music Files", "*.mp3")])
    if file_paths:
        for file_path in file_paths:
            playlist.append(file_path)
            playlist_box.insert(tk.END, os.path.basename(file_path))

def play_music():
    if playlist:
        pygame.mixer.music.load(playlist[playlist_box.curselection()[0]])
        pygame.mixer.music.play()
        current_song.set(os.path.basename(playlist[playlist_box.curselection()[0]]))

def pause_music():
    pygame.mixer.music.pause()

def stop_music():
    pygame.mixer.music.stop()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def recommend_music():
    if not playlist:
        return
    
    # Simulando preferências do usuário
    user_preferences = np.random.rand(10, 5)  # 10 músicas, 5 características cada
    current_song_features = user_preferences[playlist_box.curselection()[0]].reshape(1, -1)

    # Treinando o modelo Nearest Neighbors
    knn = NearestNeighbors(n_neighbors=2)
    knn.fit(user_preferences)

    # Encontrando a música mais próxima
    distances, indices = knn.kneighbors(current_song_features)
    recommended_index = indices[0][1]  # Segunda música mais próxima (a primeira é a música atual)

    recommended_song = os.path.basename(playlist[recommended_index])
    recommended_song_label.set(f"Recommended: {recommended_song}")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando o ruído...")
        recognizer.adjust_for_ambient_noise(source)
        print("Diga um comando...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Você disse: {command}")
            process_command(command)
        except sr.UnknownValueError:
            print("Não consegui entender o comando.")
        except sr.RequestError as e:
            print(f"Erro ao se conectar ao serviço de reconhecimento de voz: {e}")

def process_command(command):
    print(f"Processando o comando: {command}")
    if "black and black" in command:
        if os.path.exists(rock_mp3_path):
            pygame.mixer.music.load(rock_mp3_path)
            pygame.mixer.music.play()
            current_song.set("Tocando: Rock.mp3")
        else:
            print("O arquivo de música não foi encontrado.")
    else:
        print("Comando não reconhecido.")

def on_speak_button_click():
    print("Iniciando reconhecimento de voz...")
    threading.Thread(target=recognize_speech).start()

# Configuração inicial do pygame mixer
pygame.mixer.init()

# Configuração da interface Tkinter com tema
root = tk.Tk()
root.title("Synapse Music Player")
root.geometry("400x600")
root.configure(bg="#2E2E2E")

# Estilo do aplicativo
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Helvetica", 12), background="#4E4E4E", foreground="white", padding=10)
style.map("TButton", background=[('active', '#3A3A3A')])
style.configure("TLabel", font=("Helvetica", 12), background="#2E2E2E", foreground="#FFFFFF")
style.configure("TScale", background="#2E2E2E", foreground="#1DB954", troughcolor="#535353")

# Variáveis para a música atual e recomendada
current_song = tk.StringVar()
current_song.set("No song loaded")
recommended_song_label = tk.StringVar()
recommended_song_label.set("Recommended: None")

# Playlist
playlist = []

# Criação dos widgets
frame_controls = ttk.Frame(root, style="TFrame")
frame_controls.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

load_button = ttk.Button(frame_controls, text="Load", command=load_music, style="TButton")
load_button.grid(row=0, column=0, padx=5)

play_button = ttk.Button(frame_controls, text="Play", command=play_music, style="TButton")
play_button.grid(row=0, column=1, padx=5)

pause_button = ttk.Button(frame_controls, text="Pause", command=pause_music, style="TButton")
pause_button.grid(row=0, column=2, padx=5)

stop_button = ttk.Button(frame_controls, text="Stop", command=stop_music, style="TButton")
stop_button.grid(row=0, column=3, padx=5)

recommend_button = ttk.Button(frame_controls, text="Recommend", command=recommend_music, style="TButton")
recommend_button.grid(row=0, column=4, padx=5)

speak_button = ttk.Button(frame_controls, text="Falar", command=on_speak_button_click, style="TButton")
speak_button.grid(row=0, column=5, padx=5)

volume_label = ttk.Label(frame_controls, text="Volume", style="TLabel")
volume_label.grid(row=1, column=0, padx=5)

volume_slider = ttk.Scale(frame_controls, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, style="TScale")
volume_slider.set(50)
volume_slider.grid(row=1, column=1, columnspan=4, padx=5, pady=10)

song_label = ttk.Label(root, textvariable=current_song, style="TLabel")
song_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

recommended_label = ttk.Label(root, textvariable=recommended_song_label, style="TLabel")
recommended_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

playlist_box = tk.Listbox(root, selectmode=tk.SINGLE, height=10, bg="#1E1E1E", fg="#FFFFFF", font=("Helvetica", 10), bd=0, highlightthickness=0, relief='flat')
playlist_box.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=350, height=250)

# Inicializa a interface
root.mainloop()
