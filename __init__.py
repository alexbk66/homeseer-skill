from mycroft import MycroftSkill, intent_file_handler
from datetime import datetime
import threading
import time
import socket


def thread_function(ip, port):
    print("Thread %s:%s", ip, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)

    n = 0
    
    while True:
       time.sleep(2)
       n = n + 1
       message = "your very important message: %s" % datetime.now().strftime("%H:%M:%S")
       message = message.encode()
              
       server.sendto(message, (ip, port))


class Homeseer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)


    def initialize(self):
            
        self.log.info("__init__");

       
        broadcast = self.GetBroadcastAddr()

        self.speak_dialog('Broadcast %s' % broadcast);
        
        x = threading.Thread(target=thread_function, args=(broadcast, 10666))

        x.start()        

        print('****************');
        
    
    @intent_file_handler('homeseer.intent')
    def handle_homeseer(self, message):
        self.speak_dialog('homeseer')


    def GetBroadcastAddr(self):
        """ Get local IP and replace last bit with 255 """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # connect() for UDP doesn't send packets
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        return local_ip[:local_ip.rfind('.')+1] + '255'


def create_skill():
    return Homeseer()

