import vlc
import glob
import time
from random import random
from bt_proximity import BluetoothRSSI


VIDEOS = ["video/adiktator.mp4", "video/hev_spot6.mp4"]
BT_ADDR = 'B8:27:EB:06:DF:94'
btrssi = BluetoothRSSI(addr=BT_ADDR)


class MediaPlayer():
    ''' Ez a media player osztalyunk ami segit nekunk
        osszecsomagolni a sok-sok apro kodot, hogy
        nekunk az osztalyon kivul mar semmit ne kelljen
        csinalnunk, csak kb annyit, hogy "player.play()"
        vagy "plyer.swap_to_other_video()"
    '''

    def __init__(self, video1, video2):
        '''Ez a fuggveny az, amibol letrejon az osztaly.
           Ahhoz, hogy letrejojjon, szukseg lesz ket video
           elerhetosegre, video1-re es video2-re. Ezek vannak
           fent a VIDEOS konstansban.
        '''

        # Ez a fo instance, sokat en sem tudok rola,
        # ez egy fajta kozpontja a vlc-nek, innen kell
        # definialni es szarmaztatni mindent. Ez nem
        # olyan fontos
        self.instance = vlc.Instance()

        # Itt definialunk is egy playlistet, ami tartalmazza
        # a ket videot
        self.playlist = self.instance.media_list_new()
        self.playlist.insert_media(self.instance.media_new(video1), 0)
        self.playlist.insert_media(self.instance.media_new(video2), 1)

        # Ez lesz a videolejatszonk
        self.player = self.instance.media_player_new()

        # Ez pedig az ID-ja annak a videonak, amit eppen
        # le akarunk jatszani (0 vagy 1)
        self.play_id = 0
        self.rssi_average_list = []


    def run(self):
        '''Ez futtatja a videot folyamatosan, miutan mindent
           aprosagot beallitottunk. Addig jatszunk egy videot,
           amig nem valtunk a masikra, vagy nem er veget a video. Az
           utobbi esetben ujra kell inditani
        '''
        self.play()
        while True:

            # Minden tized masodpercben csekkoljuk az eventeket,
            # (pl hogy kell-e videot cserelni)
            # kozottuk varunk, a python nyelven alszunk.
            time.sleep(0.1)

            # Ha a video veget ert, inditsuk ujra
            if self.ended():
                self.restart()

            # Debug tool, lassuk, hogy mit ir ki ez a tavolsagmero
            # fuggveny

            self.rssi_average_list.append( btrssi.get_rssi() )
            if len( self.rssi_average_list ) > 10:
                 self.rssi_average_list.pop(0)

            rssi_average = ( float( sum( self.rssi_average_list ) ) / len( self.rssi_average_list ) )
	    print( rssi_average )
            # ======================================================
            # Itt kezdodnek az uj sorok
            # ======================================================

            # A masik eszkoz tavolsaga, meghatarozva egy biztosan
            # kozeli es egy biztosan tavoli ertekkel. A koztes
            # ertekek alkossak a 'senki foldjet', ahol nem tudjuk
            # biztosan eldonteni, hogy kozeli vagy tavoli
            device_is_close = rssi_average > -3
            device_is_far = rssi_average < -6

            # Ez a valtozo mutatja, hogy az a video van-e
            # most berakva, ami a kozeli video
            close_video_on_screen = self.play_id == 0

            # Mikor valtsunk? Ez egy boolean lesz, True / False
            # erteket fog felvenni. Akkor kell valtani, ha
            # a tavolsag nincs szinkronban a hozzarendelt videoval
            should_swap = (
                (device_is_close and not close_video_on_screen) or
                (device_is_far and close_video_on_screen)
            )

            if should_swap:
                self.swap()


    def ended(self):
        '''Visszaadja, hogy a lejatszonk a vegere ert-e
           az aktualis videonak
        '''
        return self.player.get_state() == vlc.State.Ended


    def play(self):
        '''Elinditja az aktualis videot'''
        self.player.set_media(self.playlist[self.play_id])
        self.player.play()


    def restart(self):
        '''Ujrainditja az aktualis videot'''
        self.player.pause()
        self.play()


    def swap(self):
        '''Lecsereli az aktualis videot a masikra'''
        self.player.pause()
        self.play_id = 1 - self.play_id # (0 --> 1, 1 --> 0)
        self.play()


'''
Most jon a dolgok konnyebbik resze.
Mostmar nincs mas dolgunk, mint definialni az
osztalyunkat, es elinditani.
'''

player = MediaPlayer(VIDEOS[0], VIDEOS[1])
player.run()
