#!/usr/bin/env python3
import rclpy # LIBRERIA PARA UTILIZAR PYTHON (ROS CLIENT LIBRARY PYTHON)
from rclpy.node import Node # PARA CREAR EL NODO
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 
import os # LIBRERIA PARA TRABAJAR CON ARCHIVOS
from example_interfaces.srv import SetBool
# VARIBALES GLOBALES A UTILIZAR
global cont 
global datos
global datos1
cont = 0
global inicio
inicio = True
datos = []

class TurtleBotPlayerNode(Node):
	def __init__(self):
		super().__init__("turtle_bot_player") # CREACIÓN DEL NODO
		self.publisher_ = self.create_publisher(Twist, "turtlebot_cmdVel",10) # CREACIÓN DEL SUBSCRIBER AL TOPICO DE VELOCIDAD
		self.timer_ = self.create_timer(0.75, self.recorrido) # TIEMPO DE MUESTREO
		self.cliente = self.create_client(SetBool, 'recorrido_guardado') # CREACIÓN DEL SERVICIO - CLIENTE
	
	def recorrido(self): # FUNCIÓN PARA INICIAR EL SERVICIO
		global inicio
		if inicio: # FUNCIÓN PARA ESPERAR LA COMUNIACION CON EL SERVICIO
			if not self.cliente.wait_for_service(timeout_sec=1.0): # ESPERANDO POR EL SERVICIO
				self.get_logger().warn('Esperando por el servicio...') 
				return
			request = SetBool.Request()
			request.data = True # COMUNICACIÓN BOOLEANA
			future = self.cliente.call_async(request)
			future.add_done_callback(self.funcion) # IR A LA FUNCION
		else:
			request = SetBool.Request()
			request.data = True
			future = self.cliente.call_async(request)
			future.add_done_callback(self.funcion) # IR A LA FUNCION
	
	def funcion(self, future): # FUNCION PARA RECIBIR LA RESPUESTA DEL NOMBRE Y LEER EL ARCHIVO
		global cont
		global inicio
		global datos1
		global datos
		if inicio:
			try:
				response = future.result()
				msg = Twist()	
				archivo_nombre = str(response.message) # OBTENER EL NOMBRE DEL ARCHIVO
				descargas_dir = os.path.join(os.path.expanduser("~"), "Downloads")
				archivo_ruta = os.path.join(descargas_dir, archivo_nombre) # BUSCARLO EN DESCARGAS
				try:
					with open(archivo_ruta, 'r') as archivo: # ABRIR EL ARCHIVO
						datos1 = [line.strip() for line in archivo.readlines()] # ARRAY CON TODAS LAS LINEAS DEL ARCHIVO
						inicio = False
				except FileNotFoundError:
					print(f"El archivo {archivo_ruta} no fue encontrado.")
			except Exception as e:
				self.get_logger().error('Servicio fallido ' + str(e,))
		else:
			datos = datos1
			msg = Twist()
			if 0 <= cont < len(datos): # PARA QUE NO SUPERE EL INDICE
				x = (datos[cont])
				valor = x.split(',') # SEPARAR POR COMA EL ARRAY
				msg.linear.x = float(valor[0]) # OBTENER LE VALOR DE VELOCIDAD LIENAL
				msg.angular.z = float(valor[1]) # OBTENER LE VALOR DE VELOCIDAD ANGULAR
				self.get_logger().info("Velocidad lineal: " + str(msg.linear.x))
				self.get_logger().info("Velocidad angular: " + str(msg.angular.z))
				self.publisher_.publish(msg) # PUBLICAR ESTAS VELOCIDADES
				cont += 1 # AUMENTAR EL CONTADOR
				print("Linea No. "+ str(cont) + " de "+ str(len(datos)))

def main(args=None): # FUNCIÓN PRINCIAL
	rclpy.init(args=args) # PARA INICIALIZAR EL CÓDIGO EN PYTHON
	node = TurtleBotPlayerNode()
	rclpy.spin(node) # PARA NO DEJAR MORIR LA COMUNICACIÓN
	rclpy.shutdown() # PARA APAGAR LA COMUNICACIÓN

if __name__ ==  "__main__":  # PARA CORRER LA FUNCIÓN PRINCIPAL
	main() # FUNCIÓN PRINCIPAL