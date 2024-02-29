#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 
import os
from example_interfaces.srv import SetBool

class TurtleBotPlayerNode(Node):
	def __init__(self):
		super().__init__("turtle_bot_player")
		self.publisher_ = self.create_publisher(Twist, "turtlebot_cmdVel",10)
<<<<<<< Updated upstream
		self.timer_ = self.create_timer(5, self.recorrido)
=======
		self.timer_ = self.create_timer(1.85, self.recorrido)
>>>>>>> Stashed changes
		self.cliente = self.create_client(SetBool, 'recorrido_guardado')
	
	def recorrido(self):
		if not self.cliente.wait_for_service(timeout_sec=1.0):
			self.get_logger().warn('Servicio...')
			return

		request = SetBool.Request()
		request.data = True
		future = self.cliente.call_async(request)
		future.add_done_callback(self.funcion)
		
	def funcion(self, future):
		try:
			response = future.result()
			self.get_logger().info('Respuesta del servidor: ' + str(response))
			msg = Twist()	
			archivo_nombre = str(response.message)
			self.get_logger().info("ARCHIVO: " + str(archivo_nombre))
			descargas_dir = os.path.join(os.path.expanduser("~"), "Downloads")
			archivo_ruta = os.path.join(descargas_dir, archivo_nombre)
			try:
				with open(archivo_ruta, 'r') as archivo:
					self.get_logger().info("entre a leer el archivo")
					datos = [line.strip() for line in archivo.readlines()]
					for i in datos[0:]:
						i = i.split(",")
						x = float(i[0])
						z = float(i[1])
						if str(x) == "0.0" and str(z) == "0.0" :
							None
						else:
							msg.linear.x = float(i[0])
							self.get_logger().info("lin: " + str(msg.linear.x))
							msg.angular.z = float(i[1])
							self.get_logger().info("ang: " + str(msg.angular.z))
							self.publisher_.publish(msg)

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