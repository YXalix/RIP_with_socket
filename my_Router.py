
import socket
import os
import threading
import time
import random

__auther__ = 'zhp'

class my_Router():
    def __init__(self,port):
        self.port = port
        self.address = ('127.0.0.1',int(port))
        self.net_path = "config/net.txt"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.change_sign = 1
        self.receive_sign = 0
        self.info_op = ''
        self.router_table = []

        f = open(self.net_path)
        nets_data = f.readlines()
        f.close()
        net_routers = [ net_data.split(' ') for net_data in nets_data]
        for net in net_routers:
            net[-1] = net[-1].replace('\n', '')
            if self.port in net[2:]:
                if net[1] == '1':
                    self.router_table.append([net[0],1,'8080',0])

    def get_direct_net(self):
        f = open(self.net_path)
        nets_data = f.readlines()
        f.close()
        direct_net = []
        net_routers = [ net_data.split(' ') for net_data in nets_data]
        for net in net_routers:
            net[-1] = net[-1].replace('\n', '')
            if self.port in net[2:]:
                direct_net.append(net[0])
        
        return direct_net

    def get_near_router(self):
        f = open(self.net_path)
        nets_data = f.readlines()
        f.close()
        near_router = []
        net_routers = [ net_data.split(' ') for net_data in nets_data]
        for net in net_routers:
            net[-1] = net[-1].replace('\n', '')
            if net[1] == '1':
                if self.port in net[2:]:
                    for router_port in net[2:]:
                        if self.port != router_port:
                            if router_port in near_router:
                                continue
                            else:
                                near_router.append(router_port)
        return near_router

    def get_sent_router_info(self):
        router_info = []
        for router_data in self.router_table:
            temp = router_data.copy()
            if temp[1] > 15:
                temp[2] = self.port
            else:
                temp[1] = temp[1] + 1
                temp[2] = self.port
            router_info.append(temp[:-1])
        return router_info

    def deal_to_str_router_info(self):
        temp = ""
        for table_info in self.get_sent_router_info():
            temp = temp + table_info[0] + " " +str(table_info[1]) + " " + table_info[2] + "\n"
        return temp

    def deal_to_table_router_info(self,message):
        router_table = []
        for table_item in message.split('\n')[:-1]:
            temp = table_item.split(' ')
            temp[1] = int(temp[1])
            temp.append(0)
            router_table.append(temp)
        return router_table

    def sent_router_info(self):
        for router_port in self.get_near_router():
            target_address = ('127.0.0.1',int(router_port))
            message = self.deal_to_str_router_info()
            self.s.sendto(message.encode(),target_address)
                #print(message)
            #time.sleep(random.uniform(25.5,30))
            #time.sleep(random.uniform(1,2))
            
    def update_router_table(self,router_info):
        change = False
        for router_data in router_info:
            flag = True
            for self_data in self.router_table:
                if router_data[0] == self_data[0]:
                    flag = False
                    if router_data[2] == self_data[2]:  #same router
                        if self_data[1] != router_data[1]:
                            change = True
                            self.info_op += '\n' + self_data[0] + ' ' + str(self_data[1]) + '->' + str(router_data[1]) + ' ' +self_data[2] + '->' + self_data[2]
                        self_data[1] = router_data[1]
                        self_data[3] = 0
                    else:
                        if router_data[1] < self_data[1]:
                            self.info_op += '\n' + self_data[0] + ' ' + str(self_data[1]) + '->' + str(router_data[1]) + ' ' +self_data[2] + '->' + router_data[2]
                            self_data[2] = router_data[2]
                            self_data[1] = router_data[1]
                            self_data[3] = 0
                            change = True
                        else:
                            self_data[3] = 0
            if flag:#no find net
                self.router_table.append(router_data)
                self.info_op += '\nnew:' + router_data[0] + ' ' + str(router_data[1]) + ' ' + router_data[2]
                change = True

        if change:
            self.sent_router_info()
            self.change_sign = 1
        else:
            self.info_op += 'no change\n'

    def router_timer(self):
        time_num = 0
        while True:
            time_num += 1
            for table_info_item in self.router_table:
                if table_info_item[3] < 180:
                    table_info_item[3]+=1
                elif table_info_item[3] < 300:
                    table_info_item[3]+=1
                    if table_info_item[1] != 16:
                        table_info_item[1] = 16
                        self.change_sign = 1
                        self.sent_router_info()
                else:
                    index = self.router_table.index(table_info_item)
                    del self.router_table[index]
                    self.change_sign =1
                    self.sent_router_info()
            #print(self.router_table)
            if time_num > random.uniform(25.5,30):
                self.sent_router_info()
                time_num = 0
            time.sleep(1)
       
    def router_net_timer(self):
        while True:
            f = open(self.net_path)
            nets_data = f.readlines()
            f.close()
            nets_routers = [ net_data.split(' ') for net_data in nets_data]
            for net_routers in nets_routers:
                net_routers[-1] = net_routers[-1].replace('\n', '')
                if self.port in net_routers[2:]:
                    if net_routers[1] == '1':
                        out_sign = True
                        for table_item in self.router_table:
                            if table_item[0] == net_routers[0]:
                                out_sign = False
                                if table_item[1] != 1:
                                    table_item[1] = 1
                                    table_item[2] = '8080'
                                    table_item[3] = 0
                                    self.change_sign = 1
                                
                        if out_sign:
                            self.router_table.append([net_routers[0],1,'8080',0])
                            self.change_sign = 1

                    elif net_routers[1] == '0':
                        out_sign = True
                        for table_item in self.router_table:
                            if table_item[0] == net_routers[0]:
                                out_sign = False
                                if table_item[1] == 1:
                                    table_item[1] = 16
                                    table_item[3] = 0
                                    table_item[2] = '8080'
                                    self.change_sign = 1

            if self.change_sign == 1:
                self.sent_router_info()
            time.sleep(2)


    def router_start(self):
        self.s.bind(self.address)
        time.sleep(3)   #wait all router start
        time_count = threading.Thread(target=self.router_timer) #new thread to sent router_info
        time_count.start()
        view_net = threading.Thread(target=self.router_net_timer) #new thread to check net state
        view_net.start()
        self.sent_router_info()
        while True:
            data, addr = self.s.recvfrom(2048)
            message = self.deal_to_table_router_info(data.decode())
            self.info_op += 'reveive from ' + str(addr[1]) + ':'
            self.update_router_table(message)
            self.receive_sign = 1
            self.info_op += '\n'

            #print(data)
            #ts = threading.Thread(target=save_router_info) #new thread to save router info
            #ts.start()
            #ts.join()
        self.s.close()
        time_count.join()
        view_net.join()

if __name__ == "__main__":
    #port = input("router port:")
    router = my_Router('48081')
    print("direct net:",router.get_direct_net())
    print("near router:",router.get_near_router())
    print("get sent router table info:",router.get_sent_router_info())
    print("deal to str router info:",router.deal_to_str_router_info())
    print('deal to table router info:',router.deal_to_table_router_info(router.deal_to_str_router_info()))
    print("update router table:",router.update_router_table([['net1', 2, '48082', 0], ['net2', 2, '48082', 0], ['net3', 2, '48082', 0]]))
    router.router_net_timer()
    #router.router_start()

