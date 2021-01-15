# Read data from the txt
content=[]
f= open("0.1_0.85_50k.txt",'r')
for line in f:
    content.append(line.split())
list_of_p= []
list_of_q = []
list_of_z=[]
list_of_end=[]
list_of_it=[]
for p in range(10):
    list_of_p.append(p*0.1)
    list_of_q.append(p*0.1)

for item in content:
    list_of_end.append(float(item[3]))
    list_of_it.append(float(item[4]))
new_it = []
new_end =[]
for index in range(9):
    new_it.append(list_of_it[9*index:9+index*9])
    new_end.append(list_of_end[9*index:9+index*9])

import plotly.graph_objects as go
fig = go.Figure(go.Surface(
    contours = {
        "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color":"white"},
        "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05}
    },
    x = list_of_p,
    y = list_of_q,
    z = new_end))
fig.update_layout(
        scene = {
            'camera_eye': {"x": 0, "y": -1, "z": 0.5},
            "aspectratio": {"x": 1, "y": 1, "z": 0.2}
        })
fig.show()
fig = go.Figure(go.Surface(
    contours = {
        "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color":"white"},
        "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05}
    },
    x = list_of_p,
    y = list_of_q,
    z = new_it))
fig.update_layout(
        scene = {
            'camera_eye': {"x": 0, "y": -1, "z": 0.5},
            "aspectratio": {"x": 1, "y": 1, "z": 0.2}
        })
fig.show()
