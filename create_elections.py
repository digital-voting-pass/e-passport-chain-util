#!/usr/bin/env python

"""
This module manages the elections on the blockchain. It creates a new
batch of voting tokens and distributes it to the given pubkeys.
"""

import argparse
import binascii
import csv
import hashlib
import json
import logging

import base58
from Savoir import Savoir

__author__ = "Daan Middendorp"
__copyright__ = "Copyright 2017, Digital Voting Pass"
__credits__ = ["Wilko Meijer", "Daan Middendorp", "Jonathan Raes", "Rico Tubbing"]
__license__ = "GPL"
__version__ = "0.0.1"

def main():
    """
    Handles application workflow
    """
    addresses = get_addresses()
    issue_tokens(__args__.tokenname, len(addresses))
    grant_permissions(addresses)
    distribute_tokens(__args__.tokenname, addresses)

def distribute_tokens(name, addresses):
    """
    Send every address one token
    """
    success = 0
    for address in addresses:
        if isinstance(__api__.sendasset(address, name, 1), basestring):
            success += 1
    print str(success) + " token(s) distributed over " + str(len(addresses)) + " address(es)"

def grant_permissions(addresses):
    """
    Grant send and receive permissions to addresses
    """
    __api__.grant(", ".join(addresses), "send")
    __api__.grant(", ".join(addresses), "receive")

def issue_tokens(name, amount):
    """
    Create a transaction which issues n assets with the given name
    """
    # Get wallet address of host
    issue_permissions = __api__.listpermissions('issue')
    host_wallet_address = issue_permissions[0]['address']
    print "Host wallet address: " + host_wallet_address

    # Issue assets with given amount
    transaction = __api__.issue(host_wallet_address, name, amount, 1)
    if not isinstance(transaction, basestring):
        if transaction['error']['code'] == -705:
            raise Exception('Token already issued, try a different name')
    print str(amount) + " token(s) of " + name + " issued"
    return transaction

def get_addresses():
    """
    Converts the public keys in the csv to list of addresses
    """
    addresses = []
    with open(__args__.pubkeys, 'rb') as csvfile:
        for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
            addresses.append(pubkey_to_address(row[0], __config__))
    return addresses

def pubkey_to_address(pubkey, config):
    """
    Returns a valid address on the blockchain for pubkey
    According to http://www.multichain.com/developers/address-key-format/
    """
    # Step 3
    pubkey_hash = hashlib.sha256(binascii.unhexlify(pubkey))
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(pubkey_hash.digest())

    # Step 4
    pubkey160_hash = ripemd160.hexdigest()

    # Step 5
    pubkey160_hash_w_version = ''
    for i in range(4):
        pubkey160_hash_w_version += config['version'][i] + pubkey160_hash[(i*10):(i*10)+10]

    # Step 6
    sha256_of_160hash = hashlib.sha256(binascii.unhexlify(pubkey160_hash_w_version))
    sha256_of_160hash.hexdigest()

    # Step 7
    sha256_of_prev_sha256 = hashlib.sha256(sha256_of_160hash.digest())

    # Step 8
    checksum = sha256_of_prev_sha256.hexdigest()[0:8]

    # Step 9
    xor_checksum = '{:08x}'.format(int(int(checksum, 16) ^ int(config['addresschecksum'], 16)))

    # Step 10
    binary_address = pubkey160_hash_w_version + xor_checksum

    # Step 11
    return base58.b58encode(binascii.unhexlify(binary_address))

def parse_args():
    """
    Return parsed arguments as object
    """
    parser = argparse.ArgumentParser(
        description='Create new elections and assign one token to every pubkey'
    )
    parser.add_argument('--tokenname', '-n', required=True)
    parser.add_argument('--pubkeys', '-i', required=True)
    parser.add_argument('--config', '-c', required=False, default="config.json")

    return parser.parse_args()

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    __args__ = parse_args()
    __config__ = json.load(open(__args__.config))
    __api__ = Savoir(
        __config__['rpcuser'],
        __config__['rpcpasswd'],
        __config__['rpchost'],
        __config__['rpcport'],
        __config__['chainname']
    )
    main()
