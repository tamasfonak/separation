from omxplayer.player import OMXPlayer
from bluepy.btle import Scanner
from pathlib import Path
import _thread 

#calm = OMXPlayer( Path( '/home/pi/separation_video/baba_01.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080' ], dbus_name = 'org.mpris.MediaPlayer2.calm' )
#calm.set_volume( 0 )
#ancious = OMXPlayer( Path( '/home/pi/separation_video/baba_02.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.ancious' )
#ancious.set_volume( 0 )

rssi_average = 1
rssi_average_list = []
def rssi_scanner( address ):
    ble_list = Scanner().scan( 1.0 ) #10.0 sec scanning 
    for dev in ble_list:
        if dev.addr == address:
            rssi_average_list.append( dev.rssi )
            if len( rssi_average_list ) > 10:
                rssi_average_list.pop( 0 )
            rssi_average = ( float( sum( rssi_average_list ) ) / len( rssi_average_list ) )
        print( "rssi: {} ; mac: {}".format( dev.rssi, dev.addr ) )

_thread.start_new_thread( rssi_scanner, ('B8:27:EB:06:DF:94', ) ) 


while True:
    try:
        #device_is_close = rssi_average > -3
        #device_is_far = rssi_average < -6
        if rssi_average < -6:
            #ancious.set_alpha( 255 )
            #ancious.set_volume( 100 )
            pass
        if rssi_average > -3:
            #ancious.set_alpha( 255 )
            #ancious.set_volume( 100 )
            pass
    except:
        raise Exception( "Error occured" )