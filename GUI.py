
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from my_Router import my_Router
import os
import threading
import random
from tkinter import END

nets_path = "config/net.txt"
def op_net(net,op):
    f = open(nets_path)
    nets_data = f.readlines()
    f.close()
    nets_routers = [ net_data.split(' ') for net_data in nets_data]
    new_data = []
    for net_routers in nets_routers:
        net_routers[-1] = net_routers[-1].replace('\n', '')
        if net == net_routers[0]:
            net_routers[1] = op       #0 - close  , 1 - open

    f = open(router.net_path,'w+')
    for net_routers in nets_routers:
        net_routers[-1] += '\n'
        new_data.append(' '.join(net_routers))
    
    f.writelines(new_data)
    f.close()

def router_off(net):
    f = open(nets_path)
    nets_data = f.readlines()
    f.close()
    nets_routers = [ net_data.split(' ') for net_data in nets_data]
    new_data = []
    for net_routers in nets_routers:
        net_routers[-1] = net_routers[-1].replace('\n', '')
        if net == net_routers[0]:
            if router.port in net_routers[2:]:
                index = net_routers.index(router.port)
                del net_routers[index]
                
    f = open(nets_path,'w+')
    for net_routers in nets_routers:
        net_routers[-1] += '\n'
        new_data.append(' '.join(net_routers))
    f.writelines(new_data)
    f.close()
    print(new_data)

def router_on(net):
    f = open(nets_path)
    nets_data = f.readlines()
    f.close()
    nets_routers = [ net_data.split(' ') for net_data in nets_data]
    new_data = []
    for net_routers in nets_routers:
        net_routers[-1] = net_routers[-1].replace('\n', '')
        if net == net_routers[0]:
            if router.port not in net_routers[2:]:
                net_routers.append(router.port)
    f = open(nets_path,'w+')
    for net_routers in nets_routers:
        net_routers[-1] += '\n'
        new_data.append(' '.join(net_routers))
    f.writelines(new_data)
    f.close()
    print(new_data)

def show_table_info():
    if router.change_sign == 1:
        text = ['  target_net   distence   router ']
        table_info_box.delete(1.0,'end')
        for item in router.router_table:
            item = '      ' + item[0] + '        ' + str(item[1]) + '        ' + item[2]
            text.append(item)
        text = '\n'.join(text)
        table_info_box.insert(1.0,text)
        router.change_sign = 0
    table_info_box.after(100, show_table_info)



def show_info_op():
    if router.receive_sign == 1:
        scr.insert('1.0',router.info_op)
        router.receive_sign = 0
        router.info_op = ''
    scr.after(100,show_info_op)
     

#init Router
f = open('./config/init.txt')
init_data = f.readline()
init_data = init_data.split(' ')
f.close()
port = init_data[int(init_data[0])]
init_data[0] = str(int(init_data[0])%5 +1)
temp_init_data = ' '.join(init_data)
f = open('./config/init.txt','w+')
f.write(temp_init_data)
f.close()
router = my_Router(port)

start = threading.Thread(target=router.router_start)
start.start()


#init app
app = tk.Tk()
app.geometry("300x400")

app.title('Router : %s' %(router.port))
app.iconbitmap('router.ico')

#table name
info_lable = tk.Label(app,text='Router_Table',fg = 'white',bg='black',)
info_lable.place(x = 120,y = 10)

#table info
table_info_box = tk.Text(app,height = 7,width = 35)
table_info_box.place(x = 40,y = 40)

show_table_info()

net1_on = tk.Button(app,text = 'net1 on',command = lambda: op_net('net1','1'))
net1_on.place(x = 40,y = 150)
net1_off = tk.Button(app,text = 'net1 off',command = lambda: op_net('net1','0'))
net1_off.place(x = 40,y = 180)

#net1 router off button
off = tk.Button(app,text = 'off net1',command = lambda: router_off('net1'))
off.place(x = 40,y = 245)
#net1 router on button
on = tk.Button(app,text = 'lin net1',command = lambda: router_on('net1'))
on.place(x=40,y = 215)
#-----------------------------------------------------------------
net2_on = tk.Button(app,text = 'net2 on',command = lambda: op_net('net2','1'))
net2_on.place(x = 100,y = 150)
net1_off = tk.Button(app,text = 'net2 off',command = lambda: op_net('net2','0'))
net1_off.place(x = 100,y = 180)

#net1 router off button
off = tk.Button(app,text = 'off net2',command = lambda: router_off('net2'))
off.place(x = 100,y = 245)
#net1 router on button
on = tk.Button(app,text = 'lin net2',command = lambda: router_on('net2'))
on.place(x=100,y = 215)
#-----------------------------------------------------------------
net3_on = tk.Button(app,text = 'net3 on',command = lambda: op_net('net3','1'))
net3_on.place(x = 160,y = 150)
net1_off = tk.Button(app,text = 'net3 off',command = lambda: op_net('net3','0'))
net1_off.place(x = 160,y = 180)

#net1 router off button
off = tk.Button(app,text = 'off net3',command = lambda: router_off('net3'))
off.place(x = 160,y = 245)
#net1 router on button
on = tk.Button(app,text = 'lin net3',command = lambda: router_on('net3'))
on.place(x=160,y = 215)
#-----------------------------------------------------------------
net4_on = tk.Button(app,text = 'net4 on',command = lambda: op_net('net4','1'))
net4_on.place(x = 220,y = 150)
net1_off = tk.Button(app,text = 'net4 off',command = lambda: op_net('net4','0'))
net1_off.place(x = 220,y = 180)

#net1 router off button
off = tk.Button(app,text = 'off net4',command = lambda: router_off('net4'))
off.place(x = 220,y = 245)
#net1 router on button
on = tk.Button(app,text = 'lin net4',command = lambda: router_on('net4'))
on.place(x=220,y = 215)
#-----------------------------------------------------------------

#update_button = tk.Button(app,text='update',width=5,height=1,command=show_table_info)
#update_button.place(x = 250,y=5)

#clock time
#table name
info_op = tk.Label(app,text='op',fg = 'white',bg='black',)
info_op.place(x = 10,y = 295)
scr = scrolledtext.ScrolledText(app,width = 30,height = 6,wrap=tk.WORD)
scr.place(x = 40,y = 280)
show_info_op()

app.mainloop()

