# separation
DWM1000 (decawave)

Raspberry Pi bluetooth proximity project:

Set in the /boot/config.txt
```
gpu_mem_256
```

Install python3 and plugins and clone the project:
```
sudo apt install python3-pip
sudo pip3 install bluepy
sudo pip3 install omxplayer-wrapper
git clone https://github.com/tamasfonak/separation

sudo setcap cap_net_raw+e  <PATH>/bluepy-helper
sudo setcap cap_net_admin+eip  <PATH>/bluepy-helper
```
Set in the /etc/bluetooth/main.conf
```
DiscoverableTimeout = 0
PairableTimeout = 0
```
Set in the /etc/rc.local
```
sudo bluetoothctl <<EOF
power on
discoverable on
pairable on
EOF

python3 /home/pi/separation/separation.py
```
