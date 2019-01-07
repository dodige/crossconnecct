#cd /home/pi/nodejs

#node app.js&

cd /home/pi

/etc/init.d/cron restart

/home/pi/updateModemState.sh&

node /home/pi/nodejs/app.js &

uv4l -driver raspidisp
export LD_PRELOAD=/usr/lib/uv4l/uv4lext/armv6l/libuv4lext.so
route add -net 224.0.0.0 netmask 240.0.0.0 eth0
#avconv -f video4linux2  -re -i /dev/uv4l -f avi -an   udp://239.0.1.23:1234& 


/home/pi/om2.py


# sleep 30

# ./net_tester
