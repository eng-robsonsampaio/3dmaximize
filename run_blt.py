

import bluetooth
import os
import subprocess
from time import sleep

if __name__ == "__main__":
    print("Awaiting connection")
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #create server object
    port = 1
    server_socket.bind(("",port))
    server_socket.listen(1)
    client_socket,address = server_socket.accept()

    print("Accepted connection from ",address)

    while True:
        res = client_socket.recv(1024)
        res = res.decode().strip() # decodes from bin and removes the '\n' at the end of the string received
        if res == "quit":
            print ("Quiting")
            break
        else:
            print("Recording in 5 seconds")
            sleep(5)
            os.system("python3 /home/pi/3dmaximize/recording.py "+address[0]) # calls the script for recording

    print("End of communication")
#    client_socket.close()
#    server_socket.close()
