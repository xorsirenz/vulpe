#!/usr/bin/env python3
import os
import sys
from src import source

if __name__ == '__main__':
    try:
        source.main()
    except KeyboardInterrupt:
        print(f"\n[-] Vulpe shutting down..")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
