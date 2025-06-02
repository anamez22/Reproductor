import pygame.mixer as mx

class Barra_progresso:
    def __init__(self, barra_progreso,duracion_segundos, tiempo_actual_var=None, tiempo=None):
        
        self.barra_progreso = barra_progreso
        self.duracion_segundos = duracion_segundos
        self.tiempo_actual_var = tiempo_actual_var
        self.tiempo = tiempo
        self.actualizando = False
    
        self.barra_progreso.bind("<ButtonRelease-1>", self.usuario_mueve_barra)


    def actualizar_barra(self):
        if not self.actualizando:
            return
        if mx.music.get_busy():
            tiempo_ms = mx.music.get_pos()
            segundos = int(tiempo_ms / 1000)
            if self.duracion_segundos > 0:
                progreso = (segundos / self.duracion_segundos) * 100
                self.barra_progreso.set(progreso)  
            if self.tiempo_actual_var is not None:
                minutos = segundos // 60
                seg = segundos % 60
                self.tiempo_actual_var.set(f"{minutos:02}:{seg:02}")
            self.barra_progreso.after(500, self.actualizar_barra)
        else:
            if not self.actualizando:
                return 

    def iniciar_barra(self):
        self.actualizando = True
        self.actualizar_barra()

    def pausar_barra(self):
        self.actualizando = False

    def usuario_mueve_barra(self, event):
        if self.duracion_segundos > 0:
            progreso = self.barra_progreso.get()
            nuevo_tiempo = int((progreso / 100) * self.duracion_segundos)
            mx.music.stop()
            mx.music.play(start=nuevo_tiempo)
            self.barra_progreso.set(progreso)
            if self.tiempo_actual_var is not None:
                minutos = nuevo_tiempo // 60
                seg = nuevo_tiempo % 60
                self.tiempo_actual_var.set(f"{minutos:02}:{seg:02}")
            self.actualizando = True
            self.barra_progreso.after(200, self.actualizar_barra)            
            if hasattr(self.tiempo, "pausa"):
                self.tiempo.pausa = False     