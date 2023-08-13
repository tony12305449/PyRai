wget http://192.168.50.145:31338/mips_scanner -O scanner
while [ ! -f scanner ]; do
    sleep 1
done