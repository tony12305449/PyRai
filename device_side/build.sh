#!/bin/bash

output_folder="../ELF_file/bin"
mkdir -p $output_folder

#請小心服用
rm -rf  ${output_folder}/*

echo "Compiling scanner..."
cd scanner
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o test -o ../${output_folder}/arm64_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=386 go build -o test -o ../${output_folder}/386_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o test -o ../${output_folder}/amd64_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=arm go build -o test -o ../${output_folder}/arm_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=loong64 go build -o test -o ../${output_folder}/loong64_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=mips go build -o test -o ../${output_folder}/mips_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=mips64 go build -o test -o ../${output_folder}/mips64_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=mips64le go build -o test -o ../${output_folder}/mips64le_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=ppc64 go build -o test -o ../${output_folder}/ppc64_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=ppc64le go build -o test -o ../${output_folder}/ppc64le_scanner
CGO_ENABLED=0 GOOS=linux GOARCH=riscv64 go build -o test -o ../${output_folder}/riscv64_scanner
CGO_ENABLED=0 GOOS=windows GOARCH=386 go build -o test -o ../${output_folder}/windows_386_scanner
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o test -o ../${output_folder}/windows_amd64_scanner
CGO_ENABLED=0 GOOS=windows GOARCH=arm go build -o test -o ../${output_folder}/windows_arm_scanner
CGO_ENABLED=0 GOOS=windows GOARCH=arm64 go build -o test -o ../${output_folder}/windows_arm64_scanner
cd ..

# 編譯 loader 資料夾內的程式碼
echo "Compiling loader..."
cd loader
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o test -o ../${output_folder}/arm64_loader
CGO_ENABLED=0 GOOS=linux GOARCH=386 go build -o test -o ../${output_folder}/386_loader
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o test -o ../${output_folder}/amd64_loader
CGO_ENABLED=0 GOOS=linux GOARCH=arm go build -o test -o ../${output_folder}/arm_loader
CGO_ENABLED=0 GOOS=linux GOARCH=loong64 go build -o test -o ../${output_folder}/loong64_loader
CGO_ENABLED=0 GOOS=linux GOARCH=mips go build -o test -o ../${output_folder}/mips_loader
CGO_ENABLED=0 GOOS=linux GOARCH=mips64 go build -o test -o ../${output_folder}/mips64_loader
CGO_ENABLED=0 GOOS=linux GOARCH=mips64le go build -o test -o ../${output_folder}/mips64le_loader
CGO_ENABLED=0 GOOS=linux GOARCH=ppc64 go build -o test -o ../${output_folder}/ppc64_loader
CGO_ENABLED=0 GOOS=linux GOARCH=ppc64le go build -o test -o ../${output_folder}/ppc64le_loader
CGO_ENABLED=0 GOOS=linux GOARCH=riscv64 go build -o test -o ../${output_folder}/riscv64_loader
CGO_ENABLED=0 GOOS=windows GOARCH=386 go build -o test -o ../${output_folder}/windows_386_loader
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o test -o ../${output_folder}/windows_amd64_loader
CGO_ENABLED=0 GOOS=windows GOARCH=arm go build -o test -o ../${output_folder}/windows_arm_loader
CGO_ENABLED=0 GOOS=windows GOARCH=arm64 go build -o test -o ../${output_folder}/windows_arm64_scanner
cd ..

echo "Compilation finished."


# Go language can compile linux architecture as follows
#linux/386
#linux/amd64
#linux/arm
#linux/arm64
#linux/loong64
#linux/mips
#linux/mips64
#linux/mips64le
#linux/mipsle
#linux/ppc64
#linux/ppc64le
#linux/riscv64
#windows/386
#windows/amd64
#windows/arm
#windows/arm64
# if want to get other ,you can use command `go tool dist list` to find