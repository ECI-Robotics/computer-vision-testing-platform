import trollius
from trollius import From
from flask import Flask, render_template, Response, send_from_directory, request, json
import pygazebo
import pygazebo.msg.joint_cmd_pb2
import multiprocessing
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
                       if(value.__contains__("name_right_wheels")):
                           name_right_wheels=value["name_right_wheels"]
                           if (value.__contains__("name_left_wheels")):
                               name_left_wheels = value["name_left_wheels"]
                               b=False
                           else:
                               raise Exception("Solicitud Incompleta falta [name_left_wheels]")

                       else:
                           raise Exception("Solicitud Incompleta falta [name_right_wheels]")

                    else:
                       raise Exception("Ingrese Nombre del Robot en la Solicitud [name_robot]")
            except Exception as error:
                logger.info(error.args)

        name='/gazebo/default/'+name_robot+'/joint_cmd'
        publisher = yield From(
            manager.advertise(name,
                              'gazebo.msgs.JointCmd'))
        wheels=[]
        wheelR=[]
        wheelL=[]
        i=0
        b=True
        max= len(name_right_wheels)
        wheel=name_right_wheels
        while (i<max):
            print(i,max)
            message=pygazebo.msg.joint_cmd_pb2.JointCmd()
            message.name = name_robot + '::' + wheel[i]
            message.force = 0
            wheels.append(message)
            i += 1
            if(i>=max and b):
                wheelR=wheels
                wheels=[]
                b=False
                i=0
                max=len(name_left_wheels)
                wheel=name_left_wheels
        wheelL=wheels

        while True:
            if not (queue.empty()):
                n=queue.get()["Instruction"]
            else:
                n="NADA"
            print(n)
            if n!="NADA":
                if(n=="w"):
                    for message,message1 in zip(wheelR,wheelL):
                        message.force += 1
                        message1.force += 1
                        yield From(publisher.publish(message))
                        yield From(publisher.publish(message1))
                if(n=="s"):
                    for message, message1 in zip(wheelR, wheelL):
                        message.force -= 2
                        message1.force -= 2
                        yield From(publisher.publish(message))
                        yield From(publisher.publish(message1))

                if (n == "a"):
                    for message1 in wheelR:
                        message1.force += 2
                        yield From(publisher.publish(message1))

                if (n == "d"):
                    for message in wheelL:
                        message.force += 2
                        yield From(publisher.publish(message))

                yield From(trollius.sleep(1.0))

                if(n=="d"):
                    for message in wheelL:
                        message.force = message.force*-1
                        yield From(publisher.publish(message))
                elif (n=="a"):
                    for message1 in wheelR:
                        message1.force = message1.force*-1
                        yield From(publisher.publish(message1))
                else:
                    for message, message1 in zip(wheelR, wheelL):
                        message.force *=-1
                        message1.force *=-1
                        yield From(publisher.publish(message))
                        yield From(publisher.publish(message1))


                yield From(trollius.sleep(1.0))
                for message in wheelR:
                    message.force = 0
                for message1 in wheelL:
                    message1.force = 0
                for message in wheelR:
                    yield From(publisher.publish(message))
                for message1 in wheelL:
                    yield From(publisher.publish(message1))

            yield From(trollius.sleep(1.0))

    loop = trollius.get_event_loop()
    loop.run_until_complete(publish_loop())

def Server(queue):
    app = Flask(__name__, static_url_path='')

    @app.route('/NameMovement', methods=['POST'])
    def add_name():
        value = request.json
        try:
            if(value.__contains__("name_robot")):
               if(value.__contains__("name_right_wheels")):
                   if (value.__contains__("name_left_wheels")):
                       queue.put(value)
                       return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
                   else:
                       raise Exception("Solicitud Incompleta falta [name_left_wheels]")

               else:
                   raise Exception("Solicitud Incompleta falta [name_right_wheels]")

            else:
               raise Exception("Ingrese Nombre del Robot en la Solicitud [name_robot]")
        except Exception as error:
            logger.info(error.args)
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


    @app.route('/Instruction', methods=['POST'])
    def add_message():
        content = request.json
        queue.put(content)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


    app.run(host="127.0.0.1" ,debug=True, port=8080)

queue = multiprocessing.Queue()
job1=multiprocessing.Process(target=Move, args=(queue,))
job2=multiprocessing.Process(target=Server,args=(queue,))
job1.start()
job2.start()

job1.join()
job2.join()