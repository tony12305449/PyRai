CGO_ENABLED=0 GOOS=linux GOARCH=mips GOMIPS=softfloat go build -o ../../ELF_file/bin/test0
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o ../../ELF_file/bin/test1
CGO_ENABLED=0 GOOS=linux GOARCH=386 go build -o ../../ELF_file/bin/test2
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o ../../ELF_file/bin/test3
CGO_ENABLED=0 GOOS=linux GOARCH=arm go build -o ../../ELF_file/bin/test4
CGO_ENABLED=0 GOOS=linux GOARCH=loong64 go build -o ../../ELF_file/bin/test5
CGO_ENABLED=0 GOOS=linux GOARCH=mips go build -o ../../ELF_file/bin/test6
CGO_ENABLED=0 GOOS=linux GOARCH=mips64 go build -o ../../ELF_file/bin/test7
CGO_ENABLED=0 GOOS=linux GOARCH=mips64le go build -o ../../ELF_file/bin/test8
CGO_ENABLED=0 GOOS=linux GOARCH=ppc64 go build -o ../../ELF_file/bin/test9
CGO_ENABLED=0 GOOS=linux GOARCH=ppc64le go build -o ../../ELF_file/bin/test10
CGO_ENABLED=0 GOOS=linux GOARCH=riscv64 go build -o ../../ELF_file/bin/test11
