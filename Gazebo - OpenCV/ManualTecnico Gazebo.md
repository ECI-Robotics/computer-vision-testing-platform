# Manual Técnico Gazebo - OpenCv 

### INTRODUCCIÓN

Se explicará los procedimientos de instalación y la configuración que se obtuvo en el proyecto.

El proyecto consta de dos programas que realiza la conexión entre Gazebo y un Algoritmo de Visión Artificial.

El programa RobotSimCvImage, es el encargado de realizar una conexión a Gazebo a través de una subscripción a un topic que dispone, para adquirir las imágenes de la cámara del robot.

El programa RobotSimCvMove, es el encargado de realizar una conexión a Gazebo como un publicador, enviando información al topic que disponible, para poder aplicarle física al robot para su movimiento.

El proyecto fue realizado en el Sistema Operativo Ubuntu 14.04, Python 2.7, OpenCv 3.0 y Gazebo7.

### INSTALACIÓN GAZEBO

Actualmente Gazebo es utilizado para simulación en la parte robótica, su versión más reciente es la 8.0 que está disponible para Ubuntu 16.

Gazebo tiene diferentes repositorios en Ubuntu donde se puede localizar la versión del simulador para la versión del sistema Operativo que se está trabajando.

Para Ubuntu 14.04 Gazebo tiene disponible la versión 7.0, el cual, fue el utilizado para el desarrollo de este proyecto.

Su instalación es muy fácil, ya que se dispone del repositorio en Ubuntu 14.04.

El paso a paso de la instalación es:

- Se abre la terminal de Ubuntu y se ingresa los siguientes comandos.
```{r, engine='bash', count_lines } 
     $sudo apt-get update
     $sudo apt-get install gazebo7
```
##### Recomendación: 
Gazebo requiere para su buen funcionamiento, una Tarjeta gráfica aceleradora 3D con OpenGL, para realizar diversas tareas de representación y simulación de imágenes correctamente. Pero no es necesario para su instalación y funcionamiento.


En este proyecto se utilizó:
- NVIDIA NVS 310 con 2 GB
- 12 GB de RAM.
- Intel coreI7


### INSTALACIÓN OPENCV EN UBUNTU CON PYTHON.

OpenCV es una librería de código abierto para C/C++. Con él se realiza procesamiento de imágenes y visión computarizada.

La versión más reciente que se tiene es la 3.2-Dev.

En el proyecto se trabajó la versión 3.0 por su compatibilidad con Python 2.7.

Python 2.7 ya viene instalado en el Sistema Operativo Ubuntu 14.04

Para iniciar la instalación de OpenCv, debemos de actualizar e instalar los paquetes preinstalados en el sistema Ubuntu 14.04.

```sh, count_lines 
 $ sudo apt-get update
 $ sudo apt-get upgrade
```
Se debe instalar las herramientas para desarrolladores, para instalar el código fuente de OpenCV
```{r, engine='bash', count_lines } 
$ sudo apt-get install build-essential cmake git pkg-config
```

Se debe instalar algunas librerías para que OpenCV pueda cargar varios formatos de archivo de imagen (JPEG, PNG, TIFF, etc.…) 
```{r, engine='bash', count_lines } 
$ sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
```

Para mostrar la imagen que OpenCv carga mediante una interfaz (GUI) se instala la librería GTK.
```{r, engine='bash', count_lines } 
$ sudo apt-get install libgtk2.0-dev
```

Se debe instalar las siguientes librerías para el flujo de videos y poder acceder individualmente a las imágenes para su análisis.
```{r, engine='bash', count_lines } 
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
```

Y, por último, se necesitará optimizar algunos detalles dentro de OpenCV, con librerías que lo permite.
```{r, engine='bash', count_lines } 
$ sudo apt-get install libatlas-base-dev gfortran
```

Se requiere un gestor de descarga y de instalación de paquetes de Python, para poder gestionar los requerimientos para utilizar OpenCV con Python.

El gestor oficial de descargas de librerías de Python es pip, se procede a descargarlos de la página oficial de PIP e instalarlo de la siguiente manera.

```{r, engine='bash', count_lines } 
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo Python get-pip.py
```

Para trabajar en Python y que se pueda crear ambientes separados y poderse manejar de una buena manera sin crear conflicto alguno. Se instala dos librerías de Python, virtualenv y virtualenvwrapper.

