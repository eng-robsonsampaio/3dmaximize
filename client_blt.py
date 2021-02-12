import obexftp
import time
cli=obexftp.client(obexftp.BLUETOOTH)
channel=obexftp.browsebt('A8:16:D0:26:09:98',obexftp.PUSH)
print(channel) #it is the correct channel, I've doubled checked
cli.connect ('A8:16:D0:26:09:98',channel)
time.sleep(2)
cli.put_file("./test1.wav") #I also noticed you need to wait a second before this
cli.disconnect()
