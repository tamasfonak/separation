
from omxplayer.player import OMXPlayer
from bt_proximity import BluetoothRSSI
from pathlib import Path
import time
import _thread
import subprocess

subprocess.call( 'sudo hciconfig hci0 down && sudo hciconfig hci0 up', shell = True )

calm = OMXPlayer( Path( '/home/pi/separation_video/anya_a_ff.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080', '--alpha', '255' ], dbus_name = 'org.mpris.MediaPlayer2.calm' )
calm.set_volume( 0 )
ancious = OMXPlayer( Path( '/home/pi/separation_video/anya_b_ff.mp4' ), args = [ '--no-osd', '--loop', '--layer', '1', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.ancious' )
ancious.set_volume( 0 )

rssi_average = 0
def rssi_scanner( address ):
    global rssi_average
    rssi = BluetoothRSSI( addr=address )
    rssi_average_list = []
    while True:
        time.sleep( 0.2 )
        r = rssi.request_rssi()
        if r is None:
            continue
        rssi_average_list.append( r[ 0 ] )
        if len( rssi_average_list ) > 10:
            rssi_average_list.pop( 0 )
        rssi_average = ( float( sum( rssi_average_list ) ) / len( rssi_average_list ) )
        print( rssi_average )

_thread.start_new_thread( rssi_scanner, ( 'B8:27:EB:5B:88:82', ) )

alpha = 0
alphaSpeed = 8 # 1 - 255
while True:
    try:
        if rssi_average < 3:
            if not ancious.is_playing():
                ancious.play()
            if alpha > 255:
                if calm.is_playing():
                    calm.pause()
                    calm.set_position( 0 )
                continue
            alpha = min( alpha + alphaSpeed, 255 )
            ancious.set_alpha( alpha )
            ancious.set_volume( alpha / 255 )
        if rssi_average > 8:
            if not calm.is_playing():
                calm.play()
            if alpha < 0:
                if ancious.is_playing():
                    ancious.pause()
                    ancious.set_position( 0 )
                continue
            alpha = max( alpha - alphaSpeed, 0 )
            ancious.set_alpha( alpha )
            ancious.set_volume( alpha / 255 )
    except:
        raise Exception( "Error occured" )