```{r, engine='bash', count_lines } 
$ sudo pip install virtualenv virtualenvwrapper
```

Se borra los residuos de pip para no generar inconvenientes.

```{r, engine='bash', count_lines } 
$ sudo rm -rf ~/.cache/pip
```

Ahora se debe de actualizar nuestro archivo “ ~ / . bashrc ” , que se encuentra en la raíz principal. Se modificará el archivo, por eso se revisa los permisos que se tiene.
```{r, engine='bash', count_lines } 
$ ls –la ~/ | more
```

En dado caso que tengas los permisos de escribir, se abre el archivo con su editor de texto favorito y al final del archivo se pegar y se guardar la siguiente información.
```{r, engine='bash', count_lines } 
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Esto nos asegura que se cargue la librería.

Para que surja efecto, cierra y vuelva abrir la terminal.

Se crear el entorno para trabajar nuestro cv. 
```{r, engine='bash', count_lines } 
$ mkvirtualenv cv
```

Vamos a trabajar con Python, debemos de instalarlo o actualizarlo si ya está instalado.
```{r, engine='bash', count_lines } 
$ sudo apt-get install python2.7-dev
```

Como las imágenes son representadas como matrices multidimensionales, necesitaríamos instalar de NumPy para poderlas trabajar.
```{r, engine='bash', count_lines } 
$ pip install numpy
```

Con esto se complementó las instalaciones de paquetes necesarios para completar nuestra instalación de OpenCV con Python.

Ahora descargaremos mediante GitHub el código fuente libre de OpenCV, guardándose en la raíz principal.
```{r, engine='bash', count_lines } 
$ cd ~
$ git clone https://github.com/Itseez/opencv.git
$ cd opencv
$ git checkout 3.0.0
```
Se descarga el OpenCV contrib, la versión con la cual podemos cargar todas las características de OpenCV 3.0 y no tener problemas en la instalación.
```{r, engine='bash', count_lines } 
$ cd ~
$ git clone https://github.com/Itseez/opencv_contrib.git
$ cd opencv_contrib
$ git checkout 3.0.0
```

Se construye la manera como se debe de instalar OpenCV.
```{r, engine='bash', count_lines } 
$ cd ~/opencv
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D BUILD_EXAMPLES=ON ..
```
###### Importante: Incluir los dos puntos en la configuración.

Se procede a Compilar OpenCV.
```{r, engine='bash', count_lines } 
$ make -j4
```
El numero significa los núcleos disponibles en su procesador.

Si todo ha salido sin errores, se procede la instalación en el sistema Ubuntu.
```{r, engine='bash', count_lines } 
$ sudo make install
$ sudo ldconfig
```

Finalizado todo, podemos confirmar si se instaló bien OpenCV.
```{r, engine='bash', count_lines } 
$ workon cv
$ python
```
```{r, engine='python', count_lines } 
>>> import cv2
>>> cv2.__version__
'3.0.0'
```
En dado caso que aparezca un error al importar el archivo OpenCV (cv2.so), buscar el archivo. 
En este caso estuvo ubicado en:

/usr/local/lib/python2.7/site-packages/cv2.so

Y procede de la siguiente manera:
```{r, engine='python', count_lines } 
>>>import sys 
>>>sys.path.append('/usr/local/lib/python2.7/site-packages')
>>> import cv2
>>> cv2.__version__
'3.0.0'
```

### CREACIÓN DEL ROBOT PARA GAZEBO

La creación de modelos de robots, en Gazebo (sin utilizar ROS), no se puede hacer directamente por medio del programa Gazebo, por lo que se debe tener creatividad, ya que Gazebo sólo permite implementar formas básicas, como una esfera, un cilindro y un cubo, los cuales sirven para darle un “cuerpo” al robot. La idea es utilizar estos objetos y construir un robot.

Inicialmente, para saber qué tanto tiene que implementar, se debe tener muy bien la idea y el boceto de un robot sencillo, para proceder a crearlo.

###### Boceto Final:
De Frente

![alt text](https://drive.google.com/uc?id=0B9eych6A6_6QQ2puRE9aNmc1OUU)

De Lado

![alt text](https://drive.google.com/uc?id=0B9eych6A6_6QVk0wTGMzcXR6WWs)

De Atrás

![alt text](https://drive.google.com/uc?id=0B9eych6A6_6QekxoYS1oS1gyZVE)

En esta ocasión, se creará un robot que tendrá una caja, la cual servirá de cuerpo al robot; otra caja, que será la cámara; unas esferas para el caster y 2 cilindros para las ruedas.

El formato de creación de los objetos, se hace mediante etiquetas, bajo especificaciones de las extensiones SDF.

El documento SDF, se puede realizar en un bloc de notas, o en un editor de código. Lo importante, es la estructura y los nombres de las etiquetas.

La estructura inicial para la creación de un robot, es la siguiente:

```{r, engine='bash', count_lines } 
<?xml version="1.0" ?>
<sdf version="1.4">
	<model name="my_robot">
	<static>false</static>
