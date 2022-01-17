from omxplayer.player import OMXPlayer
from bluepy.btle import Scanner
from pathlib import Path
import time
import _thread

ancious = OMXPlayer( Path( '/home/pi/separation_video/baba_02.mp4' ), args = [ '--no-osd', '--loop', '--layer', '1', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.ancious' )
ancious.set_volume( 0 )
calm = OMXPlayer( Path( '/home/pi/separation_video/baba_01.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.calm' )
calm.set_volume( 0 )


rssi_average = 1
rssi_average_list = []
def rssi_scanner( address ):
    global rssi_average
    while True:
        ble_list = Scanner().scan( 1.0 ) #10.0 sec scanning 
        for dev in ble_list:
            if dev.addr == address:
                rssi_average_list.append( dev.rssi )
                if len( rssi_average_list ) > 5:
                    rssi_average_list.pop( 0 )
                rssi_average = ( float( sum( rssi_average_list ) ) / len( rssi_average_list ) )
                print( abs(rssi_average) )
            #someprint( "rssi: {} ; mac: {}".format( dev.rssi, dev.addr ) )

_thread.start_new_thread( rssi_scanner, ('53:1A:42:67:24:56', ) ) 


while True:
    try:
        if (abs(rssi_average) > 50.0 ):
            ancious.set_alpha( 255 )
            ancious.set_volume( 1 )
            calm.set_alpha( 0 )
        if (abs(rssi_average) < 40.0 ):
            ancious.set_alpha( 0 )
            calm.set_alpha( 255 )
            ancious.set_volume( 0 )
    except:
        raise Exception( "Error occured" )