from omxplayer.player import OMXPlayer
from bluepy.btle import Scanner
from pathlib import Path 
import _thread 

#loop = OMXPlayer( Path( '/home/pi/separation_videos/mother.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080' ], dbus_name = 'org.mpris.MediaPlayer2.loop' )
#loop.set_volume( 0 )


while True:
    try:
        #10.0 sec scanning
        ble_list = Scanner().scan(10.0)
        for dev in ble_list:
            print("rssi: {} ; mac: {}".format(dev.rssi,dev.addr))
    except:
        raise Exception("Error occured")