```

Se declara las etiquetas XML y la versión del formato SDF a utilizar. 
La etiqueta “model” indicará la realización de un robot o cualquier objeto que se realice y se nombra; en este caso “my robot”. La etiqueta “static” es usada para referenciar si el objeto a crearse se moverá en el ambiente (false) o se quedara detenido (true).

Gazebo, utiliza dos partes, para simular un objeto:
- La primera parte se compone de las leyes de física, como su posicionamiento, sus colisiones, fricciones, etc.
- La segunda parte se compone de los elementos gráficos del objeto.

En este ejemplo, mostraremos algunos elementos utilizados, con su física y su parte visual:
```{r, engine='bash', count_lines } 
<link name="chassis">
		<pose>0 0 .1 0 0 0</pose>
		<collision name="collision">
			<geometry>
				<box>
					<size>.4 .2 .1</size>
				</box>
			</geometry>
		</collision>
		
		<visual name ="visual">
			<geometry>
				<box>
					<size>.4 .2 .1</size>
				</box>
			</geometry>
		</visual>
```

Se realiza, la primera caja, que sería el “chassis”. Se utiliza la etiqueta link, para declarar las propiedades físicas y visuales del modelo. “Pose” es la declaración de la posición (x,y,x) y su orientación (roll, pitch, yaw), según el marco de referencia, y debe estar incluida en la etiqueta link. La etiqueta “collision” hace referencia a las propiedades de colisiones de un objeto. En este caso, estamos declarando la de una figura geométrica por medio de la etiqueta “geometry”, que sería la caja (en este caso, “box”), dentro de la cual se declaran las dimensiones del tamaño, por medio de la etiqueta “size”, en las posiciones (x,y,z).
El objeto geométrico creado anteriormente se ubica dentro de la etiqueta “visual”, para representar el mismo objeto visualmente.

Para la parte del caster, que va incluido en el “chassis” para su movimiento, se utiliza una esfera:
```
        <collision name="caster_collision">
			<pose>-0.15 0 -0.05 0 0 0</pose>
			<geometry>
				<sphere>
					<radius>.05</radius>
				</sphere>
			</geometry>
			
			<surface>
				<friction>
					<ode>
						<mu>0</mu>
						<mu2>0</mu2>
						<slip1>1.0</slip1>
						<slip2>1.0</slip2>
					</ode>
				</friction>	
			</surface>
		</collision>
```


Se ubica primero el objeto, en una parte central del chassis, y se trae la figura geométrica de la esfera, declarando el radio que se va a utilizar. Cuando se trata de una esfera, se declaran algunas propiedades de la superficie, por medio de la etiqueta “surface”; en este caso, se declaró la parte de fricción en la etiqueta “friction”, para declarar los valores de la torsión (dentro de la etiqueta “ode”), lo cuales son la fuerza del deslizamiento, y la fuerza de la fricción; estos valores se dan entre el rango [0..1] (para la fuerza de deslizamiento por medio de la etiqueta “slip”) y el coeficiente de fricción en el rango de [0..1] (por medio de la etiqueta “mu”).

En la parte visual, solamente se declara el objeto geométrico con su respectivo radio y posición dentro del “chassis”:

```
        <visual name="caster_visual">
			<pose>-0.15 0 -0.05 0 0 0</pose>
			<geometry>
				<sphere>
					<radius>.05</radius>
				</sphere>
			</geometry>
		</visual>
