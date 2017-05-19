"""This module manages the elections on the blockchain"""
import argparse
import binascii
import csv
import hashlib

import base58

# Update according to params.dat
__version__ = ['00', '8c', 'b5', 'd6']
__addressChecksum__ = '5afce7b2'

def main():
    """
    Reads arguments and handles application workflow
    """
    parser = argparse.ArgumentParser(
        description='Create new elections and assign one token to every pubkey'
    )
    parser.add_argument('--server', '-s')
    parser.add_argument('--token-name', '-n')
    parser.add_argument('--pubkeys', '-i')

    args = parser.parse_args()

    with open(args.pubkeys, 'rb') as csvfile:
        for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
            print pubkey_to_address(row[0])

def pubkey_to_address(pubkey):
    """
    Returns a valid address on the blockchain for pubkey
    According to http://www.multichain.com/developers/address-key-format/
    """
    # step 3
    pubkey_hash = hashlib.sha256(binascii.unhexlify(pubkey))
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(pubkey_hash.digest())

    # step 4
    pubkey160_hash = ripemd160.hexdigest()

    # step 5
    pubkey160_hash_w_version = ''
    for i in range(4):
        pubkey160_hash_w_version += __version__[i] + pubkey160_hash[(i*10):(i*10)+10]

    # step 6
    sha256_of_160hash = hashlib.sha256(binascii.unhexlify(pubkey160_hash_w_version))
    sha256_of_160hash.hexdigest()

    # step 7
    sha256_of_prev_sha256 = hashlib.sha256(sha256_of_160hash.digest())

    # step 8
    checksum = sha256_of_prev_sha256.hexdigest()[0:8]

    # step 9
    xor_checksum = '{:08x}'.format(int(int(checksum, 16) ^ int(__addressChecksum__, 16)))

    # step 10
    binary_address = pubkey160_hash_w_version + xor_checksum

    # step 11
    return base58.b58encode(binascii.unhexlify(binary_address))

if __name__ == '__main__':
    main()
