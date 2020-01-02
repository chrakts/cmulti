sudo ifconfig lo multicast
sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev lo
socat -d -d pty pty &
python -m serial.tools.miniterm -e /dev/pts/2
