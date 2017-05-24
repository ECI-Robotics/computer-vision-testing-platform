import sys
sys.path.append('../')

from camera import VideoCamera
import numpy as np
import trollius
from flask import Flask, Response, request,json
from trollius import From

import cv2
import pygazebo
import pygazebo.msg.image_stamped_pb2
import pygazebo.msg.joint_cmd_pb2




video = VideoCamera()
import multiprocessing
from time import sleep
import logging

logger=multiprocessing.log_to_stderr(logging.DEBUG)

def Move(queue):
    @trollius.coroutine
    def publish_loop():
        manager = yield From(pygazebo.connect())
        b=True
        while(b):
            try:
                if(not(queue.empty())):
                    value=queue.get()
                    if(value.__contains__("name_robot")):
                       name_robot=value["name_robot"]
                       if(value.__contains__("name_right_wheel")):
                           name_right_wheel=value["name_right_wheel"]
                           if(value.__contains__("name_left_wheel")):
                               name_left_wheel=value["name_left_wheel"]
                               b=False
                           else:
                               raise Exception("Solicitud Incompleta falta [name_left_wheel]")
                       else:
                           raise Exception("Solicitud Incompleta falta [name_right_wheel]")

                    else:
                       raise Exception("Ingrese Nombre del Robot en la Solicitud [name_robot]")
            except Exception as error:
                logger.info(error.args)
        print("paso aca")
        name='/gazebo/default/'+name_robot+'/joint_cmd'
        print(name)
        publisher = yield From(
            manager.advertise(name,
                              'gazebo.msgs.JointCmd'))
        message = pygazebo.msg.joint_cmd_pb2.JointCmd()
        message1 = pygazebo.msg.joint_cmd_pb2.JointCmd()
        message1.name = name_robot+'::'+name_right_wheel
        message1.force = 0
        message.name= name_robot+'::'+name_left_wheel
        message.force = 0

        while True:
            if not (queue.empty()):
                n=queue.get()["Instruction"]
            else:
                n="NADA"
            if n!="NADA":
                if(n=="w"):
                    message.force += 0.5
                    message1.force += 0.5
                if(n=="s"):
                    message.force -= 0.5
                    message1.force -= 0.5
                if (n == "a"):
                    message1.force += 0.5
                    message1.force += 0.5
                if (n == "d"):
                    message.force += 0.5
                    message.force += 0.5
                yield From(publisher.publish(message))
                yield From(publisher.publish(message1))
                yield From(trollius.sleep(1.0))
                if(n=="d"):
                    message.force = message.force*-1
                    yield From(publisher.publish(message))
                elif (n=="a"):
                    message1.force = message1.force*-1
                    yield From(publisher.publish(message1))
                else:
                    message.force = message.force * -1
                    message1.force = message1.force * -1
                    yield From(publisher.publish(message1))
                    yield From(publisher.publish(message))
                yield From(trollius.sleep(1.0))
                message.force = 0
                message1.force = 0
                yield From(publisher.publish(message))
                yield From(publisher.publish(message1))
            yield From(trollius.sleep(1.0))

    loop = trollius.get_event_loop()
    loop.run_until_complete(publish_loop())


def gazebo(queue):
    @trollius.coroutine
    def publish_loop():
        manager = yield From(pygazebo.connect())
        def callback(data):
           message = pygazebo.msg.image_stamped_pb2.ImageStamped.FromString(data)
           width = message.image.width
           height = message.image.height
           channels = message.image.pixel_format
           newFileByteArray = bytearray(message.image.data)
           imgx = np.zeros((height, width, channels), dtype=np.uint8)
           p=0
           i=0
           while(i<height):
               k=0
               while(k<width):
                   j=0
                   while(j<channels):
                       imgx[i][k][j]=newFileByteArray[p]
                       p+=1
                       j+=1
                   k+=1
               i+=1
           queue.put(imgx)

        b = True

        while (b):
            try:
                if (not (queue.empty())):
                    value = queue.get()
                    if (value.__contains__("name_robot")):
                        name_robot = value["name_robot"]
                        if (value.__contains__("name_camera")):
                            name_camera = value["name_camera"]
                            if (value.__contains__("name_camera_sensor")):
                                name_camera_sensor = value["name_camera_sensor"]
                                b = False
                            else:
                                raise Exception("Solicitud Incompleta [name_camera_sensor]")
                        else:
                            raise Exception("Solicitud Incompleta [name_camera]")

                    else:
                        raise Exception("Ingrese Nombre del Robot en la Solicitud [name_robot]")
            except Exception as error:
                logger.info(error.args)
        print("Paso ACA1")
        name='/gazebo/default/'+name_robot+'/'+name_camera+'/'+name_camera_sensor+'/image'
        manager.subscribe(name,
                          'gazebo.msgs.ImageStamped',
                          callback)
        while (True):
           yield From(trollius.sleep(0.1))

    logging.basicConfig()
    loop = trollius.get_event_loop()
    loop.run_until_complete(publish_loop())



def Server(queue,queue1,video):
    app = Flask(__name__, static_url_path='')

    @app.route('/NameCamera', methods=['POST'])
    def add_nameCamera():
        content = request.json
        try:
            if (content.__contains__("name_robot")):
                if (content.__contains__("name_camera")):
                    if (content.__contains__("name_camera_sensor")):
                        queue.put(content)
                        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
                    else:
                        raise Exception("Solicitud Incompleta [name_camera_sensor]")
                else:
                    raise Exception("Solicitud Incompleta [name_camera]")

            else:
                raise Exception("Ingrese Nombre del Robot en la Solicitud [name_robot]")
        except Exception as error:
            logger.info(error.args)
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    def gen(video):
        global conta
        while True:
            frame=""
            if(video.isOpen()):
                frame=video.get_frame()
            else:
                if not(queue.empty()):
                    frame = queue.get()

                if (isinstance(frame,np.ndarray)):
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    frame=jpeg.tostring()

                    yield (b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                    sleep(0.1)

    @app.route('/video.mjpg')
    def video_feed():
        return Response(gen(video),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/NameMovement', methods=['POST'])
    def add_nameMovement():
        content = request.json
        try:
            if (content.__contains__("name_robot")):
                if (content.__contains__("name_right_wheel")):
                    if (content.__contains__("name_left_wheel")):
                        queue1.put(content)
                        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
                    else:
                        raise Exception("Solicitud Incompleta falta [name_left_wheel]")
                else:
                    raise Exception("Solicitud Incompleta falta [name_right_wheel]")

            else:
                raise Exception("Ingrese Nombre del Robot en la Solicitud [name_robot]")
        except Exception as error:
            logger.info(error.args)
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    @app.route('/Instruction', methods=['POST'])
    def add_message():
        content = request.json
        queue1.put(content)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    app.run(host="127.0.0.1" , debug=True, port=8080)

queue = multiprocessing.Queue()
queue1 = multiprocessing.Queue()
lock = multiprocessing.Lock()
job3=multiprocessing.Process(target=Server,args=(queue,queue1,video))
job1=multiprocessing.Process(target=gazebo, args=(queue,))
job2=multiprocessing.Process(target=Move, args=(queue1,))
job1.start()
job2.start()
job3.start()