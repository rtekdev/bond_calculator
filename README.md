# Polish Bond Calculator

An advanced compound interest calculator that estimates profitability of a safe investment strategy. It tells you interest-rate scenarios, total profit, inflation loss, etc.

## Table of Contents
-  [Prerequisites](#prerequisites)
-  [Installation](#installation)
-  [Technologies Used](#technologies-used)

## Prerequisites
- **Python 3.10+**
- **Make** (for convenience targets)

## Installation
> At the start, you need to install:
```bash
sudo apt install -y libcurl4-openssl-dev libcjson-dev
```

> To use, download the files or clone the repository
- Clone the repo:
  ```bash
  git clone https://github.com/rtekdev/bond_calculator.git
  cd bond_calculator
  ```

Two available routes:

A. Running the Front-end version
  1. ``make build-app``
  2. ``python3`` OR ``python main.py``

B. Running only logic (C testing)
  1. ``make build``
  2. ``./my_app``

Additional to clear created files inside terminal write:

``make clear``

## Technologies Used

1. **C** - All logic.
2. **Python** - Front-end with PyQt6.
3. **Python with ctypes** connection
4. **C read .json files**
5. **C fetch GUS API**
