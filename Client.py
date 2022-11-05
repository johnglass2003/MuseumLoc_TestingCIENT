# echo-client.py

import socket
import sys
import PySimpleGUI as sg
from pynput.mouse import Listener

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

#set layout
layout = [
    [sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), background_color='red', enable_events=True, key='graph')],
    [sg.Text("Hello from PySimpleGUI")], [sg.Button('1', key=lambda: func('Button 1 pressed'))]
]

#create PySimpleGUI window
window = sg.Window("Demo", layout,size=(1250, 750), resizable=True, finalize=True)

#create graph
graph = window['graph']         # type: sg.Graph
#create point in graph
point = graph.draw_point((25, 25), 10, color='green')

#for creating a list of people in museum
#people = 5
#peopleList = []
#for i in range(people):
#    point = graph.draw_point((25, 25), 10, color='green')
#    peopleList.append(point)
# can also use keys and element = window[key] <-- possibly better approach

#test button for pressing
def func(message='Default message'):
    print(message)


#creating socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            event, values = window.read(timeout=10)
            if callable(event):
                event()
            try:
                window.Refresh()
                data = conn.recv(1024)
                if not data:
                    print("stopped")
                    break
                if data:
                    #receieve and parse data
                    data_decoded = data.decode('utf-8')
                    data_decoded = data_decoded.replace('[', '')
                    data_decoded = data_decoded.replace(']', '')
                    print(str(data_decoded))
                    pos = data_decoded.split()
                    #casting to int
                    x = int(pos[0].split('.')[0])
                    y = int(pos[1].split('.')[0])
                    #move point
                    graph.MoveFigure(point, x, y)
                    
            except OSError:
                s.close()
                print('Closed Socket')
                break
