import tkinter as tk
import chord_dicts
import audio
import os
import pygame
from pathlib import Path

def create_radio_btn(frame, my_text, var, value, row, col, width=4):
    button = tk.Radiobutton(
        frame, 
        text=my_text, 
        variable=var,
        value=value,
        width=width, 
        anchor='w'
        )
    return button

class ChordSearch():
    def __init__(self, window, color) -> None:

        self.window = window
        self.btn_color = '#1a1a1a'
        self.lbl_color = '#000000'
        self.txt_color = '#ffffff'

        pygame.mixer.init()
        folder = os.getcwd()
        folder = os.path.join(folder, "Rhodes Notes")
        clip_folder = Path(folder)
        self.file = f'{clip_folder}\\temp.wav'

        self.frame = tk.Frame(window, bg=color)
        self.title = tk.Label(
            self.frame, 
            text='Chord Search', 
            bg=color,
            fg='#ffffff'
            )
        self.title.grid(row=0, column=4, sticky='ew')

        self.frame.grid(row=0, column=1, sticky='nsew')
        self.frame.grid_columnconfigure(
            (1,2,3,4,5,6,7), 
            weight=1, 
            uniform='equal'
            )

        self.text_var = tk.StringVar()
        self.text_var.set("Csus2 b5")

        self.chord_label = tk.Label(self.frame, textvariable=self.text_var, bg=self.btn_color, fg=self.txt_color).grid(
            row=15, 
            column=5, 
            sticky='ew'
            )

        tk.Label(self.frame, text='Root', bg=self.lbl_color, fg=self.txt_color).grid(row=1, column=1, sticky='ew')
        tk.Label(self.frame, text='3rd', bg=self.lbl_color, fg=self.txt_color).grid(row=1, column=2, sticky='ew')
        tk.Label(self.frame, text='5th', bg=self.lbl_color, fg=self.txt_color).grid(row=1, column=3, sticky='ew')
        tk.Label(self.frame, text='7th', bg=self.lbl_color, fg=self.txt_color).grid(row=1, column=4, sticky='ew')
        tk.Label(self.frame, text='9th', bg=self.lbl_color, fg=self.txt_color).grid(row=1, column=5, sticky='ew')
        tk.Label(self.frame, text='11th', bg=self.lbl_color, fg=self.txt_color).grid(row=1, column=6, sticky='ew')
        tk.Label(self.frame, text='13th', bg=self.lbl_color, fg=self.txt_color).grid(row=1, column=7, sticky='ew')

        self.root_var = tk.IntVar()
        self.third_var = tk.IntVar()
        self.fifth_var = tk.IntVar()
        self.seventh_var = tk.IntVar()
        self.ninth_var = tk.IntVar()
        self.eleventh_var = tk.IntVar()
        self.thirteenth_var = tk.IntVar()

        self.root_var.set(0)
        self.third_var.set(1)
        self.fifth_var.set(1)
        self.seventh_var.set(0)
        self.ninth_var.set(0)
        self.eleventh_var.set(0)
        self.thirteenth_var.set(0)

        self.vars=[
            self.root_var, 
            self.third_var, 
            self.fifth_var,
            self.seventh_var,
            self.ninth_var,
            self.eleventh_var,
            self.thirteenth_var
            ]

        self.cardinalities = [12, 4, 3, 3, 4, 3, 3]
        self.btns=[
            [0,1,2,3,4,5,6,7,8,9,10,11],
            [0,1,2,3],
            [0,1,2],
            [0,1,2],
            [0,1,2,3],
            [0,1,2],
            [0,1,2]
            ]

        for i, var in enumerate(self.vars):
            for j in range(self.cardinalities[i]):
                if i == 1 or i == 2:
                    button = tk.Radiobutton(
                        self.frame,
                        text=chord_dicts.chord_array_dict[i][j],
                        variable=var,
                        value=j+1,
                        width=4,
                        bg=color,
                        fg=self.txt_color,
                        activebackground=self.txt_color,
                        activeforeground=self.txt_color,
                        selectcolor=self.btn_color,
                        anchor='w'
                        )

                else:
                    button = tk.Radiobutton(
                        self.frame,
                        text=chord_dicts.chord_array_dict[i][j],
                        variable=var,
                        value=j,
                        width=4,
                        bg=color,
                        fg=self.txt_color,
                        activebackground=self.txt_color,
                        activeforeground=self.txt_color,
                        selectcolor=self.btn_color,
                        anchor='w'
                        )
                
                self.btns[i][j]=button

        for i, btn_group in enumerate(self.btns):
            for j, btn in enumerate(btn_group):
                btn.grid(row=j+2, column=i+1, sticky='ew')

        self.play_chord_btn = tk.Button(
            self.frame, 
            text='Play Chord', 
            bg=self.btn_color,
            fg=self.txt_color,
            command=lambda:self.play_chord_cmd(self.file),
            anchor='w'
            )
        self.play_chord_btn.grid(row=15, column=7, sticky='ew')

        self.correct_chord_btn = tk.Button(
            self.frame,
            text='Correct Chord',
            bg=self.btn_color,
            fg=self.txt_color,
            command = lambda:self.chord_correction(),
            anchor = 'w'
            )
        self.correct_chord_btn.grid(row=15, column=6, sticky='ew')

    def chord_correction(self):
        self.chord=[var.get() for var in self.vars]

        self.text_var.set(audio.chord_name(self.chord))

        #====chord modification

        # sus 2 and natural 9 -> set 9 to 0
        if self.chord[1] == 1 and self.chord[4] == 2:
            self.chord[4] = 0
            self.ninth_var.set(0)

        # sus 2 and sharp 9 -> set third to minor (2), 9 to natural (2)
        if self.chord[1] == 1 and self.chord[4] == 3:
            self.chord[1] = 2
            self.chord[4] = 2

            self.third_var.set(2)
            self.ninth_var.set(2)

        # minor 3rd and sharp 9 -> set 9 to 0
        if self.chord[1] == 2 and self.chord[4] == 3:
            self.chord[4] = 0

            self.ninth_var.set(0)

        # sus 4 and natural 11 -> set 11 to 0
        if self.chord[1] == 4 and self.chord[5] == 1:
            self.chord[5] = 0

            self.eleventh_var.set(0)

        # sus 4 and sharp 9 and no 11 -> set third to minor (2), 9 to 0, 11 to natural
        if self.chord[1] == 4 and self.chord[4] == 3 and self.chord[5] == 0:
            self.chord[1] = 2
            self.chord[4] = 0
            self.chord[5] = 1

            self.third_var.set(2)
            self.ninth_var.set(0)
            self.eleventh_var.set(1)


        # sus 4 and natural 9 and no 11 -> set third to sus 2 (1), 9 to 0, 11 to natural
        if self.chord[1] == 4 and self.chord[4] == 2 and self.chord[5] == 0:
            self.chord[1] = 1
            self.chord[4] = 0
            self.chord[5] = 1

            self.third_var.set(1)
            self.ninth_var.set(0)
            self.eleventh_var.set(1)

        # flat 5 and sharp 11 -> set 11 to 0
        if self.chord[2] == 1 and self.chord[5] == 2:
            self.chord[5] = 0

            self.eleventh_var.set(0)

        # sharp 5 and flat 13 -> set 13 to 0
        if self.chord[2] == 3 and self.chord[6] == 1:
            self.chord[6] = 0

            self.thirteenth_var.set(0)

        # sharp 5 and sharp 11 and no 13 -> set 5 to flat (1), 13 to flat (1)
        if self.chord[2] == 3 and self.chord[5] == 2 and self.chord[6] == 0:
            self.chord[2] = 1
            self.chord[6] = 1

            self.fifth_var.set(1)
            self.thirteenth_var.set(1)

    def play_chord_cmd(self, filename):

        self.chord_correction()
        self.chord=[var.get() for var in self.vars]     

        file_exists = os.path.exists(filename)
        if file_exists:
            pygame.mixer.music.unload()
            os.remove(filename)

        segment = audio.play_chord_progression2([self.chord])
        file = audio.file_from_audio_segment(segment, 'temp.wav')
        self.play_sound(file)

    def play_sound(self, filename):
        with open(filename) as f:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            # pygame.mixer.music.get_endevent()
            # pygame.event.wait()
        
