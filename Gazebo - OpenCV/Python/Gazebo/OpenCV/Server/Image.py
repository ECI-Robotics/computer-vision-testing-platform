import numpy as np
import trollius
from flask import Flask, Response, request,json
from trollius import From
import sys
sys.path.append('../')

import cv2
import pygazebo
import pygazebo.msg.image_stamped_pb2
from Models.camera import VideoCamera

video = VideoCamera()
import multiprocessing
from time import sleep
import logging

logger=multiprocessing.log_to_stderr(logging.DEBUG)


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
           if(queue.full()):
               queue.get()
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

        name='/gazebo/default/'+name_robot+'/'+name_camera+'/'+name_camera_sensor+'/image'
        manager.subscribe(name,
                          'gazebo.msgs.ImageStamped',
                          callback)
        while (True):
           yield From(trollius.sleep(0.1))

    logging.basicConfig()
    loop = trollius.get_event_loop()
    loop.run_until_complete(publish_loop())



def Server(queue,video):
    app = Flask(__name__, static_url_path='')

    @app.route('/NameCamera', methods=['POST'])
    def add_name():
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

    app.run(host="127.0.0.1" , port=8081)

queue = multiprocessing.Queue(15)
lock = multiprocessing.Lock()
job1=multiprocessing.Process(target=gazebo, args=(queue,))
job2=multiprocessing.Process(target=Server,args=(queue,video))
job1.start()
job2.start()

# Wait for the worker to finish
job1.join()
job2.join()


#<update_rate>1</update_rate>