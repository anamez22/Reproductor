import tkinter as tk
import pygame.mixer as mx
from tkinter import messagebox as mb
from mutagen.mp3 import MP3


class Botones():
           
    def obtener_duracion_actual(self, ruta):
     try:
        audio = MP3(ruta)
        duracion_segundos = int(audio.info.length)
        minutos = duracion_segundos // 60
        segundos = duracion_segundos % 60
        return f"{minutos:02}:{segundos:02}"
     except:
        return "00:00"

    def PlayPause(self, event=None):
        ruta = self.obtener_ruta_actual()
        if not ruta:
            mb.showerror("Error", "No se ha seleccionado ninguna canción.")
            return
        if not hasattr(self, 'pausa'):
            self.pausa = False  

        if not mx.music.get_busy() and not self.pausa:
            # Si no hay música sonando ni está pausada, reproducir desde cero
            mx.music.stop() 
            mx.music.load(ruta)
            mx.music.play()

            if ruta in self.lista_rutas:
                self.tiempo.reproducir_tiempo_musica()

            self.reproducirCancion()
            self.tiempo.reproducir_tiempo_musica()
            self.iniciar_barra#valery cambio
            self.pausa = False
            self.btnPlay.config(image=self.iconopause)

        elif mx.music.get_busy() and not self.pausa:
            # Si está reproduciendo, pausar
            mx.music.pause()
            self.pausa = True
            self.btnPlay.config(image=self.iconoPlay)
            self.pausar_barra#valery cambio
    
        else:
            # Si está pausada, reanudar
            mx.music.unpause()
            self.pausa = False
            self.btnPlay.config(image=self.iconopause)
            self.iniciar_barra#valery cambio
            self.tiempo.reanudar_tiempo_musica()

        # Habilitar el botón de stop
        self.btnStop.config(state="normal")

    def detener(self, event=None):
        mx.music.stop()
        self.pausa = False
        self.btnPlay.config(image=self.iconoPlay)
        self.btnStop.config(state="disabled")
       
    def avanzar(self, event=None):
        try:
            posicion = mx.music.get_pos() / 1000
            nuevaPosicion = min(posicion + 10)
            mx.music.set_pos(nuevaPosicion)
        except:
            mb.showwarning("Aviso", "No se puede avanzar esta canción.")
            
    def retroceder(self, event=None):
        try:
            posicion = mx.music.get_pos() / 1000
            nuevaPosicion = max(posicion - 10)
            mx.music.set_pos(nuevaPosicion)
        except:
            mb.showwarning("Aviso", "No se puede retroceder esta canción.")

    def siguiente(self, event=None):
        self.tiempoActual = (self.tiempoActual + 1) % len(self.lista_rutas)
        self.reproducirCancion()
       

    def anterior(self, event=None):
        self.tiempoActual = (self.tiempoActual - 1) % len(self.lista_rutas)
        self.reproducirCancion()
     
        
    def reproducirCancion(self, event=None):
        ruta = self.lista_rutas[self.tiempoActual]  
        mx.music.load(ruta) 
        mx.music.play()

       
        duracion = self.obtener_duracion_actual(ruta)
        self.tiempo.duracion_var.set(duracion)
        self.tiempo.tiempo_actual_var.set("00:00")

        nombre_cancion = list(self.lista_musica.keys())[self.tiempoActual]
        self.lblNombreCancion.config(text=f"Canción actual: {nombre_cancion}")
        
        

       
    def __init__(self, ventana, btnPlay, btnStop, btnFormer, btnAdvance, btnNext, btnBack, 
             nombre_cancion, duracion_cancion, iconoPlay, iconopause, obtener_ruta_actual, tiempo, pausar_barra=None, iniciar_barra=None):

        self.ventana = ventana
        self.btnPlay = btnPlay
        self.btnStop = btnStop
        self.btnFormer = btnFormer
        self.btnAdvance = btnAdvance
        self.btnNext = btnNext
        self.btnBack = btnBack
        self.nombre_cancion = nombre_cancion
        self.duracion_cancion = duracion_cancion
        self.iconoPlay = iconoPlay
        self.iconopause = iconopause
        self.obtener_ruta_actual = obtener_ruta_actual
        self.tiempoActual = 0
        self.tiempo_pausa=0
        

        self.tiempo = tiempo
        self.pausa = False

        self.pausar_barra = pausar_barra 
        self.iniciar_barra = iniciar_barra 

        self.lblNombreCancion = tk.Label(self.ventana, text="Canción actual: ", font=("Arial", 12), fg="#d260eb", bg="#000000")
        self.lblNombreCancion.place(relx=0.5, rely=0.7, anchor="center")

        self.btnPlay.bind("<Button-1>", self.PlayPause)
        self.btnStop.bind("<Button-1>",self.detener)
        self.btnAdvance.bind("<Button-1>", self.avanzar)
        self.btnFormer.bind("<Button-1>", self.retroceder)
        self.btnNext.bind("<Button-1>", self.siguiente)
        self.btnBack.bind("<Button-1>", self.anterior)

        self.ventana.bind("<space>", self.PlayPause)         
        self.ventana.bind("<Right>", self.siguiente)         
        self.ventana.bind("<Left>", self.anterior)            
        self.ventana.bind("<Up>", self.avanzar)               
        self.ventana.bind("<Down>", self.retroceder)          
        self.ventana.bind("<Control-s>", self.detener)

        self.ventana.bind("<Control-p>", self.PlayPause)      
        self.ventana.bind("<Control-n>", self.siguiente)      
        self.ventana.bind("<Control-b>", self.anterior) 
       
    
        self.lista_musica = {
            "Amy Winehouse - Rehab": r"musica\Amy Winehouse - Rehab.mp3",
            "Arctic Monkeys - Why'd You Only Call Me When You're High_ español": r"musica\Arctic Monkeys - Why'd You Only Call Me When You're High_ español.mp3",
            "Hozier - Too Sweet (Official Video)": r"musica\Hozier - Too Sweet (Official Video).mp3",
            "Maroon 5 - Maps (Lyric Video)": r"musica\Maroon 5 - Maps (Lyric Video).mp3",
            "Soda Stereo - Entre Caníbales (Letra)": r"musica\Soda Stereo - Entre Caníbales (Letra).mp3"
        }
        self.lista_rutas = list(self.lista_musica.values())

    




    
