# Grabación y obtención del video tomado por la cámara del robot dentro de Gazebo

Para este ejemplo, usaremos el robot "Turtlebot", el cual usa varios "topics" de imágen. Se utilizará el topic /camera/rgb/image_raw.

Primero, iniciamos Gazebo con ROS usando el robot Turtlebot:

	`roslaunch turtlebot_gazebo turtlebot_world.launch`

En una nueva terminal, ejecutaremos el siguiente comando para poder mover el robot:
	
	`roslaunch turtlebot_teleop keyboard_teleop.launch`

En una terminal diferente, ejecutamos el siguiente comando para lanzar el topic:

	`rosrun image_view image_view image:=/camera/rgb/image_raw`

Y finalmente, en otra terminal diferente, ejecutamos el comando para iniciar el grabador de video:

	`rosrun image_view video_recorder image:=/camera/rgb/image_raw`

Así, obtendremos el video grabado por la cámara del robot dentro del entorno Gazebo.




