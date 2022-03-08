#!/usr/bin/env python3

import zmq
from pynput import keyboard
import time


# testing class that listens for keys and sends them to robot controller

def listenForKey(socket):
    with keyboard.Events() as events:
        event = events.get(1e6)
        if event.key == keyboard.KeyCode.from_char('i'):
            print('Command recognized! Sending %s' % event.key)
            socket.send_string('i')
        elif event.key == keyboard.KeyCode.from_char('o'):
            print('Command recognized! Sending %s' % event.key)
            socket.send_string('o')
        elif event.key == keyboard.KeyCode.from_char('k'):
            print('Command recognized! Sending %s' % event.key)
            socket.send_string('k')
        elif event.key == keyboard.KeyCode.from_char('l'):
            print('Command recognized! Sending %s' % event.key)
            socket.send_string('l')
        else:
            raise Exception("Command not recognized")

def listenForConfirmation():
    message = socket.recv_string()   
    print("Recieved reply: %s" % message)

if __name__ == "__main__":
    context = zmq.Context()

    #  Socket to talk to server
    print("Listening for you input!")
    # socket = context.socket(zmq.REQ) # For TCP
    socket = context.socket(zmq.PUB) # For UDP 
    # socket.connect("tcp://localhost:5555")
    socket.bind("tcp://*:4441")


    while True:
        listenForKey(socket)
        # listenForConfirmation() # only useful for TCP
        time.sleep(0.1)
        
