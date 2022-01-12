from omxplayer.player import OMXPlayer
from bluepy.btle import Scanner
from pathlib import Path
import _thread 

calm = OMXPlayer( Path( '/home/pi/separation_video/baba_01.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.calm' )
calm.set_volume( 0 )

ancious = OMXPlayer( Path( '/home/pi/separation_video/baba_02.mp4' ), args = [ '--no-osd', '--loop', '--layer', '1', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.ancious' )
ancious.set_volume( 0 )

rssi_average = 0

def rssi_scanner( address ):
    global rssi_average
    rssi_average_list = []
    while True:
        ble_list = Scanner().scan( 1.0 ) #1.0 sec scanning 
        for dev in ble_list:
            if dev.addr == address:
                rssi_average_list.append( dev.rssi )
                if len( rssi_average_list ) > 5:
                    rssi_average_list.pop( 0 )
                rssi_average = ( float( sum( rssi_average_list ) ) / len( rssi_average_list ) )

_thread.start_new_thread( rssi_scanner, ('7e:17:54:25:08:54', ) ) 

alpha = 0;

while True:
    try:
        if ( rssi_average < -50 ):
            if alpha < 255:
                alpha += 1
            ancious.set_alpha( alpha )
            ancious.set_volume( alpha / 25 )
        if ( rssi_average > -40 ):
            if alpha > 0:
                alpha += 1
            ancious.set_alpha( alpha )
            ancious.set_volume( alpha / 25 )
    except:
        raise Exception( "Error occured" )