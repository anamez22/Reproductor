import tkinter as tk
import time
import pygame
import pygame.mixer as mx
import threading
import os
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3

class ListaMusica():

    def abrirDialogoCarpeta(self,event=None):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.cargarCancionesDesdeCarpeta(carpeta)
   

    def cargarCancionesDesdeCarpeta(self, rutaCarpeta):
        try:
            archivos = os.listdir(rutaCarpeta)
            extensionesValidas = ('.mp3', '.wav', '.ogg')
            cancionesEncontradas = [os.path.join(rutaCarpeta, f) for f in archivos if f.lower().endswith(extensionesValidas)]

            if cancionesEncontradas:
                self.lista_musica.clear()
                self.lista_duraciones.clear()

                for ruta_completa in cancionesEncontradas:
                    nombre = os.path.basename(ruta_completa)
                    self.lista_musica[nombre] = ruta_completa

                
                    try:
                        if ruta_completa.lower().endswith(".mp3"):
                            audio = MP3(ruta_completa)
                            duracion_seg = int(audio.info.length)
                            minutos = duracion_seg // 60
                            segundos = duracion_seg % 60
                            self.lista_duraciones[nombre] = f"{minutos:02}:{segundos:02}"
                        else:
                            self.lista_duraciones[nombre] = "00:00"
                    except:
                        self.lista_duraciones[nombre] = "00:00"

            
                if hasattr(self, "lista_musica_listbox"):
                    self.lista_musica_listbox.delete(0, tk.END)
                    for nombre in self.lista_musica:
                        self.lista_musica_listbox.insert(tk.END, nombre)

                
                self.nombre_cancion = list(self.lista_musica.keys())[0]
                self.ruta = self.lista_musica[self.nombre_cancion]
                self.duracion_cancion = self.lista_duraciones[self.nombre_cancion]

                if hasattr(self, "botones"):
                    self.botones.lblNombreCancion.config(text=f"Canción actual: {self.nombre_cancion}")
            
            else:
                messagebox.showinfo("Vacío", "No se encontraron archivos de música válidos en la carpeta seleccionada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar canciones: {str(e)}")
        self.btnFolder.bind("<Button-1>", self.cargarCancionesDesdeCarpeta)


    def obtener_ruta_actual(self):
        return self.ruta

    def intercambiar_lista_musica(self, event):
        if self.bandera==False:
            self.mostrar_lista_musica()
            self.bandera = True
        else:
            self.ocultar_lista_musica()
            self.bandera = False

    def ocultar_lista_musica(self):
       self.lista_musica_frame.destroy()

    def mostrar_lista_musica(self):
        self.lista_musica_frame = tk.Frame(self.ventana, bg="#FFFFFF")
        self.lista_musica_frame.place(x=500, y=90, width=450, height=150)

        self.lista_musica_label = tk.Label(self.lista_musica_frame, text="Lista de Música", bg="#FFFFFF", fg="#000000")
        self.lista_musica_label.place(x=225, y=10, anchor="n")

        self.lista_musica_listbox = tk.Listbox(self.lista_musica_frame, bg="#FFFFFF", fg="#000000", selectbackground="#7ea7ff")

        for cancion in self.lista_musica:
            self.lista_musica_listbox.insert(tk.END, cancion)

        self.lista_musica_listbox.place(x=2, y=50, width=450, height=150)

        self.lista_musica_listbox.bind("<<ListboxSelect>>", self.seleccionar_cancion)


    def seleccionar_cancion(self, event):
        seleccion = self.lista_musica_listbox.curselection()
        if seleccion:
            cancion_seleccionada = self.lista_musica_listbox.get(seleccion)
            self.ruta = self.lista_musica[cancion_seleccionada]
            self.nombre_cancion = cancion_seleccionada
            self.duracion_cancion = self.lista_duraciones[cancion_seleccionada]

            if hasattr(self, "botones"):
                self.botones.lblNombreCancion.config(text=f"Canción actual: {cancion_seleccionada}")

            
            duracion_str = self.duracion_cancion 

            if duracion_str and ":" in duracion_str:
                minutos, segundos = map(int, duracion_str.split(":"))
                duracion_segundos = minutos * 60 + segundos
            else:
                duracion_segundos = 0
          
            if hasattr(self, 'tiempo_musica') and hasattr(self.tiempo_musica, 'barra') and self.tiempo_musica.barra:
                self.tiempo_musica.barra.duracion_segundos = duracion_segundos

            print(f"Canción seleccionada: {cancion_seleccionada} - Ruta: {self.ruta}")
            self.tiempo_musica.reproducir_tiempo_musica()



         
    def __init__(self, ventana,btnOpenF, btnFolder):
        self.ventana = ventana
        self.botones = None

        self.lista_musica = {
            "Amy Winehouse - Rehab": r"musica\Amy Winehouse - Rehab.mp3",
            "Arctic Monkeys - Why'd You Only Call Me When You're High_ español": r"musica\Arctic Monkeys - Why'd You Only Call Me When You're High_ español.mp3" ,
            "Hozier - Too Sweet (Official Video)": r"musica\Hozier - Too Sweet (Official Video).mp3",
            "Maroon 5 - Maps (Lyric Video)": r"musica\Maroon 5 - Maps (Lyric Video).mp3",
            "Soda Stereo - Entre Caníbales (Letra)": r"musica\Soda Stereo - Entre Caníbales (Letra).mp3",
        }

        self.lista_duraciones = {
            "Amy Winehouse - Rehab": "03:33",
            "Arctic Monkeys - Why'd You Only Call Me When You're High_ español": "02:44",
            "Hozier - Too Sweet (Official Video)": "04:08",
            "Maroon 5 - Maps (Lyric Video)": "03:09",
            "Soda Stereo - Entre Caníbales (Letra)": "04:07",
        }
            
        self.btnOpenF = btnOpenF
        self.duracion_segundos = 0
        self.bandera=False
        self.ruta= None
        self.duracion_cancion = None
        self.nombre_cancion = None
        self.btnFolder = btnFolder

      

        self.btnFolder.bind("<Button-1>",self.abrirDialogoCarpeta)
        self.btnOpenF.bind("<Button-1>", self.intercambiar_lista_musica)

