import socket
import sys
import paramiko
import PySimpleGUI as sg


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

#SSH sending information
host = "127.0.0.1"   #server host
username = "jason"     #username
password = "xxxx"      #password
port = "22"            #port

#test button for pressing
def func(message='Default message'):
    print(message)

#function for pairing audio file and exhibit upon button press
def pair(audFile, exh):
    #client = paramiko.client.SSHClient()
    #client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect(host, username=username, password=password,port=port)
    #_stdin, _stdout, _stderr = client.exec_command('python hello.py')
    #print(_stdout.read().decode())
    #client.close()
    print("Attempted to pair " + audFile + " " + exh)

#creating socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        #audio files list
        audioFiles = []
        exhibits = []

        print(f"Connected by {addr}")

        #recieve, decode and add audio files and exhibits from server into list
        data = conn.recv(1024)
        data_decoded = data.decode('utf-8')
        data_decoded = data_decoded.replace('[', '')
        data_decoded = data_decoded.replace(']', '')
        data_decoded = data_decoded.replace(',', '')
        data_decoded = data_decoded.replace('\'', '')
        lists = data_decoded.split("^")
        pos1 = lists[0].split()
        pos2 = lists[1].split()
        for p1 in pos1:
            audioFiles.append(p1)
        for p2 in pos2:
            exhibits.append(p2)

        #set layout
        layout = [
            [sg.Graph(canvas_size=(1000, 500), graph_bottom_left=(0, 0), graph_top_right=(400, 400), background_color='grey', enable_events=True, key='graph')],
            [sg.Text("Hello from PySimpleGUI")], 
            [sg.Combo(audioFiles, size = (10,1), key='Audio')],
            [sg.Combo(exhibits, size = (10,1), key='Exhibits')],
            [sg.Button('Pair')]
        ]

        #create PySimpleGUI window
        window = sg.Window("Demo", layout,size=(1150, 700), resizable=True, finalize=True)


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
        while True:
            event, values = window.read(timeout=10)
            if event == 'Pair':
                a = values['Audio']
                e = values['Exhibits']
                pair(a,e)
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
                    graph.relocate_figure(point, x, y)
                    
            except OSError:
                s.close()
                print('Closed Socket')
                break