</link>	
```

Se cierra ese objeto, indicando que se finaliza su construcción.

La parte de las ruedas, se crearon con cilindros de la siguiente manera:

```
<link name="left_wheel">
		<pose>0.1 0.13 0.1 0 1.5707 1.5707</pose>
		<collision name="collision">
			<geometry>
				<cylinder>
					<radius>.1</radius>
					<length>.05</length>
				</cylinder>
			</geometry>
		</collision>
		
		<visual name="visual">
			<geometry>
				<cylinder>
					<radius>.1</radius>
					<length>.05</length>
				</cylinder>
			</geometry>
		</visual>
	</link>
```

Se referencia la creación de un objeto por medio de la etiqueta “link”, que será, en este caso, la rueda izquierda. Se le asigna la posición donde estará ubicada la rueda, y se le asignan las propiedades de colisión, declarando un objeto geométrico, en este caso un cilindro, para el cual se solicitan los datos de la magnitud del radio y el ancho. En la parte visual se declaran las mismas propiedades del objeto, para su visualización.

Para el caso de la rueda derecha, se declaran los mismos valores de la anterior rueda, pero la única diferencia, es ponerla al otro costado, modificando los valores de la posición (xyz).
```
	<link name="right_wheel">
		<pose>0.1 -0.13 0.1 0 1.5707 1.5707</pose>
		<collision name="collision">
			<geometry>
				<cylinder>
					<radius>.1</radius>
					<length>.05</length>
				</cylinder>
			</geometry>
		</collision>
		
		<visual name="visual">
			<geometry>
				<cylinder>
					<radius>.1</radius>
					<length>.05</length>
				</cylinder>
			</geometry>
		</visual>
	</link>
```

Y por último se crea la cámara. En este caso, se utilizó una caja con una declaración de masa:

```
<link name="camera">
		<pose>0 0 .2 0 0 0</pose>
		<inertial>
        		<mass>0.1</mass>
      		</inertial>
		<collision name="camera_collision">
		        <geometry>
			        <box>
				        <size>0.1 0.1 0.1</size>
			          </box>
		        </geometry>
		</collision>
		<visual name="camera_visual">
		        <geometry>
			          <box>
            				<size>0.1 0.1 0.1</size>
			          </box>
		        </geometry>
		</visual>
```

Se declaró la posición (encima del chasis), una masa y sus propiedades físicas y visuales.

Gazebo, cuando se trata de realizar la captura de alguna información, maneja sensores, los cuales existen de una gran variedad, sensores de ruido, buscadores de rayos láser, cámaras en 2D y 3D, sensores estilo Kinect, sensores de contacto, entre muchos más. 

En esta ocasión, se utilizó un sensor de cámara:
```
        <sensor name="camera" type="camera">
			<always_on>1</always_on>
		        <update_rate>10</update_rate>
		        <visualize>false</visualize>
			<camera>
	                    <horizontal_fov>1.047</horizontal_fov>
			       <image>
			            <width>640</width>
			            <height>480</height>
			       </image>
		              <clip>
			            <near>0.1</near>
		        	    <far>100</far>
			      </clip>
		        </camera>
	     </sensor>
</link>
```

Se declara que se utilizará un sensor, dentro del objeto que se está formando, y se especifica el tipo “type”, en este caso “camera”.

Las propiedades del sensor se dividen en dos partes:
##### - Propiedades propias de todo sensor:
 
- “Always on”, si es true (1), el sensor se actualizará según la velocidad definida en la toma de información.
- “update rate”, define la frecuencia de la generación, o toma de los datos.}
- “Visualize”, si es true, la información del sensor, será visualizada en el ambiente.

##### - Las propiedades del tipo especificado del sensor:
  - “camera”: declara las propiedades de la cámara.
  - “Horizontal fov”: se declara el campo horizontal por ver.
  - “image”: declara el alto y el ancho de la imagen a generar.
  - “clip”: se declara los “near” y “far”, que utilizara la cámara.
 
Después de realizar todo el cuerpo del robot, solamente falta unir las partes del mismo, para lo cual se requiere utilizar la etiqueta “joint”:
```
<joint type="revolute" name="camera">
		<pose>0 0 0.3 0 0 0</pose>
		<child>camera</child>
		<parent>chassis</parent>
		<axis>
			<xyz>0 1 0</xyz>
		</axis>
