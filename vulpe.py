#!/usr/bin/env python3
from src.source import main, verify_config, shutdown

if __name__ == '__main__':
    try:
        verify_config()
        main()
    except KeyboardInterrupt:
        shutdown()
