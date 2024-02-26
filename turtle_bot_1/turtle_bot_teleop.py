#!/usr/bin/env python3
import rclpy # LIBRERIA PARA UTILIZAR PYTHON (ROS CLIENT LIBRARY PYTHON)
from sshkeyboard import listen_keyboard # PARA MONITOREAR EL TECLADO
from geometry_msgs.msg import Twist # ES EL TIPO DE MENSAJE 

TurtleBotTeleopNode = rclpy.create_node("turtle_bot_teleop") # CREACIÓN DEL NODO
linear_in = float(input("What is the Linear Velocity?: ")) # PEDIR VELOCIDAD LINEAL AL USUARIO
angular_in = float(input("What is the Angular Velocity?: ")) # PEDIR VELOCIDAD ANGULAR AL USUARIO
TurtleBotTeleopNode.get_logger().info('\n' '\n' "Now, to move the robot you have to press: " '\n' "w | a | s | d") # IMPRIMIR INSTRUCCIONES
msg = Twist() # TIPO DE MENSAJE 
global linear_out , angular_out # ATRIBUTO DE LAS VARIABLES AUXILIARES
linear_out = 0.0 # VARIABLE AUXILIAR PARA LA VELOCIDAD LINEAL
angular_out = 0.0 # VARIABLE AUXILIAR PARA LA VELOCIDAD ANGULARwdsd

def PressCase(key): # FUNCIÓN PARA CUANDO SE PRESIONA UNA TECLA
    global linear_out , angular_out # ATRIBUTO DE LAS VARIABLES AUXILIARES
    if key == 'w': # SI SE PRESIONA LA TECLA W
        linear_out = linear_out + linear_in # VA HACIA ADELANTE
    elif key == 's':  # SI SE PRESIONA LA TECLA S
        linear_out = - linear_out - linear_in # VA HACIA ATRÁS
    elif key == 'a':  # SI SE PRESIONA LA TECLA A
        angular_out = angular_out + angular_in # GIRA A LA IZQUIERDA
    elif key == 'd':  # SI SE PRESIONA LA TECLA D
        angular_out = - angular_out - angular_in # GIRA A LA DERECHA
    else: # SI SE PRESIONA UNA TECLA DIFERENTE
        print('Key no valid!')
    msg.linear.x = linear_out # OBTENER VELOCIDAD LINEAL
    msg.angular.z = angular_out # OBTENER VELOCIDAD ANGULAR
    Publish.publish(msg) # PUBLICAR VELOCIDADES

def ReleaseCase(key):
    global linear_out , angular_out # ATRIBUTO DE LAS VARIABLES AUXILIARES
    if key == "w": # SI SE PRESIONA LA TECLA W
        linear_out = linear_out - linear_in # DETIENE LA VELOCIADAD LINEAL HACIA ADELANTE
    elif key == "s": # SI SE PRESIONA LA TECLA S
        linear_out = linear_out + linear_in # DETIENE LA VELOCIADAD LINEAL HACIA ATRAS
    elif key == "a": # SI SE PRESIONA LA TECLA A
        angular_out = angular_out - angular_in # DETIENE LA VELOCIADAD ANGULAR HACIA LA IZQUIERDA
    elif key == "d":  # SI SE PRESIONA LA TECLA D
        angular_out = angular_out + angular_in # DETIENE LA VELOCIADAD ANGULAR HACIA LA DERECHA
    msg.linear.x = linear_out # OBTENER VELOCIDAD LINEAL
    msg.angular.z = angular_out # OBTENER VELOCIDAD ANGULAR
    Publish.publish(msg) # PUBLICAR VELOCIDADES

rclpy.init() # INICILIZACIÓN DEL CÓDIGO
TurtleBotTeleopNode = rclpy.create_node("turtle_bot_teleop") # CREACIÓN DEL NODO
Publish = TurtleBotTeleopNode.create_publisher(Twist, "turtlebot_cmdVel", 10) # CREACIÓN DEL PUBLISHER
TurtleBotTeleopNode.create_timer(0.2, PressCase)
TurtleBotTeleopNode.create_timer(0.2, ReleaseCase)



def main(args=None): # FUNCIÓN PRINCIAL
    listen_keyboard(on_press=PressCase, on_release=ReleaseCase,) # COMANDO PARA MONITOREAR EL TECLADO
    rclpy.init(args=args) # PARA INICIALIZAR EL CÓDIGO EN PYTHON
    rclpy.spin(TurtleBotTeleopNode) # PARA NO DEJAR MORIR LA COMUNICACIÓN
    rclpy.shutdown() # PARA APAGAR LA COMUNICACIÓN

if __name__ == '__main__': # PARA CORRER LA FUNCIÓN PRINCIPAL
    main() # FUNCIÓN PRINCIPAL