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
        x = threading.Thread(target=thread_function, args=("255.255.255.255", 10666))
        #x = threading.Thread(target=thread_function, args=("192.168.0.131", 10666))
        x.start()        
        print('****************');

    @intent_file_handler('homeseer.intent')
    def handle_homeseer(self, message):
        self.speak_dialog('homeseer')


def create_skill():
    return Homeseer()

