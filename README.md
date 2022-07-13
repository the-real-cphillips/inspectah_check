# Inspectah/Scann

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
        * Specifically IIS 7.X or Nginx 1.7.X
    * Is the Directory Listing Available

Included in this is also a wrapper to leverage `scann`

This wrapper is `inspectah.py`

---

