#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 
import os
from example_interfaces.srv import SetBool

global cont 
global datos
global datos1
cont = 0
global inicio
inicio = True
datos = []

class TurtleBotPlayerNode(Node):
	def __init__(self):
		super().__init__("turtle_bot_player")
		self.publisher_ = self.create_publisher(Twist, "turtlebot_cmdVel",10)
		self.timer_ = self.create_timer(0.2, self.recorrido)
		self.cliente = self.create_client(SetBool, 'recorrido_guardado')
	
	def recorrido(self):
		global inicio
		if inicio:
			if not self.cliente.wait_for_service(timeout_sec=1.0):
				self.get_logger().warn('Servicio...')
				return
			request = SetBool.Request()
			request.data = True
			future = self.cliente.call_async(request)
			future.add_done_callback(self.funcion)
		else:
			request = SetBool.Request()
			request.data = True
			future = self.cliente.call_async(request)
			future.add_done_callback(self.funcion)
	
	def funcion(self, future):
		global cont
		global inicio
		global datos1
		global datos
		
		if inicio:
			try:
				response = future.result()
				msg = Twist()	
				archivo_nombre = str(response.message)
				descargas_dir = os.path.join(os.path.expanduser("~"), "Downloads")
				archivo_ruta = os.path.join(descargas_dir, archivo_nombre)
				try:
					with open(archivo_ruta, 'r') as archivo:
						datos1 = [line.strip() for line in archivo.readlines()]
						inicio = False

				except FileNotFoundError:
					print(f"El archivo {archivo_ruta} no fue encontrado.")
			except Exception as e:
				self.get_logger().error('Servicio fallido ' + str(e,))

		else:
			datos = datos1
			msg = Twist()
			if 0 <= cont < len(datos):
				x = (datos[cont])
				valor = x.split(',')
				msg.linear.x = float(valor[0])
				msg.angular.z = float(valor[1])
				print(msg.linear.x)
				print(msg.angular.z)
				self.get_logger().info("lineal: " + str(msg.linear.x))
				self.get_logger().info("angular: " + str(msg.angular.z))
				self.publisher_.publish(msg)
				cont += 1
				print(cont)

def main(args=None):
	rclpy.init(args=args)
	node = TurtleBotPlayerNode()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ ==  "__main__":
	main()