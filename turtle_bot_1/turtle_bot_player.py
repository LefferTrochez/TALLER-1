#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 
import os

class TurtleBotPlayerNode(Node):
	def __init__(self):
		super().__init__("turtle_bot_player")
		self.publisher_ = self.create_publisher(Twist, "turtlebot_cmdVel",10)
		self.timer_ =self.create_timer(1/2, self.recorrido)
		self.get_logger().info("dentro")
	
	def recorrido(self, msg=Twist()):
		archivo_ruta = os.path.join(os.path.expanduser("~"), "recorrido.txt")
		try:
			with open(archivo_ruta, 'r') as archivo:
				contenido = archivo.read()
				print(contenido)
				for linea in archivo:
					datos = linea.strip().split(',')
					msg.linear.x = float(datos[0])
					print("lin: " + str(msg.linear.x))
					msg.angular.z = float(datos[1])
					print("vel: " + str(msg.angular.z))
					self.publisher_.publish(msg)

		except FileNotFoundError:
			print(f"El archivo {archivo_ruta} no fue encontrado.")

def main(args=None):
	rclpy.init(args=args)
	node = TurtleBotPlayerNode()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ ==  "__main__":
	main()

