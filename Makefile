# ========= Tool / platform detection =========
ifeq ($(OS),Windows_NT)
    # ---- Windows (MinGW / MSYS2 / Git-Bash) ----
    EXE_EXT  := .exe
    SHLIB_EXT:= .dll
    SHFLAGS  := -shared              
    RM       := del /f /q            
    RMDIR    := rmdir /s /q
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Darwin)
        # ---------- macOS ----------
        SHLIB_EXT := .dylib
        SHFLAGS   := -dynamiclib -fPIC
    else
        # ---------- Linux ----------
        SHLIB_EXT := .so
        SHFLAGS   := -shared -fPIC
    endif
    EXE_EXT :=                     
    RM     := rm -f
    RMDIR  := rm -rf
endif

CC       := gcc
SRC      := src/logic/operations.c src/logic/inflation.c src/logic/bond_loader.c
LDFLAGS  := -lm -lcurl -lcjson
OUT_DEV  := my_app$(EXE_EXT)
OUT      := my_app$(SHLIB_EXT)

help:
	@echo "make build      - Build CLI test binary ($(OUT_DEV))"
	@echo "make build-app  - Build shared library   ($(OUT))"
	@echo "make clear      - Remove generated binaries"

build: $(SRC) main.c
	$(CC) $^ -o $(OUT_DEV) $(LDFLAGS)

build-app: $(SRC)
	$(CC) $(SHFLAGS) $^ -o $(OUT) $(LDFLAGS)

clear:
	-$(RMDIR) $(OUT_DEV) $(OUT)

.PHONY: help build build-app clear
