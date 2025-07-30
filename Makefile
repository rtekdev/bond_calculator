.PHONY: help
default: help

CC = gcc
SRC = src/logic/operations.c src/logic/inflation.c src/logic/bond_loader.c
OUT_DEV = my_app
OUT = my_app.so

help: 
	@echo	"Available Actions:"
	@echo	"	make build-app 	- Build application for .so file"
	@echo	"	make build 	- Build application for test C file"


build:
	$(CC) $(SRC) -o $(OUT_DEV) main.c -lm -lcurl -lcjson

build-app:
	$(CC) -shared -fPIC -O3 $(SRC) -o $(OUT) main.c -lm -lcurl -lcjson