</joint>
```
La declaración de una etiqueta “joint”, se realiza indicando el tipo de unión. Existen 5 tipos, los cuales generalmente son para movimientos. En este caso, se utilizó el tipo “revolute”, la cual permite realizar un giro sobre un eje fijo. Se determina la posición donde se dará la unión, por medio de la etiqueta “pose”; La etiqueta “child” se determina el “link” a unir y la etiqueta “parent” permite identificar qué objeto es el principal para unir.

la Etiqueta “axis”, determinará cual eje se activará para realizar su propia rotación.

Se realiza las uniones de las ruedas con el chasis del robot movible.
```
<joint type="revolute" name="left_wheel_hinger">
		<pose>0 0 0.03 0 0 0</pose>
		<child>left_wheel</child>
		<parent>chassis</parent>
		<axis>
			<xyz>0 1 0</xyz>
		</axis>
</joint>

<joint type="revolute" name="right_wheel_hinger">
		<pose>0 0 0.03 0 0 0</pose>
		<child>right_wheel</child>
		<parent>chassis</parent>
		<axis>
			<xyz>0 1 0</xyz>
		</axis>
</joint>
```

Es importante realizar el cierre de todo, en especial del modelo y de la extensión del documento.
```
	</model>
</sdf>
```

Se debe de ubicar la carpeta .gazebo/models, se crea una nueva carpeta, con el nombre del modelo del Robot.

Se crea un archivo con la extensión .config para detectar la configuración del modelo del Robot.

El archivo contendrá un modelo de etiquetas XML como el siguiente.

```
<?xml version="1.0" ?>
<model>
	<name>Nombre_Robot </name>
	<version>1.0</version>
	<sdf version="1.4"> Archivo_Diseño_Robot.sdf</sdf>
	<author>
		<name>Nombre_Autor</name>
		<email>email_Autor@Mail.com</email>
	</author>

	<description>
		Descripción del robot
	</description>
</model>

```

En la estructura debe de incluir el nombre del modelo, la estructura del diseño del robot creado y con la version del SDF utilizado.

Opcionalmente, le solicita la información del autor y la descripción del modelo del robot.

Finalmente, al abrir **Gazebo**, podrá encontrar en el listado de los modelos de **Gazebo** donde se encontrar el Robot.



### CREACION DE ESCENARIOS PARA GAZEBO

El escenario que se creó para el proyecto, se divide en dos partes: 
- Se realizó mediante el programa de Blender. Un escenario de Mallas donde se puede Terrenos.
- Los Obstáculos con los elementos geométricos que está en **Gazebo**

El escenario se crea mediante un archivo .word con una estructura de etiquetas SDF, es necesariamente que el escenario hecho en Blender sea exportada en formato .DAE, para que **Gazebo** la pueda reconocerlo.

Inicialmente el archivo debe de contener la siguiente cabecera.

```
<?xml version="1.0"?>
<sdf version="1.4">
  <world name="default">
```

Con la información que se creara un archivo XML, junto con la estructura de etiquetas SDF y se nombra el escenario "Word" que se va a construir.

Para incluir modelos se realiza con la etiqueta "include". En el proyecto el escenario incluyo el "planeta" que tiene **Gazebo**, el robot en una posición del escenario y el Sol que incluye **Gazebo**.

```
 <include>
      <uri>model://ground_plane</uri>
    </include>
	<include>
		<pose>-1.809116 4.699705 0.013797 .0 .0 .0</pose>
	      <uri>model://Robot</uri>
	</include>
    <include>
      <uri>model://sun</uri>
    </include>

```

Para construir elementos dentro del escenario, donde se tendrá física y algunas especificaciones, se debe de crear un modelo sobre los elementos que estarán. 

En el proyecto, se introdujo el escenario de Mallas de un terreno y una caja.

El modelo inicia con la etiqueta "model".

```
<model name="my_mesh">
      <pose>0 0 0  0 0 0</pose>
      <static>true</static>
