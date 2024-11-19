#!/usr/bin/env python3
from src.source import main, shutdown

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        shutdown()
