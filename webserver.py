#!/usr/bin/env python

#import logging

from webserver import *

if __name__ == '__main__':
    #logging.basicConfig(
    #    format="[%(asctime)s] %(name)s/%(levelname)-6s - %(message)s", 
    #    level=logging.CRITICAL,
    #    datefmt='%Y-%m-%d %H:%M:%S'
    #)
    # Only enable debug level for bbot
    #logger = logging.getLogger('bastardbot')
    #logger.setLevel(logging.DEBUG)
    
    print("Initializing BastardBot web server...")
    B = BastardBot()

    print("BastardBot server stopped.")
