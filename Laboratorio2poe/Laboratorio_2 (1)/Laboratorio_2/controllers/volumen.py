import tkinter as tk
import pygame.mixer as mx
class Volumen:

    def __init__(self, ventana, iconoAudio, btnVolumen=None):
        self.ventana = ventana
        self.btnVolumen = btnVolumen
        self.iconoAudio = iconoAudio
        self.estado=False
        self.volumen_elegido = None

        self.volumen_barra= tk.Scale(self.ventana, from_=0, to=100, orient="horizontal", length=200, label="Volumen")
        self.btnVolumen.bind("<Button-1>", self.alternar)
        self.volumen_barra.bind("<ButtonRelease-1>", self.obtener_volumen)

    def mostrar_volumen(self):
        self.volumen_barra.place(x=760, y=400, width=200, height=70)
        self.volumen_barra.set(50)

    def ocultar_volumen(self):
        self.volumen_barra.place_forget()

    def alternar(self,event):
        if self.estado==False:
            self.mostrar_volumen()
            self.estado=True
        else:
            self.ocultar_volumen()
            self.estado=False
    
    def obtener_volumen(self,event):
        self.volumen_elegido= self.volumen_barra.get()
        volumen_normalizado = self.volumen_elegido / 100
        mx.music.set_volume(volumen_normalizado)

        
        
        
        