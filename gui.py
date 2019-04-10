from tkinter import Tk, Canvas
from json_network import NetworkInterface
from PIL import Image, ImageTk

window = Tk()
canvas = Canvas(window, width=1500, height=900)
canvas.pack()

canvas.create_rectangle(0, 0, 1, 1, fill='white', outline='white')

canvas.update()

image_robot = Image.open("thumbnail_ugv3_60.png")
photo_robot = ImageTk.PhotoImage(image_robot, master=canvas, width=40, height=40)

image_task = Image.open("thumbnail_goal point.png")
photo_task = ImageTk.PhotoImage(image_task, master=canvas, width=40, height=40)

coordinate = {}
img = {}

network = NetworkInterface(port=12888)
network.initSocket()
network.startReceiveThread()

while True:
    recvData = network.retrieveData()
    if recvData:
        try:
            cor = recvData['data']['coordinate']
            id = recvData['data']['id']
            print(id, end=',', flush=True)

            if not id in coordinate:
                coordinate[id] = cor
                img[id] = canvas.create_image(cor[0], cor[1], image=photo_robot)
                canvas.update()
            else:
                canvas.move(img[id], cor[0]-coordinate[id][0], cor[1]-coordinate[id][1])
                coordinate[id] = cor
                canvas.update()

        except KeyError as error:
            pass
        except TypeError as error:
            pass
        except Exception as e:
            raise e
        else:
            pass

        try:
            task = recvData['data']['new_task']
            cor = recvData['data']['coordinate']
            canvas.create_image(cor[0], cor[1], image=photo_task)

            canvas.update()

        except KeyError as error:
            pass
        except TypeError as error:
            pass
        except Exception as e:
            raise e
        else:
            pass