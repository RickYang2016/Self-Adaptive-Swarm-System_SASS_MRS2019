from tkinter import Tk, Canvas
from PIL import Image, ImageTk
import random
import datetime
import time
import ast

# cat *.log | grep coordinate | sort | cut -f2 -d'_' | sed "s/\[Status\]//" > all.log
# for((i=1;i<=20;i++)); do cat *_$i.log | grep coordinate | head -n 1 | cut -f2 -d'{' | cut -f1 -d'}' | sed "s/'coordinate': //" | sed "s/'id': //" | sed "s/, \[/: \[/"; done

window = Tk()
canvas = Canvas(window, width=1500, height=900)
canvas.pack()

canvas.create_rectangle(0, 0, 1, 1, fill='white', outline='white')

canvas.update()

image_robot = [Image.open("../thumbnail_ugv3_60.png"), Image.open("../thumbnail_ugv3_60.png")]
photo_robot = [ImageTk.PhotoImage(image, master=canvas, width=40, height=40) for image in image_robot]

image_task = Image.open("../thumbnail_goal point.png")
photo_task = ImageTk.PhotoImage(image_task, master=canvas, width=40, height=40)

task = [(5, [325, 475]), (30, [1200, 700]), (60, [1075, 175])]

coordinate = {
1: [64.83188736076488, 463.82592193842777],
2: [128.35845667000984, 489.90730011030786],
3: [145.13078469065542, 717.0997798083329],
4: [66.5885394640858, 328.8389982292473],
5: [126.32551542635137, 349.9117611378859],
6: [127.93072501910191, 127.19507481340997],
7: [137.41429215242624, 632.592536619873],
8: [65.91745241345295, 690.7177606982718],
9: [66.9509667017363, 546.4587212409398],
10: [125.91248272662804, 390.8850497057774],
11: [68.11536387712684, 390.8878057697172],
12: [66.50522259306067, 769.8934354253663],
13: [140.95337496892637, 260.96453446177406],
14: [67.86764315479617, 251.62160986972958],
15: [129.97796954774807, 182.40409613879035],
16: [71.33135067098873, 118.53069579682482],
17: [136.72338538660182, 563.3357603951644],
18: [63.978475455057314, 620.3442351085803],
19: [139.31994588870322, 787.4521625466268],
20: [74.4123801851858, 185.4066495743569]}

img = {}

for this_id in coordinate:
    img[this_id] = canvas.create_image(coordinate[this_id][0], coordinate[this_id][1], image=photo_robot[int(random.random()*2)])
    canvas.update()

with open('all.log', 'r') as f:
    time_coordinate = f.readlines()

time_baseline = datetime.datetime.strptime(time_coordinate[0].split('{')[0], '%H:%M:%S.%f')

index = 1

task_index = 0

time_start = time.time()

while True:
    time_1 = datetime.datetime.strptime(time_coordinate[index].split('{')[0], '%H:%M:%S.%f')
    time_elapse = (time_1 - time_baseline).total_seconds() + 5
    if time.time() - time_start >= time_elapse:
        dict_str = time_coordinate[index][time_coordinate[index].index('{'):]
        dict_cor = ast.literal_eval(dict_str)
        this_id = dict_cor['id']
        this_coordinate = dict_cor['coordinate']

        if not this_id in coordinate:
            coordinate[this_id] = this_coordinate
            img[this_id] = canvas.create_image(this_coordinate[0], this_coordinate[1], image=photo_robot[int(random.random()*2)])
            canvas.update()
        else:
            canvas.move(img[this_id], this_coordinate[0]-coordinate[this_id][0], this_coordinate[1]-coordinate[this_id][1])
            coordinate[this_id] = this_coordinate
            canvas.update()

        if index < len(time_coordinate) - 1:
            index = index + 1

    if task_index < len(task) and time.time() - time_start >= task[task_index][0] - 2.5:
        canvas.create_image(task[task_index][1][0], task[task_index][1][1], image=photo_task)
        canvas.update()
        task_index = task_index + 1
