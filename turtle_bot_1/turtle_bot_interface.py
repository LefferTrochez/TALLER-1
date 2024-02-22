#!/usr/bin/env python3
import rclpy # LIBRERIA PARA UTILIZAR PYTHON (ROS CLIENT LIBRARY PYTHON)
import pygame # BIBLIOTECA PARA APLICACIONES MULTIMEDIA
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 
from tkinter import filedialog # PARA LA SELECCIÓN DE ARCHIVOS Y DIRECTORIOS
import os # INTERFACE PARA INTERACTUAR CON EL SISTEMA OPERATIVO SUBYACENTE
import time
from example_interfaces.srv import SetBool
import copy
pygame.init() # INICILIZACIÓN DEL CÓDIGO
pantalla = pygame.display.set_mode((600, 650)) # CREACIÓN DE LA PANTALLA Y TAMAÑO DE LA MISMA
robot = (0, 0, 0) # COLOR DEL ROBOT - NEGRO - (R G B)
pantalla.fill((255, 255, 255)) # COLOR DEL FONDO - BLANCO - (R G B)
global vel_lineal
global vel_angular
global x
global y
global lista_lineal
global lista_angular
global pos_x
global pos_y
global mantener
global primero
global cuatro
global demas
global resp_demas
global otro
global velocidad_lineal, velocidad_angular

def evento(i, forma_boton, funcion_asiganada = None): # FUNCIÓN PARA DETECTAR EL MOUSE
    if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1: # DETECCIÓN DEL MOUSE
        if forma_boton.collidepoint(i.pos): # HABILITAR EL BOTÓN
            if funcion_asiganada: 
                funcion_asiganada() # CORRER LA FUNCIÓN ASIGNADA

def boton(pantalla, posicion_y_boton, texto, function = None): # FUNCIÓN PARA CREAR EL BOTÓN
    posicion_x_boton = 430 # POSICIÓN X DEL BOTON DENTRO DE LA PANTALLA
    ancho_boton = 160 # DIMENSIÓN ANCHO DEL BOTÓN
    alto_boton = 30 # DIMENSIÓN ALTO DEL BOTÓN
    parametro_boton = pygame.Surface((ancho_boton, alto_boton)) # DEFINE EL ANCHO Y ALTO DEL BOTÓN
    parametro_boton.fill((0, 0, 0)) # DEFINE EL COLOR DEL BOTÓN - NEGRO - (R G B)
    fuente_boton = pygame.font.SysFont("Aharoni", 24) # TIPO DE FUENTE DEL BOTÓN Y TAMAÑO DE LA LETRA
    texto_boton = fuente_boton.render(texto, True, (255, 255, 255)) # CREAR EL TEXTO DEL BOTÓN EN COLOR BLANCO - (R G B)
    parametro_boton.blit(texto_boton, ((1/2)*(ancho_boton - texto_boton.get_width()), (1/2)*(alto_boton - texto_boton.get_height()))) # PONER TEXTO EN LA SUPERFICIE DEL BOTÓN CENTRADO
    pantalla.blit(parametro_boton, (posicion_x_boton, posicion_y_boton)) # CONSTRUIR EL BOTÓN EN LA PANTALLA
    forma_boton = pygame.Rect(posicion_x_boton, posicion_y_boton, ancho_boton, alto_boton) # FORMA RECTÁNGULAR DEL BOTÓN INSERTADO EN LA PANTALLA
    return parametro_boton, forma_boton # RETORNOS DE LA FUNCIÓN

def boton_decision(pantalla, posicion_x_boton, texto, function = None): # FUNCIÓN PARA CREAR EL BOTÓN
    posicion_y_boton = 325 # POSICIÓN Y DEL BOTON DENTRO DE LA PANTALLA
    ancho_boton = 110 # DIMENSIÓN ANCHO DEL BOTÓN
    alto_boton = 30 # DIMENSIÓN ALTO DEL BOTÓNs
    parametro_boton = pygame.Surface((ancho_boton, alto_boton)) # DEFINE EL ANCHO Y ALTO DEL BOTÓN
    parametro_boton.fill((0, 0, 0)) # DEFINE EL COLOR DEL BOTÓN - NEGRO - (R G B)
    fuente_boton = pygame.font.SysFont("Aharoni", 24) # TIPO DE FUENTE DEL BOTÓN Y TAMAÑO DE LA LETRA
    texto_boton = fuente_boton.render(texto, True, (255, 255, 255)) # CREAR EL TEXTO DEL BOTÓN EN COLOR BLANCO - (R G B)
    parametro_boton.blit(texto_boton, ((1/2)*(ancho_boton - texto_boton.get_width()), (1/2)*(alto_boton - texto_boton.get_height()))) # PONER TEXTO EN LA SUPERFICIE DEL BOTÓN CENTRADO
    pantalla.blit(parametro_boton, (posicion_x_boton, posicion_y_boton)) # CONSTRUIR EL BOTÓN EN LA PANTALLA
    forma_boton = pygame.Rect(posicion_x_boton, posicion_y_boton, ancho_boton, alto_boton) # FORMA RECTÁNGULAR DEL BOTÓN INSERTADO EN LA PANTALLA
    return parametro_boton, forma_boton # RETORNOS DE LA FUNCIÓN

