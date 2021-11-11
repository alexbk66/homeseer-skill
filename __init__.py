from mycroft import MycroftSkill, intent_file_handler
import threading
import time
import socket


def thread_function(ip, port):
    print("Thread %s:%s", ip, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    message = b"your very important message"
    while True:
       time.sleep(2)
       print("Thread %s ", port) 
       server.sendto(message, (ip, port))

class Homeseer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        print('****************');

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip = s.getsockname()[0]
        local_ip = local_ip[:local_ip.rfind('.')+1] + '255'
        
        broadcast = self.GetBroadcastAddr()

        #x = threading.Thread(target=thread_function, args=("255.255.255.255", 10666))
        #x = threading.Thread(target=thread_function, args=(local_ip, 10666))
        x = threading.Thread(target=thread_function, args=(broadcast, 10666))

        x.start()        

        print('****************');

    @intent_file_handler('homeseer.intent')
    def handle_homeseer(self, message):
        self.speak_dialog('homeseer')


    def GetBroadcastAddr(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip = s.getsockname()[0]
        return local_ip[:local_ip.rfind('.')+1] + '255'


def create_skill():
    return Homeseer()

