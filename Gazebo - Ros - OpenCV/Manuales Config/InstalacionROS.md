# Instalación y configuración ROS

Usaremos la versión Indigo de ROS. 

Inicialmente, debemos configurar los repositorios de Ubuntu para permitir instalaciones "restricted", "universe" y "multiverse".

![packagesubuntu](https://gitlab.com/eci-artvision-pgr/pruebas-concepto-simulacion-cv/blob/22e2e3618679ab692b0dcfee15ca0758f95e9343/paquetesubuntu.png)


A continuación, debemos ejecutar el comando que permitirá recibir paquetes desde packages.ros.org:

	`sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'`

Realizamos la configuración de llaves:

	`sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116`

Actualizamos los paquetes del sistema operativo:

	`sudo apt-get update`

En caso de que aparezcan errores de dependencias, utilizamos el siguiente comando:

	`sudo apt-get install libgl1-mesa-dev-lts-utopic`

A continuación se procede a realizar la instalación completa:

	`sudo apt-get install ros-indigo-desktop-full`

Si se necesita instalar un paquete específico, se usa el siguiente comando, reemplazando PACKAGE por el nombre del paquete a instalar:

	`sudo apt-get install ros-indigo-PACKAGE`

Antes de usar ROS, debemos inicializar rosdep, herramienta que nos permitirá instalar dependencias y correr algunos componentes de ROS:

	`sudo rosdep init`
	`rosdep update`

Finalmente, se recomienda que las variables de entorno de ROS sean añadidas automáticamente cada vez que se abra una nueva terminal:

	`echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc`
	`source ~/.bashrc`

---

# Gazebo con ROS

Una vez instalado ROS, instalamos los simuladores necesarios:

	`sudo apt-get install ros-indigo-simulators`

Y finalmente, configuramos las variables de entorno nuevamente:

	`source /opt/ros/%YOUR_ROS_DISTRO%/setup.bash`

Existen varias formas de iniciar Gazebo con ROS:

  1. `roslaunch gazebo_ros empty_world.launch`
  2. `roscore &`
     `rosrun gazebo_ros gazebo`
  3. `rosrun gazebo_ros gazebo` (para iniciar el cliente y el servidor juntos)




