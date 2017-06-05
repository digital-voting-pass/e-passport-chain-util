#!/usr/bin/env python

"""
This module creates a keypair which can be used to
simulate a machine readable travel document.
"""

import argparse
import binascii
import json

from ecdsa import BRAINPOOLP320r1, SigningKey

from create_elections import pubkey_to_address

__author__ = "Daan Middendorp"
__copyright__ = "Copyright 2017, Digital Voting Pass"
__credits__ = ["Wilko Meijer", "Daan Middendorp", "Jonathan Raes", "Rico Tubbing"]
__license__ = "GPL"
__version__ = "0.0.1"

def main():
    """
    Handles the application workflow
    """
    signing_key = SigningKey.generate(curve=BRAINPOOLP320r1)
    verifying_key = signing_key.get_verifying_key()
    print "Address: " + pubkey_to_address(binascii.hexlify(
        "04" + verifying_key.to_string()), __config__)
    print "Public: 04" + binascii.hexlify(verifying_key.to_string())
    print "Private: " + binascii.hexlify(signing_key.to_string())

def parse_args():
    """
    Return parsed arguments as object
    """
    parser = argparse.ArgumentParser(
        description='Create a new keypair to simulate a passport'
    )
    parser.add_argument('--config', '-c', required=False, default="config.json")
    return parser.parse_args()

if __name__ == '__main__':
    __args__ = parse_args()
    __config__ = json.load(open(__args__.config))
    main()
