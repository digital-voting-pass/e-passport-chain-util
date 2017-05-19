"""This module manages the elections on the blockchain"""
import argparse
import binascii
import csv
import hashlib

import base58
from Savoir import Savoir

# Update according to params.dat
__version__ = ['00', '8c', 'b5', 'd6']
__addresschecksum__ = '5afce7b2'
__rpcuser__ = 'multichainrpc'
__rpcpasswd__ = 'YoUrLoNgRpCpAsSwOrD'
__rpchost__ = 'localhost'
__rpcport__ = '22335'
__chainname__ = 'myChain'

def main():
    """
    Reads arguments and handles application workflow
    """
    parser = argparse.ArgumentParser(
        description='Create new elections and assign one token to every pubkey'
    )
    parser.add_argument('--token-name', '-n')
    parser.add_argument('--pubkeys', '-i')

    args = parser.parse_args()

    with open(args.pubkeys, 'rb') as csvfile:
        for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
            print pubkey_to_address(row[0])

    api = Savoir(__rpcuser__, __rpcpasswd__, __rpchost__, __rpcport__, __chainname__)
    api.getinfo()

def pubkey_to_address(pubkey):
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
        pubkey160_hash_w_version += __version__[i] + pubkey160_hash[(i*10):(i*10)+10]

    # Step 6
    sha256_of_160hash = hashlib.sha256(binascii.unhexlify(pubkey160_hash_w_version))
    sha256_of_160hash.hexdigest()

    # Step 7
    sha256_of_prev_sha256 = hashlib.sha256(sha256_of_160hash.digest())

    # Step 8
    checksum = sha256_of_prev_sha256.hexdigest()[0:8]

    # Step 9
    xor_checksum = '{:08x}'.format(int(int(checksum, 16) ^ int(__addresschecksum__, 16)))

    # Step 10
    binary_address = pubkey160_hash_w_version + xor_checksum

    # Step 11
    return base58.b58encode(binascii.unhexlify(binary_address))

if __name__ == '__main__':
    main()