```

La debe de identificar el modelo y ubicarlo dentro del escenario. Además, especificar si el modelo estará "quieto" dentro de la simulación.

Se procede dentro de la estructura del modelo, con los "link" que son construcciones de elementos dentro del elemento. 

dentro de un link, se podrá crear un elemento con las herramientas que trae **Gazebo** o se puede importar algunos elementos.

Dentro del proyecto se importó el escenario de mallas, un terreno realizado previamente en Blende y exportando en formato .DAE

```
<link name="body">
    	<collision name="geom">
          <geometry>
            <mesh><uri>file://pasto1.dae</uri></mesh>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <mesh><uri>file://pasto1.dae</uri></mesh>
          </geometry>
        </visual>
</link>
```

Dentro del elemento que se va a importar, se le puede dar la opción de que el terreno tenga implementadas las leyes de físicas, en dado caso, se especifica en la etiqueta “Collision"", que **Gazebo** lo interpreta como un elemento que contendrá elementos de física. Las mallas son figuras formadas por triángulos geométricos, permitiendo que **Gazebo** las interprete dentro de la etiqueta "Geometry"->"Mesh", y se dará la ubicación donde se encuentre el archivo .DAE del escenario de Mallas.

Para que el elemento sea visible dentro del escenario. se utiliza la etiqueta "visual" e incluyendo la misma información de la etiqueta "collision", para que se tenga una relación entre lo visual y la parte de leyes de física.

En la creación de los demás elementos, se utiliza igualmente, como se realizó en la estructura del Robot. 

Se realiza mediante la etiqueta "link".
```
<link name="Box1">
		<pose>1.788620 5.703180 0.523794 .0 .0 .0</pose>
		<inertial>
        		<mass>0.1</mass>
      		</inertial>
		<collision name="Box1_collision">
		        <geometry>
			        <box>
				        <size>1 1 1</size>
			          </box>
		        </geometry>
		</collision>
		<visual name="Box1_visual">
		        <geometry>
			          <box>
            				<size>1 1 1</size>
			          </box>
		        </geometry>
		</visual>
</link>
```

Se especifica el nombre del elemento que se va a crear y la posición donde se ubicara con la etiqueta "pose".

Se especificará dentro de la etiqueta "inertia" algunas características internas del elemento, en el ejemplo, se especifica la masa que tendrá el elemento dentro de la etiqueta "mass".

Se especifica la parte de la física que contendrá el elemento, en la etiqueta "collision". en el ejemplo, se hace referencia a crear una figura geométrica, de una caja, con las etiquetas "geometry"->"box", y se dará la especificación, de sus dimensiones en X, Y y Z.

Por la parte visual del elemento. se realiza mediante la etiqueta "visual", copiando la misma información de la parte de las leyes de física, para que se pueda tener una relación entre la física y lo visual.

Para finalizar el documento, se cierra las etiquetas iniciales.
```
    </model>
  </world>
</sdf>

```

Para ver que el escenario se construyó bien, en la terminal de Ubuntu debe de correr **Gazebo** y pasarle como parámetro el nombre del archivo que contiene el escenario creado anteriormente.

```sh
 $Gazebo Nombre_escenario.world
