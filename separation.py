from omxplayer.player import OMXPlayer
from bluepy.btle import Scanner
from pathlib import Path
import _thread 

#calm = OMXPlayer( Path( '/home/pi/separation_video/baba_01.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080' ], dbus_name = 'org.mpris.MediaPlayer2.calm' )
#calm.set_volume( 0 )
ancious = OMXPlayer( Path( '/home/pi/separation_video/baba_02.mp4' ), args = [ '--no-osd', '--loop', '--layer', '1', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.ancious' )
ancious.set_volume( 0 )

rssi_average = 1
rssi_average_list = []
def rssi_scanner( address ):
    while True:
        ble_list = Scanner().scan( 10.0 ) #10.0 sec scanning 
        for dev in ble_list:
            if dev.addr == address:
                rssi_average_list.append( dev.rssi )
                if len( rssi_average_list ) > 10:
                    rssi_average_list.pop( 0 )
                rssi_average = ( float( sum( rssi_average_list ) ) / len( rssi_average_list ) )
                print( rssi_average )
            print( "rssi: {} ; mac: {}".format( dev.rssi, dev.addr ) )

_thread.start_new_thread( rssi_scanner, ('7e:17:54:25:08:54', ) ) 


while True:
    try:
        #device_is_close = rssi_average > -3
        #device_is_far = rssi_average < -6
        if rssi_average < -60:
            ancious.set_alpha( 0 )
            ancious.set_volume( 0 )
        if rssi_average > -40:
            ancious.set_alpha( 0 )
            ancious.set_volume( 0 )
    except:
        raise Exception( "Error occured" )