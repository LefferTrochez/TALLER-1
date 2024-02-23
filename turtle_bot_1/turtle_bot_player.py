#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 
import os
import time
from example_interfaces.srv import SetBool

class TurtleBotPlayerNode(Node):
	def __init__(self):
		super().__init__("turtle_bot_player")
		self.publisher_ = self.create_publisher(Twist, "turtlebot_cmdVel",10)
		self.timer_ = self.create_timer(0.2, self.recorrido)
		#self.timer1_ = self.create_timer(10, self.funcion)
		self.cliente = self.create_client(SetBool, 'recorrido_guardado')
	
	def recorrido(self):
		if not self.cliente.wait_for_service(timeout_sec=1.0):
			self.get_logger().warn('Servicio...')
			return

		request = SetBool.Request()
		request.data = True
		future = self.cliente.call_async(request)
		future.add_done_callback(self.funcion)
		#time.sleep(4)
		
	def funcion(self, future):
		try:
			response = future.result()
			self.get_logger().info('Respuesta del servidor: ' + str(response))
			#time.sleep(2)
			msg = Twist()	
			archivo_nombre = str(response.message)
			self.get_logger().info("ARCHIVO: " + str(archivo_nombre))
			#time.sleep(2)
			descargas_dir = os.path.join(os.path.expanduser("~"), "Downloads")
			archivo_ruta = os.path.join(descargas_dir, archivo_nombre)
			try:
				with open(archivo_ruta, 'r') as archivo:
					self.get_logger().info("entre a leer el archivo")
					datos = [line.strip() for line in archivo.readlines()]
					#while str(archivo_nombre) == "reco.txt":
					for i in datos[0:]:
						i = i.split(",")
						x = float(i[0])
						z = float(i[1])
						if str(x) == "0.0" and str(z) == "0.0" :
							None
						else:
							msg.linear.x = float (float(i[0] ) / 0.5)
							self.get_logger().info("lin: " + str(msg.linear.x))
							msg.angular.z = float (float(i[1] ) / 0.72)
							self.get_logger().info("vel: " + str(msg.angular.z))
							self.publisher_.publish(msg)
							msg.angular.z = float (0)
							msg.linear.x = float (0)
							self.publisher_.publish(msg)
							
							time.sleep(0.2)

			except FileNotFoundError:
				print(f"El archivo {archivo_ruta} no fue encontrado.")

		except Exception as e:
			self.get_logger().error('Servicio fallido ' + str(e,))


def main(args=None):
	rclpy.init(args=args)
	node = TurtleBotPlayerNode()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ ==  "__main__":
	main()