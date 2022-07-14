# Inspectah Check/Scann

[![Lint with Black](https://github.com/the-real-cphillips/inspectah_check/actions/workflows/black.yaml/badge.svg)](https://github.com/the-real-cphillips/inspectah_check/actions/workflows/black.yaml) [![Pytest](https://github.com/the-real-cphillips/inspectah_check/actions/workflows/pytest.yaml/badge.svg)](https://github.com/the-real-cphillips/inspectah_check/actions/workflows/pytest.yaml)

Wu-tang is Forever... Open ports (possibly) shouldn't be.

---

## Installation

1. Obtain Source 
1. `python3 -m venv env`
1. `. env/bin/activate`
1. `python3 -m pip install -r requirements.txt`

---

## Overview

In the `scann` Module (`scann.py`) there is a `HostScan` Class.

This class is responsible for:

* Instantiating an response object of a port scan using `socket`
* Determining Attributes we are looking for:
    * Server Type
        * Specifically IIS 7.X or Nginx 1.2.X
    * Is the Directory Listing Available

Included in this is also a wrapper to leverage `scann`

This wrapper is `inspectah_check.py`

---

## Usage

#### Parameters

* `-t`,`--ip`: Target IP, can be multiple seperated by a space
    * Example: `-t 127.0.0.1 192.168.22.111 10.96.1.59`
* `-s`, `--start_port`: Beginning Port Number
* `-e`, `--end_port`: Ending Port Number
    * NOTE: The end number should always be one more then you want  
      If you want your last port to be 8000, this value should be 8001


#### Help Text

```sh
> ./inspectah_check.py -h
usage: inspectah_check.py [-h] -t TARGETS [TARGETS ...] [-s START_PORT] [-e END_PORT]

Wu-tang is Forever... Open ports (possibly) shouldn't be
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⡀⠀⠀⠀
 ⠀⢀⣶⣶⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⡄⠀⠀
 ⠀⣼⣿⣿⣿⣿⣿⣿⣿⣷⣶⡤⠀⠀⠀⠀⢤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀
 ⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⢀⣀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀
 ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠰⣾⣿⣿⣷⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
 ⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
 ⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
 ⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀
 ⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀
 ⠀⠀⠀⠀⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⡄⠀⠀⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠀⣸⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

optional arguments:
  -h, --help            show this help message and exit
  -t TARGETS [TARGETS ...], --ip TARGETS [TARGETS ...]
                        IP Address to Scan
  -s START_PORT, --start_port START_PORT
                        Start of Port Range to Scan
  -e END_PORT, --end_port END_PORT
                        End of Port Range to Scan. Note: Don't Forget to Add 1 if the last port you want is 8080, make sure you set this to 8081

```

### Basic Usage

NOTE: This takes some time if you scan all the ports from 1-65535 as shown below.

```sh
> ./inspectah_check.py --ip 127.0.0.1

[I] Starting Scan 127.0.0.1
+--------+---------------------+-------------------+---------------+----------------+
|   Port | Has Server Header   | Has Server Type   | Server Type   | Can List Dir   |
+========+=====================+===================+===============+================+
|    631 | True                | False             |               | False          |
+--------+---------------------+-------------------+---------------+----------------+
|   8082 | True                | False             |               | False          |
+--------+---------------------+-------------------+---------------+----------------+
|   8085 | True                | True              | nginx/1.2.9   | True           |
+--------+---------------------+-------------------+---------------+----------------+
|  55008 | False               | False             |               | False          |
+--------+---------------------+-------------------+---------------+----------------+
Scan Time: 15.91 seconds

**** Total Run Time: 15.91 seconds ****
```

### Advanced Usage

```sh
./inspectah_check.py --ip 127.0.0.1 192.168.86.1 -s 8000 -e 8086

[I] Starting Scan 127.0.0.1
+--------+---------------------+-------------------+---------------+----------------+
|   Port | Has Server Header   | Has Server Type   | Server Type   | Can List Dir   |
+========+=====================+===================+===============+================+
|   8082 | True                | False             |               | False          |
+--------+---------------------+-------------------+---------------+----------------+
|   8085 | True                | True              | nginx/1.2.9   | True           |
+--------+---------------------+-------------------+---------------+----------------+
Scan Time: 0.18 seconds

[I] Starting Scan 192.168.86.1
+--------+---------------------+-------------------+---------------+----------------+
|   Port | Has Server Header   | Has Server Type   | Server Type   | Can List Dir   |
+========+=====================+===================+===============+================+
|   8080 | False               | False             |               | False          |
+--------+---------------------+-------------------+---------------+----------------+
|   8081 | False               | False             |               | False          |
+--------+---------------------+-------------------+---------------+----------------+
Scan Time: 1.05 seconds

**** Total Run Time: 1.23 seconds ****
```

## [TODO][todo]

## [Contribute!][contrib]

---
[contrib]: CONTRIBUTING.md
[todo]: CONTRIBUTING.md
