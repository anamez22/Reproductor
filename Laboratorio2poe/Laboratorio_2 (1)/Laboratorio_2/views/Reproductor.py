import tkinter as tk
from tkinter import *
from tkinter import ttk
from views.Tooltip import Tooltip
from PIL import Image, ImageTk
import pygame.mixer as mx
from controllers.lista_musica import ListaMusica
from controllers.botones import Botones
from controllers.lista_musica import Tiempo_musica 
from controllers.barras_deslizantes import Barra_progresso
from controllers.volumen import Volumen

class Reproductor():

    def correr_botones(self):
     self.botones = Botones(
        self.ventana, self.btnPlay, self.btnStop, self.btnFormer, self.btnAdvance,
        self.btnNext, self.btnBack, self.lista_musica.nombre_cancion,
        self.lista_musica.duracion_cancion, self.iconoPlay, self.iconoPause,
        self.lista_musica.obtener_ruta_actual, self.tiempo,self.barra.pausar_barra, self.barra.iniciar_barra
    )

    def mostrar_lista_musica(self):
        self.lista_musica = ListaMusica(self.ventana, self.btnOpenF, self.btnFolder)

    def mostrar_tiempo(self):
        self.tiempo_actual_var = tk.StringVar(value="00:00")
        self.duracion_var = tk.StringVar(value="00:00")
        self.tiempo = Tiempo_musica(self.lista_musica, self.tiempo_actual_var, self.duracion_var, self.btnPlay, self.iconoPause,None)
    
    def mostrar_barra_progreso(self):
        self.barra= Barra_progresso(self.barra_progreso,0,self.tiempo_actual_var,self.tiempo)
       
    def mostrar_volumen(self):
        self.volumen = Volumen(self.ventana, self.iconoAudio, self.btnAudio)

    def mostrar_ventana_ayuda(self):
        if hasattr(self, '_help_window') and self._help_window.winfo_exists():
            self.ventanaHelp.lift()
            return
        
        self.ventanaHelp = Toplevel(self.ventana)
        self.ventanaHelp.title("Atajos de teclado")
        self.ventanaHelp.config(width=450, height=450, bg="#EABDEA")
        self.ventanaHelp.protocol("WM_DELETE_WINDOW", self.ventanaHelp.destroy)

        textFrame = Frame(self.ventanaHelp, bd=2, relief="groove")
        textFrame.pack(padx=10, pady=10, fill="both", expand=True)

        self.textoVentana = Text(textFrame, wrap="word", font=("Arial", 10),
                               bg="#f0f0f0", fg="#333333", relief="flat")
        self.textoVentana.pack(side="left", fill="both", expand=True)

        hotkeys_info = """
                    Bienvenido a la ayuda de atajos de teclado:

                    Controles de Reproducción:
                    
                    Espacio / Ctrl + P:  Reproducir / Pausar
                    Ctrl + S:            Detener Canción

                    Navegación de Canciones:
                   
                    Flecha Derecha / Ctrl + N: Siguiente Canción
                    Flecha Izquierda / Ctrl + B: Canción Anterior

                    Control de Tiempo:
                    
                    Flecha Arriba / Ctrl + F:  Avanzar 10 segundos
                    Flecha Abajo / Ctrl + R:   Retroceder 10 segundos"""

     

        self.textoVentana.insert("1.0", hotkeys_info)
        self.textoVentana.config(state="disabled")

    def __init__(self):
        mx.init()

        self.ventana = tk.Tk()
        self.ventana.title("Player music")
        self.ventana.config(width=1000, height=800, bg="#000000")
        self.ventana.resizable(1,1)
        

        self.lienzo = tk.Canvas(self.ventana, bg = "#000000",highlightbackground="#4bf8f0" )
        self.lienzo.place(relx=0.5, rely=0.5, anchor="center", width=950, height=750)
        imagenOriginal = Image.open(r"icons\Adobe Express - file (1).png")
        imagentk = ImageTk.PhotoImage(imagenOriginal)
        image = self.lienzo.create_image(270, 260, image=imagentk) 

        self.iconoPlay = tk.PhotoImage(file=r"icons\icons8-play-40.png")
        self.iconoStop = tk.PhotoImage(file=r"icons\icons8-stop-40.png")
        self.iconoPause = tk.PhotoImage(file=r"icons\icons8-pause-40.png")
        self.iconoFormer = tk.PhotoImage(file=r"icons\icons8-skip-to-start-40.png")
        self.iconoAdvance = tk.PhotoImage(file=r"icons\icons8-end-40.png")
        self.iconoNext = tk.PhotoImage(file=r"icons\icons8-go-to-end-40.png")
        self.iconoBack = tk.PhotoImage(file=r"icons\icons8-go-to-start-40.png")
        self.iconoOpenF = tk.PhotoImage(file=r"icons\icons8-task-40.png")
        self.iconoEcualizador = tk.PhotoImage(file=r"icons\icons8-audio-wave-40.png")
        self.iconoHelp = tk.PhotoImage(file=r"icons\icons8-help-40.png")
        self.iconoAudio= tk.PhotoImage(file=r"icons\icons8-audio-40.png")
        self.iconoFolder= tk.PhotoImage(file=r"icons\icons8-opened-folder-40.png")


        self.btnPlay = tk.Button(self.ventana, image=self.iconoPlay)
        self.btnPlay.place(relx=0.5,rely=0.85,x=5, width=50, height=50)
        self.btnPlay.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnPlay, "Presione para reproducir la canción")

   
        self.btnStop = tk.Button(self.ventana, image=self.iconoStop)
        self.btnStop.place(relx=0.5, rely=0.85, x=-75, width=50, height=50)
        self.btnStop.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnStop, "Presione para detener la reproducción")

        self.btnFormer = tk.Button(self.ventana, image=self.iconoFormer)
        self.btnFormer.place(relx=0.5, rely=0.85, x=-145, width=50, height=50)
        self.btnFormer.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnFormer, "Presione para retroceder la canción")

        self.btnAdvance = tk.Button(self.ventana, image=self.iconoAdvance)
        self.btnAdvance.place(relx=0.5, rely=0.85, x=75, width=50, height=50)
        self.btnAdvance.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnAdvance, "Presione para adelantar la reproducción")

        self.btnBack = tk.Button(self.ventana, image=self.iconoBack)
        self.btnBack.place(relx=0.5, rely=0.85, x=-215, width=50, height=50)
        self.btnBack.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnBack, "Presione para reproducir la canción anterior")

        self.btnNext = tk.Button(self.ventana, image=self.iconoNext)
        self.btnNext.place(relx=0.5, rely=0.85, x=145, width=50, height=50)
        self.btnNext.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnNext, "Presione para reproducir la siguiente canción")


        self.btnOpenF = tk.Button(self.ventana, image=self.iconoOpenF)
        self.btnOpenF.place(relx=0.9, rely=0.05, x=10, width=50, height=50)
        self.btnOpenF.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnOpenF, "Presione para mostrar la lista de canciones")

        self.btnFolder = tk.Button(self.ventana, image=self.iconoFolder)
        self.btnFolder.place(relx=0.8, rely=0.05, x=10, width=50, height=50)
        self.btnFolder.config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnFolder, "Presione para cargar la carpeta de canciones")


        self.btnHelp = tk.Button(self.ventana, image=self.iconoHelp, command=self.mostrar_ventana_ayuda)
        self.btnHelp .place(relx=0.05, rely=0.05, width=50, height=50)
        self.btnHelp .config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnHelp, "Presione para recibir ayuda")

        self.btnAudio = tk.Button(self.ventana, image=self.iconoAudio)
        self.btnAudio .place(relx=0.9, rely=0.5, y=80, x=-10, width=50, height=50)
        self.btnAudio .config(bg="black", activebackground="black", borderwidth=0)
        Tooltip(self.btnAudio, "Presione para subir volumen")

        
        self.barra_progreso=ttk.Scale(self.ventana, from_=0, to=100, orient="horizontal", length=400)
        self.barra_progreso.place(relx=0.5, rely=0.75, anchor="center")

        self.tiempo=None
        self.barra=None

        self.mostrar_lista_musica()
        self.mostrar_tiempo() 
        self.lista_musica.tiempo_musica = self.tiempo 
        self.mostrar_barra_progreso()     
        self.correr_botones() 
        self.mostrar_volumen()
        
        self.barra.tiempo = self.tiempo
        self.tiempo.barra = self.barra
        self.lista_musica.botones = self.botones
        
        
        self.label_tiempo_actual = tk.Label(self.ventana, textvariable=self.tiempo_actual_var, bg="black", fg="white", font=("Helvetica", 12))
        self.label_tiempo_actual.place(relx=0.5, rely=0.8, anchor="e")

        self.label_duracion = tk.Label(self.ventana, textvariable=self.duracion_var, bg="black", fg="white", font=("Helvetica", 12))
        self.label_duracion.place(relx=0.5, rely=0.8, anchor="w")
        


        self.ventana.mainloop()