primero = True
def callback(msg): # FUNCIÓN PARA GRAFICAR EN TIEMPO REALuuuuuuu
        if primero:
            preguntar = pygame.font.SysFont("Arial", 30) 
            texto_preguntar = preguntar.render("¿Quieres guardar el recorrido del TurtleBot?", True, (0, 0, 0)) 
            posicion_x_preguntar = 12 # POSICIÓN X DEL TÍTULO DENTRO DE LA PANTALLA
            posicion_y_preguntar = 250 # POSICIÓN Y DEL TÍTULO DENTRO DE LA PANTALLA
            pantalla.blit(texto_preguntar, (posicion_x_preguntar, posicion_y_preguntar)) # PONER EL TEXTO DEL TÍTULO EN LA PANTALLA
            pygame.display.update()  # ACTUALIZAR
            posicion_x_boton_no = 350
            posicion_x_boton_si = 150
            parametro_boton, Boton_si = boton_decision(pantalla,posicion_x_boton_si , "Si quiero") 
            parametro_boton, Boton_no = boton_decision(pantalla, posicion_x_boton_no ,"No quiero") 
            resp_demas = 0
            for i in pygame.event.get(): # ENTRAR A LA FUNCIÓN EVENTO
                evento(i, Boton_si, funcion_asiganada = lambda:SiQuiero()) 
                evento(i, Boton_no, funcion_asiganada = lambda:NoQuiero()) 

        else:
                if escribir: 
                    global velocidad_angular, velocidad_lineal
                    pygame.display.update() # ACTUALI
                    x = (msg.linear.x)*100
                    y = (msg.linear.y)*100
                    vel_lineal = 0
                    vel_angular = 0
                    velocidad_lineal = (msg.linear.x)
                    velocidad_angular = (msg.angular.z)

                    if len(str(velocidad_lineal)) < 7:
                        vel_lineal = velocidad_lineal
                    if len(str(velocidad_angular)) < 7:
                        vel_angular = velocidad_angular
                    print("veloc lineal: " + str(vel_lineal))
                    print("veloc angular: " + str(vel_angular))
                    EscribirArchivoTexto(vel_lineal, vel_angular, "SinNombre.txt")
                    
                    if len(str(x)) > 6 and len(str(y)) > 6:

                    # print("este es x: " + str(x))
                    # print("este es y: " + str(y))
                        pygame.draw.circle(pantalla, robot, (x+pantalla.get_width()/2, -y+pantalla.get_height()/2), 4) # DIBUJA EL CIRCULO EN LA PANTALLA EN LA COORDENADA DADA
                        titulo = pygame.font.SysFont("Arial", 26) # TIPO DE FUENTE DEL TÍTULO Y TAMAÑO DE LA LETRA
                        texto_titulo = titulo.render("Gráfica de Posición TurtleBot", True, (0, 0, 0)) # TÍTULO DE LA  GRÁFICA
                        posicion_x_titulo = 20 # POSICIÓN X DEL TÍTULO DENTRO DE LA PANTALLA
                        posicion_y_titulo = 25 # POSICIÓN Y DEL TÍTULO DENTRO DE LA PANTALLA
                        pantalla.blit(texto_titulo, (posicion_x_titulo, posicion_y_titulo)) # PONER EL TEXTO DEL TÍTULO EN LA PANTALLA
                        velocidad_lineal = (msg.linear.x)
                        velocidad_angular = (msg.angular.z)
                    #  print("angular : " + str(velocidad_angular))
                #        vel_lineal = 0
                  #      vel_angular = 0

                        
                        pygame.display.update()  # ACTUALIZAR
                        posicion_y_boton_imagen = 10 # POSICIÓN Y DEL BOTON DENTRO DE LA PANTALLA
                        parametro_boton, Boton_guardar_imagen = boton(pantalla, posicion_y_boton_imagen, "Guardar imagenn") # CREAR EL BOTÓN "GUARDAR"
                        posicion_y_boton_recorrido = 45 # POSICIÓN Y DEL BOTON DENTRO DE LA PANTALLA
                        parametro_boton, Boton_guardar_recorrido = boton(pantalla, posicion_y_boton_recorrido, "Guardar recorrido") # CREAR EL BOTÓN "GUARDAR"
                        for i in pygame.event.get(): # ENTRAR A LA FUNCIÓN EVENTO
                            evento(i, Boton_guardar_imagen, funcion_asiganada = lambda:GuardarImagen()) # SI SE OPRIME EL BOTÓN "GUARDAR" CORRER LA FUNCIÓN "GUARDAR ARCHIVO"
                            evento(i, Boton_guardar_recorrido, funcion_asiganada = lambda:GuardarRecorrido()) 
                            pygame.display.update() # ACTUALIZAR

                    
                
                
                else: 
                    x = (msg.linear.x)*500 # COORDENADA DEL ROBOT EN X ESCALA POR 100
                    y = (msg.linear.y)*500 # COORDENADA DEL ROBOT EN Y ESCALA POR 100
                    pygame.draw.circle(pantalla, robot, (x+pantalla.get_width()/2, -y+pantalla.get_height()/2), 4) # DIBUJA EL CIRCULO EN LA PANTALLA EN LA COORDENADA DADA
                    titulo = pygame.font.SysFont("Arial", 26) # TIPO DE FUENTE DEL TÍTULO Y TAMAÑO DE LA LETRA
                    texto_titulo = titulo.render("Gráfica de Posición TurtleBot", True, (0, 0, 0)) # TÍTULO DE LA  GRÁFICA
                    posicion_x_titulo = 20 # POSICIÓN X DEL TÍTULO DENTRO DE LA PANTALLA
                    posicion_y_titulo = 25 # POSICIÓN Y DEL TÍTULO DENTRO DE LA PANTALLA
                    pantalla.blit(texto_titulo, (posicion_x_titulo, posicion_y_titulo)) # PONER EL TEXTO DEL TÍTULO EN LA PANTALLA
                    pygame.display.update()  # ACTUALIZAR
                    posicion_y_boton_imagen = 10 # POSICIÓN Y DEL BOTON DENTRO DE LA PANTALLA
                    parametro_boton, Boton_guardar_imagen = boton(pantalla, posicion_y_boton_imagen, "Guardar imagen") # CREAR EL BOTÓN "GUARDAR"
                    for i in pygame.event.get(): # ENTRAR A LA FUNCIÓN EVENTO
                        evento(i, Boton_guardar_imagen, funcion_asiganada = lambda:GuardarImagen()) # SI SE OPRIME EL BOTÓN "GUARDAR" CORRER LA FUNCIÓN "GUARDAR ARCHIVO"
                        pygame.display.update() # ACTUALIZAR



