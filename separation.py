from omxplayer.player import OMXPlayer
from bluepy.btle import Scanner
from pathlib import Path
import time
import _thread

calm = OMXPlayer( Path( '/home/pi/separation_video/baba_01.mp4' ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080', '--alpha', '255' ], dbus_name = 'org.mpris.MediaPlayer2.calm' )
calm.set_volume( 0 )
ancious = OMXPlayer( Path( '/home/pi/separation_video/baba_02.mp4' ), args = [ '--no-osd', '--loop', '--layer', '1', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.ancious' )
ancious.set_volume( 0 )
noise = OMXPlayer( Path( '/home/pi/separation_video/baba_02.mp4' ), args = [ '--no-osd', '--loop', '--layer', '2', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name = 'org.mpris.MediaPlayer2.noise' )
noise.set_volume( 0 )

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
                print( rssi_average )
            #print( "rssi: {} ; mac: {}".format( dev.rssi, dev.addr ) ) # print all scannned MAC( Media Access Control ) address, the iOS devices always change the MAC address - randomly -  when the BLE turn on. 

_thread.start_new_thread( rssi_scanner, ('53:1a:42:67:24:56', ) ) 

alpha = 0
alphaSpeed = 25 # 1 - 255 
while True:
    try:
        if ( rssi_average < -50.0 ):
            noise.set_alpha( 0 )
            if alpha == 255:
                continue
            alpha = min( aplha + alphaSpeed, 255 )
            ancious.set_alpha( alpha )
            ancious.set_volume( alpha / 25 )
        if ( rssi_average < -40 and rssi_average > -50 ):
            noise.set_alpha( 255 )
        if ( rssi_average > -40.0 ):
            noise.set_alpha( 0 )
            if alpha == 0:
                continue
            alpha = max( aplha - alphaSpeed, 0 )
            ancious.set_alpha( alpha )
            ancious.set_volume( alpha / 25 )
    except:
        raise Exception( "Error occured" )