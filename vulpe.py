#!/usr/bin/env python3
from src import source

if __name__ == '__main__':
    try:
        source.main()
    except KeyboardInterrupt:
        source.shutdown()