def EscribirArchivoTexto (vel_lineal , vel_angular, nombre_txt):
    with open(nombre_txt, 'a') as archivo:
        archivo.write(str(vel_lineal) + " , " + str(vel_angular) +'\n')

demas = 0
def SiQuiero():
    print("entro a SiQuiero")
    global escribir, primero
    escribir = True
    pantalla.fill((255, 255, 255))
    pygame.display.update() # ACTUALIZAR
    resp_demas = inicio_demas(demas)
    print("demas es: " + str(resp_demas))
    primero = False

  #  return primero

def NoQuiero():
    global escribir, primero
    escribir = False
    pantalla.fill((255, 255, 255))
    pygame.display.update() # ACTUALIZAR
    primero = False
        
def GuardarImagen(): # FUNCIÓN PARA GUARDAR LA IMAGEN DEL RECORRIDO
    imagen = pygame.Surface(pantalla.get_size()) # TOMA EL TAMAÑO DE LA PANTALLA
    imagen.blit(pantalla, (0, 0)) # CAPTURA LA IMAGEN
    pygame.image.save(imagen, 'SinNombre.png') # GUARDA LA IMAGEN CON EL NOMBRE POR DEFECTO "SINNOMBRE" POR SI NO SE LE DA UN NOMBRE A LA IMAGEN
    archivo = filedialog.asksaveasfilename(defaultextension='.png') # PREGUNTAR AL USUARIO POR EL NOMBRE DE LA GRÁFICA
    if archivo: # ENTRA AL ARCHIVO 
        with open('SinNombre.png', 'rb') as SinNombre: # ABRIR EL ARCHIVO EN MODO LECTURA BINARIA
            with open(archivo, 'wb') as ConNombre: # ABRIR EL ARCHIVO EN MODO ESCRITURA BINARIA
                ConNombre.write(SinNombre.read()) # ESCRIBIR EN EL ARCHIVO EL CONTENIDO DE LA IMAGEN "SINNOMBRE"
                os.remove('SinNombre.png') # ELIMINA LA IMAGEN "SINNOMBRE" Y DEJA LA IMAGEN ARCHIVO 
                os.remove('SinNombre.txt') # ELIMINA LA IMAGEN "SINNOMBRE" Y DEJA LA IMAGEN ARCHIVO 

