#!/bin/python

"""
Calculate address from public key according to:
http://www.multichain.com/developers/address-key-format/
"""

import argparse
import json

from pyasn1.codec.der.decoder import decode
from pypassport import epassport, reader

from create_elections import pubkey_to_address

__author__ = "Daan Middendorp"
__copyright__ = "Copyright 2017, Digital Voting Pass"
__credits__ = ["Wilko Meijer", "Daan Middendorp", "Jonathan Raes", "Rico Tubbing"]
__license__ = "GPL"
__version__ = "0.0.1"

def main():
    """
    Handles the basic workflow
    """
    passport_reader = reader.ReaderManager().waitForCard(10)
    mrz = "" # enter last line of MRZ here
    passport = epassport.EPassport(passport_reader, mrz)

    passport.doBasicAccessControl()
    public = passport._getDG(15).body

    received_record = decode(public)[0]

    bit_list = received_record.__getitem__(1)
    bits = ''
    for bit in bit_list:
        bits = bits + str(bit)

    # step 2
    pubkey = hex(int(bits, 2))[2:-1]

    print "The multichain address of document " + mrz[:9] + ":"
    print pubkey_to_address(pubkey, __config__)

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