class Tiempo_musica():
    def __init__(self, lista_musica,tiempo_actual_var, duracion_var,btnPlay, iconoPause,barra= None):
        self.lista_musica = lista_musica
        self.tiempo_actual_var = tiempo_actual_var
        self.duracion_var = duracion_var
        self.btnPlay=btnPlay
        self.iconoPause=iconoPause

        self.barra = barra

        self.reproducir_tiempo= False
    
    def pausar_tiempo_musica(self):
        self.reproducir_tiempo = False
        if self.barra:
            self.barra.pausar_barra()
        # Guarda el tiempo actual al pausar
        self.tiempo_pausado = pygame.mixer.music.get_pos()

    def reanudar_tiempo_musica(self):
        self.reproducir_tiempo = True
        self.barra.iniciar_barra()
        # Continúa actualizando el tiempo desde donde se pausó
        self.actualizar_tiempo_en_vivo()

    
    def reproducir_tiempo_musica(self):
        ruta= self.lista_musica.obtener_ruta_actual()
        if ruta:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play()
            self.barra.iniciar_barra()
            self.btnPlay.config(image=self.iconoPause)

            self.reproducir_tiempo = True
            self.segundos_actuales = 0  # Reinicia el tiempo actual
            self.tiempo_actual_var.set("00:00")  # Actualiza la interfaz

            self.duracion_var.set(self.lista_musica.duracion_cancion)
            self.actualizar_tiempo_en_vivo()
            
    
    def detener_tiempo_musica(self):
        pygame.mixer.music.stop()
        self.reproducir_tiempo = False
        self.tiempo_actual_var.set("00:00")
    
    def actualizar_tiempo_en_vivo(self):
     def actualizar():
        while self.reproducir_tiempo and pygame.mixer.music.get_busy():
            tiempo_ms = pygame.mixer.music.get_pos()
            segundos = int(tiempo_ms / 1000)
            minutos = segundos // 60
            segundos = segundos % 60
            tiempo_formateado = f"{minutos:02}:{segundos:02}"
            self.tiempo_actual_var.set(tiempo_formateado)
            time.sleep(1)
     threading.Thread(target=actualizar, daemon=True).start()


    def formatear_tiempo(self, segundos):
        minutos = int(segundos) // 60
        segundos = int(segundos) % 60
        return f"{minutos:02}:{segundos:02}"
    
    def mostrar_tiempo(self):
        self.tiempo_actual_var.set("00:00")
        self.duracion_var.set("00:00")
        
        self.tiempo_frame = tk.Frame(self.lista_musica.ventana, bg="#FFFFFF")
        self.tiempo_frame.place(x=500, y=250, width=450, height=50)

        self.tiempo_actual_label = tk.Label(self.tiempo_frame, textvariable=self.tiempo_actual_var, bg="#FFFFFF", fg="#000000")
        self.tiempo_actual_label.place(x=10, y=10)

        self.duracion_label = tk.Label(self.tiempo_frame, textvariable=self.duracion_var, bg="#FFFFFF", fg="#000000")
        self.duracion_label.place(x=400, y=10)
 



            

