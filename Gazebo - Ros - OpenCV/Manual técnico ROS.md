# Instalación y configuración ROS

En este manual se instalará la versión Indigo de ROS. 

Inicialmente, debemos configurar los repositorios de Ubuntu para permitir instalaciones "restricted", "universe" y "multiverse":

![alt-text](https://drive.google.com/uc?id=0B7qDHl7DSpgQOHM4MmJ1NkRnV2c "Multiverse")

A continuación, debemos ejecutar el comando que permitirá recibir paquetes desde packages.ros.org:

```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```

Realizamos la configuración de llaves:
```bash 
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
```

Actualizamos los paquetes del sistema operativo:
```bash
sudo apt-get update
```

En caso de que aparezcan errores de dependencias, utilizamos el siguiente comando:
```bash
sudo apt-get install libgl1-mesa-dev-lts-utopic
```

A continuación se procede a realizar la instalación completa de ROS Indigo:
```bash
sudo apt-get install ros-indigo-desktop-full
```
Debido a que ROS funciona con versiones específicas de Gazebo, el anterior comando desinstalará la versión actual de Gazebo y procederá a instalar la versión específica para la distribución utilizada.

**Importante: En caso de que aparezcan errores con paquetes, se recomienda instalar paquete por paquete hasta que se permita ejecutar el comando de instalación completa. De igual forma se recomienda el uso del gestor de paquetes Aptitude para aquellos paquetes que no se puedan instalar por medio del comando apt-get.**

Si se necesita instalar un paquete específico, se usa el siguiente comando, reemplazando PACKAGE por el nombre del paquete a instalar:
```bash
sudo apt-get install ros-indigo-PACKAGE
```

Antes de usar ROS, debemos inicializar rosdep, herramienta que nos permitirá instalar dependencias y correr algunos componentes de ROS:
```bash
sudo rosdep init
rosdep update
```

Finalmente, se recomienda que las variables de entorno de ROS sean añadidas automáticamente cada vez que se abra una nueva terminal:
```bash
echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

# Gazebo con ROS

Una vez instalado ROS, instalamos los simuladores necesarios:
```bash
sudo apt-get install ros-indigo-simulators
```

Finalmente, configuramos las variables de entorno nuevamente (donde %YOUR_ROS_DISTRO% es la distribución de ROS instalada):
```bash
source /opt/ros/%YOUR_ROS_DISTRO%/setup.bash
```

Existen varias formas de iniciar Gazebo con ROS:

  1. ```roslaunch gazebo_ros empty_world.launch ```
  2. ```roscore &```
     ```rosrun gazebo_ros gazebo```
  3. ```rosrun gazebo_ros gazebo``` (para iniciar el cliente y el servidor juntos)


---

# Modelo de robot controlado por ROS

El siguiente modelo, realizado con la versión Indigo de ROS y la versión 14.04 de Ubuntu, es una adaptación del [tutorial][1] realizado por Vanessa Mazzari para el blog llamado "Generation Robots".

Después de realizar la instalación de ROS y Gazebo, se procede a descargar los archivos fuentes del tutorial. Se puede apreciar principalmente la siguiente estructura de directorios:

![alt-text](https://drive.google.com/uc?id=0B7qDHl7DSpgQMndfc2ZjRjFsMGs "Directorios")

De la anterior estructura, nos enfocamos principalmente en el subdirectorio src, el cual contiene toda la información del modelo. De igual forma, se pueden observar tres subdirectorios dentro de src, los cuales son:

* mybot_control: el cual contiene los directorios config, donde se encuentra el archivo de configuración de los controladores del robot y launch, donde se encuentra el archivo que carga y gestiona los mismos.

* mybot_description: el cual contiene el directorio urdf, dentro del cual se encuentran los archivos que describen al robot, como sus componentes, la geometría y física de los mismos, así como los colores y el tamaño de éstos. Específicamente, se encuentran los siguiente archivos:
	* mybot.xacro: el cual contiene la descripción principal del robot.
	* mybot-gazebo: el cual contiene todos los aspectos específicos para Gazebo del robot.
	* materials.xacro: el cual contiene la definición de los materiales usados en el robot, en su mayoría        colores.
	* macros.xacro: el cual contiene la definición de varias macros que permiten describir de forma más clara y corta al robot.	 

* mybot_gazebo: el cual contiene los directorios launch, donde se encuentra el archivo con la información de los elementos que van a iniciar al momento de ejecutar el comando roslaunch, tanto el modelo, como programas adicionales como rviz, y el directorio worlds, donde se encuentra el archivo con la información del entorno en el cual va a estar el robot.

El modelo del robot está compuesto principalmente por:

* el chasis:
```SDF
<link name="chassis">
    <collision>
      <origin xyz="0 0 ${wheelRadius}" rpy="0 0 0"/>
      <geometry>
	<box size="${chassisLength} ${chassisWidth} ${chassisHeight}"/>
      </geometry>
    </collision>

    <visual>
      <origin xyz="0 0 ${wheelRadius}" rpy="0 0 0"/>
      <geometry>
	<box size="${chassisLength} ${chassisWidth} ${chassisHeight}"/>
      </geometry>
      <material name="orange"/>
    </visual>

    <inertial>
      <origin xyz="0 0 ${wheelRadius}" rpy="0 0 0"/>
      <mass value="${chassisMass}"/>
      <box_inertia m="${chassisMass}" x="${chassisLength}" y="${chassisWidth}" z="${chassisHeight}"/>
    </inertial>
  </link>
```
* las ruedas:
```SDF
<link name="caster_wheel">

    <collision>
      <origin xyz="${casterRadius-chassisLength/2} 0 ${casterRadius-chassisHeight+wheelRadius}" rpy="0 0 0"/>
      <geometry>
	<sphere radius="${casterRadius}"/>
      </geometry>
    </collision>
  
    <visual> 
      <origin xyz="${casterRadius-chassisLength/2} 0 ${casterRadius-chassisHeight+wheelRadius}" rpy="0 0 0"/>
      <geometry>
	<sphere radius="${casterRadius}"/>
      </geometry>
    </visual>

    <inertial>
      <origin xyz="${casterRadius-chassisLength/2} 0 ${casterRadius-chassisHeight+wheelRadius}" rpy="0 0 0"/>
      <mass value="${casterMass}"/>
      <sphere_inertia m="${casterMass}" r="${casterRadius}"/>
    </inertial>
  </link>


  <wheel lr="left" tY="-1"/>
  <wheel lr="right" tY="1"/>
```
* y finalmente la cámara montada sobre el chasis:
```SDF
<link name="camera">
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
	<box size="${cameraSize} ${cameraSize} ${cameraSize}"/>
      </geometry>
    </collision>

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
	<box size="${cameraSize} ${cameraSize} ${cameraSize}"/>
      </geometry>
      <material name="blue"/>
    </visual>

    <inertial>
      <mass value="${cameraMass}" />
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <box_inertia m="${cameraMass}" x="${cameraSize}" y="${cameraSize}" z="${cameraSize}" />
    </inertial>
  </link>
```
Teniendo la anterior estructura, es necesario instalar los paquetes de ros_control, con el objetivo de que el robot pueda ser controlado a través de los controladores de ROS. Para instalar dichos paquetes, se ejecuta el siguiente comando:
```bash
sudo apt-get install ros-indigo-ros-control ros-indigo-ros-controllers
```

FInalmente, para mostrar el modelo en Gazebo, se ejecuta el siguiente comando:
```bash
roslaunch mybot_gazebo mybot_world.launch
```
Tras ejecutar el comando, nos debería aparecer el modelo de robot controlado por medio de ROS:
![alt-text](https://drive.google.com/uc?id=0B7qDHl7DSpgQeDlHM2RmR2JiTTQ "Vista Delantera")

![alt-text](https://drive.google.com/uc?id=0B7qDHl7DSpgQdEZKdE1abm5iamM "Vista Trasera")

![alt-text](https://drive.google.com/uc?id=0B7qDHl7DSpgQUEljOHd6YTEtNlk "Vista Lateral")

# Arquitectura del programa

![alt-text](https://drive.google.com/uc?id=0B7qDHl7DSpgQZUJzaWtSQk5WRzQ "Vista Lateral")

Gazebo utiliza una arquitectura de Software de Suscriptor y Publicador. De este modo, y para poder comunicar el robot controlado por medio de ROS en Gazebo con el API, se utilizan los topics proporcionados por ROS, los cuales son: 

- ros.msgs.image: este topic posee la información del sensor de la cámara (imagen).
  Se maneja una estructura de un paquete de mensaje, donde contiene: 
    - Las dimensiones (width y height ) de la imagen.
    - El formato de píxeles que utiliza. 
    - Un arreglo de bytes (Imagen).
- ros.msgs.cmd_vel:  este topic maneja la información de las articulaciones (Joints) que tiene el robot, en         este caso, las ruedas del robot. Se maneja una estructura de un paquete de mensaje, donde se tiene la siguiente información:
    - Nombre.
    - Fuerza, que maneja la unidad de Newton (N).
    - Positión.
    - Eje. 
    - Velocidad.
    - Reset.

La comunicación de Gazebo con la información generada a través de **gzserver** mediante el patrón **Suscriptor / Publicador**, mediante el protocolo **TCP/IP socket**. Permitiendo a **Google Protobufs** realizar la serialización (traducción) de los mensajes entre el suscriptor y el publicador. A la vez, **Boost ASIO** realiza la comunicación entre las capas de **Gazebo** y **Google Protobuts**.
 
#### TECNOLOGÍA UTILIZADA

La comunicación que se realizó con Gazebo, fueron con dos programas en la cual incluía la tecnología de **Trollius**.

**Trollius:** Utiliza una infraestructura para la escritura de un solo código concurrente que usa coroutine, múltiple acceso I/O sobre sockets y otros recursos.

Se utilizó el lenguaje de programación **Python**. Para realizar la comunicación entre los programas y ROS, se utilizó la librería **Pyros**.

**Pyros:** librería que provee API's multiprocesos a ROS junto a Python, manteniéndolos a los dos completamente desacoplados.


# Referencias

[1]: https://www.generationrobots.com/blog/en/2015/02/robotic-simulation-scenarios-with-gazebo-and-ros/ "Robotic SImulation"

1. Generation Robots (2015) "Robotic simulation scenarios with Gazebo and ROS". Recuperado el 11 de Marzo de 2017 desde: https://www.generationrobots.com/blog/en/2015/02/robotic-simulation-scenarios-with-gazebo-and-ros/