def GuardarRecorrido(): # FUNCIÓN PARA GUARDAR LA IMAGEN DEL RECORRIDO
    archivo = filedialog.asksaveasfilename(defaultextension='.txt') # PREGUNTAR AL USUARIO POR EL NOMBRE DE LA GRÁFICA
    Nombre_predetermiando = "SinNombre.txt"
    if archivo: # ENTRA AL ARCHIVO 
        with open(Nombre_predetermiando, 'rb') as SinNombre: # ABRIR EL ARCHIVO EN MODO LECTURA BINARIA
            with open(archivo, 'wb') as ConNombre: # ABRIR EL ARCHIVO EN MODO ESCRITURA BINARIA
                ConNombre.write(SinNombre.read()) # ESCRIBIR EN EL ARCHIVO EL CONTENIDO DE LA IMAGEN "SINNOMBRE"
                ConNombre.close()

cuatro = 0
def servicio_player(request, response):
        print("soy servicio player")
        var = inicio_cuatro(cuatro)
        print("var es: " +  str(var))
        if var == 1:
            print("entro a servicio player")
            if request.data:
                response.success = True
                file_options = {
            'title': 'Seleccionar un archivo',
            'filetypes': [('Todos los archivos', '.*')],
            'initialdir': '~/Downloads',  # Directorio inicial, ajusta esto según tu sistema
        }
                archivo = filedialog.askopenfilename(**file_options)
                nombre_archivo = os.path.basename(archivo)
                response.message = str(nombre_archivo)

                print("Servidor response: " + str(response))
                print("Servidor request: " + str(request))
                RecorridoTxt(msg=Twist())

                #print("el archivo es: " + str(nombre_archivo))
            else:
                response.success = False
                response.message = "no puedo"
                print("Servidor response: " + str(response))
                print("Servidor request: " + str(request))
            return response

global aqui
aqui = True
otro = 0
def RecorridoTxt (msg):
    print("soy REcorridoTxt")
    var = inicio_otro(otro)
    print("var es: " +  str(var))
    if var == 1:
        TurtleBotInterfaceNode = rclpy.create_node('turtle_bot_interface') 
        TurtleBotInterfaceNode.create_subscription(Twist, '/turtlebot_position', RecorridoTxt, 10) # CREACIÓN DEL SUSCRIBER
        print("entro a REcorridoTxt")
        global aqui
        pantalla.fill((255, 255, 255))
        if aqui:
            pygame.display.update() #
            pos_x = 0
            pos_y = 0
            if len(str(msg.linear.x)) > 5:
                pos_x = (msg.linear.x)*500
            if len(str(msg.linear.y)) > 5:
                pos_y = (msg.linear.y)*500
            print(pos_x)
            print(pos_y)
            pygame.draw.circle(pantalla, robot, (pos_x+pantalla.get_width()/2, -pos_y+pantalla.get_height()/2), 4) # DIBUJA EL CIRCULO EN LA PANTALLA EN LA COORDENADA DADA


def inicio_cuatro(cuatro):
    print("entro al inicio cuatro")
    cuatro = 1
    pantalla.fill((255, 255, 255))
    pygame.display.update() # ACTUALIZAR
    
    return cuatro

def inicio_demas(demas):
    demas = 1
    pantalla.fill((255, 255, 255))
    pygame.display.update() # ACTUALIZAR
    primero = False
    return demas


def inicio_otro(otro):
    otro = 1
    pantalla.fill((255, 255, 255))
    pygame.display.update() # ACTUALIZAR
    return otro


def main(args=None): # FUNCIÓN PRINCIAL
   # msg = Twist()
    rclpy.init(args=args) # PARA INICIALIZAR EL CÓDIGO EN PYTHON
    TurtleBotInterfaceNode = rclpy.create_node('turtle_bot_interface') # CREACIÓN DEL NODO
    Servicio = TurtleBotInterfaceNode.create_service(SetBool, 'recorrido_guardado', servicio_player)
    subscriber_position = TurtleBotInterfaceNode.create_subscription(Twist, '/turtlebot_position', callback, 10) # CREACIÓN DEL SUSCRIBER
    subscriber_velocidad = TurtleBotInterfaceNode.create_subscription(Twist, '/turtlebot_cmdVel', callback, 10) # CREACIÓN DEL SUSCRIBER
    callback(msg = Twist())
 #   subscriber_recorrido_pos = TurtleBotInterfaceNode.create_subscription(Twist, '/turtlebot_position', RecorridoTxt, 10) # CREACIÓN DEL SUSCRIBER
    rclpy.spin(TurtleBotInterfaceNode) # PARA NO DEJAR MORIR LA COMUNICACIÓN
    rclpy.shutdown() # PARA APAGAR LA COMUNICACIÓN

if __name__ == '__main__': # PARA CORRER LA FUNCIÓN PRINCIPAL
    main() # FUNCIÓN PRINCIPAL