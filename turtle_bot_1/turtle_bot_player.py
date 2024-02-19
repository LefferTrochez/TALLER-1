#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 
import os
import time

class TurtleBotPlayerNode(Node):
	def __init__(self):
		super().__init__("turtle_bot_player")
		self.publisher_ = self.create_publisher(Twist, "turtlebot_cmdVel",10)
		self.timer_ =self.create_timer(1/2, self.recorrido)
	
	def recorrido(self):
		msg = Twist()
		archivo_ruta = os.path.join(os.path.expanduser("~"), "recorrido.txt")
		try:
			with open(archivo_ruta, 'r') as archivo:
				datos = [line.strip() for line in archivo.readlines()]
			for i in datos[0:]:
				i = i.split(",")
				msg.linear.x = float(i[0])
				self.get_logger().info("lin: " + str(msg.linear.x))
				msg.angular.z = float(i[1])
				self.get_logger().info("vel: " + str(msg.angular.z))
				self.publisher_.publish(msg)
			msg.linear.x = float(123)
			msg.angular.z = float(123)
			self.publisher_.publish(msg)
			time.sleep(2)

		except FileNotFoundError:
			print(f"El archivo {archivo_ruta} no fue encontrado.")

def main(args=None):
	rclpy.init(args=args)
	node = TurtleBotPlayerNode()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ ==  "__main__":
	main()