```

Escenario 

![alt text](https://drive.google.com/uc?id=0B9eych6A6_6QQVVOXzRDN00yVXM) 

### ARQUITECTURA DEL PROGRAMA

![alt text](https://drive.google.com/uc?id=0B9eych6A6_6QZnBWNmM2anQ5bjA)

Gazebo utiliza una arquitectura de Software de Suscriptor y Publicador. Utilizando Topics generados por el modelo simulado:

Los topics que se requirió en el proyecto, fueron: 

- ImageStamped: De este topic, posee la información del sensor de la cámara (imagen).
  Se maneja una estructura de un paquete de mensaje, donde contiene: 
    - Las dimensiones (width y height ) de la imagen.
    - El formato de píxeles que utiliza. 
    - Un arreglo de bytes (Imagen).
- JointCmd: Se maneja la información de las articulaciones (Joints) que tiene el robot, en         este caso, la rueda del robot. Se maneja una estructura de un paquete de mensaje, donde     contiene la siguiente información:
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

Se utilizó el lenguaje de programación **Python**. Para realizar la comunicación entre los programas y Gazebo, se utilizó la librería de **Pygazebo**.

**Pygazebo:** contiene la estructura de mensajes que se requiere para realizar la comunicación con Gazebo Topic y la tecnología de Google Protobuts

#### CONEXIÓN

##### CV-RobotSim-Suscriptor

Al iniciarse el programa, se crea un API server que corre localmente por el puerto 8081, realizando la comunicación a un Cliente que va a consumir el servició de las imágenes que se genera en el simulador **Gazebo** o de una cámara que se encuentre conectada.

El API server, ofrece los servicios de:

- Recibimiento de la información del robot del que se requiera sacar las imágenes. La información que recibe debe seguir el siguiente estándar:
    - Se recibirá las peticiones en el formato JSON.
    - El JSON debe de tener las variables y la información de cada uno: 
        - "name_robot": El nombre del robot.
        - "name_camera": El nombre de la forma de la cámara.
        - "name_camera_sensor": El nombre del sensor que tiene la forma dela cámara.
    - Las peticiones deben ser mediante POST 
    - El Path donde deben de enviar las peticiones es: /NameCamera.
    
- Salida de imágenes del simulador **Gazebo** o de una, que utiliza el siguiente estándar:
    - La información de la imagen tiene el encabezado de:
        ```
        b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n
	```
- Se recibe peticiones mediante GET.
- El Path donde deben de enviar las peticiones es: /video.mjpg.

También, el programa se subscribe al tópico que maneja las imágenes, extrayendo la información, mediante paquetes que **Gazebo** envía cada segundo que genera una nueva imagen. 

Cada vez que llegue un nuevo paquete, se construye la imagen según la información del paquete.

El paquete que envía Gazebo trae un arreglo de bytes en formato String. El programa convierte mediante la librería numpy a un arreglo de bytes.

Se crea una nueva imagen vacía con las dimensiones y el formato RGB de la imagen que se quiere construir, mediante **OpenCv**.

Se utiliza el arreglo de bytes para poner cada byte en la imagen vacía. Acabo el proceso de construcción, se ingresa a una estructura de datos de una Cola.

Cada vez que un cliente se conecte al API Server, va consumiendo las imágenes que el API Server va sacando de la estructura de datos de una Cola.


##### CV-RobotSim-Publicador:

Al iniciarse el programa, se crea un API server que corre localmente por el puerto 8080, realizando la comunicación a un Cliente que va a enviar información al simulador **Gazebo**. 

El API server ofrece los siguientes servicios:

- Recibimiento de la información del robot y las llantas que se desean mover. La información que recibe debe cumplir el siguiente estándar:
    - Se recibirá las peticiones en el formato JSON.
    - El JSON debe de contener las variables y la información de cada uno:
        - "name_robot": El nombre del robot que desea mover.
        - "name_right_wheels": Un arreglo de las llantas de la parte Derecha.
        - "name_left_wheels": Un arreglo de las llantas de la parte Izquierda.
    - Las peticiones debe ser mediante POST.
    - El Path donde deben de enviar las peticiones es: /NameMovement.
- Recibimiento de instrucciones de movimientos, La información que se recibe debe cumplir con el siguiente estándar:
    - Se recibirá las peticiones en el formato JSON.
    - El JSON debe de contener la "Instruction".
    - En la variable "Instruction" debe de contener alguna de las siguientes letras: 
        - "w": Si desea que se mueva hacia adelante.
        - "a": Si desea que se mueva hacia la Izquierda.
        - "d": Si desea que se mueva hacia la Derecha.
        - "s": Si desea que se mueva hacia Atrás.
    - Las peticiones deben ser mediante POST.
    - El Path donde deben de enviar las peticiones es: /Instruction.
 
También, el programa se anuncia como un publicador para que **Gazebo** pueda reconocer las peticiones que se le enviará. Cada petición será de mover las articulaciones de cada llanta que tiene el robot.

Al recibir mediante el API server una petición de movimiento es introducida a una estructura de datos de una Cola. 

El publicador, estará constantemente revisando la información de la Cola. Cuando se encuentre una petición la procesa e invoca las llantas que se deban mover. 

Cada llanta recibe una información sobre la fuerza que se le va aplicar, el programa, aplicar la fuerza de 1.0 Newton (N) hacia adelante y 2.0 Newton hacia atrás y los lados.

Gracias a la librería PyGazebo, los paquetes de mensajes esta ya predefinidos, simplemente se llena las variables mencionadas anteriormente (Robot, Llantas y Fuerza) y se realiza el envió al topic donde puede publicar.

### RESULTADOS:

### BIBLIOGRAFIA
