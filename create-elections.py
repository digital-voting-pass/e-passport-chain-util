import os
import argparse
import csv
import asn1
import base58
import binascii
import hashlib
from pypassport import epassport, reader
from pyasn1.codec.der.decoder import decode
from pyasn1.type import univ, namedtype

# Update according to params.dat
version = ['00','8c','b5','d6']
addressChecksum = '5afce7b2'

def main():
    parser = argparse.ArgumentParser(description='Create new elections and assign one token to every pubkey')
    parser.add_argument('--server', '-s')
    parser.add_argument('--token-name', '-n')
    parser.add_argument('--pubkeys', '-i')

    args = parser.parse_args()

    with open(args.pubkeys, 'rb') as csvfile:
        for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
            print pubkey_to_address(row[0])


def pubkey_to_address(pubkey):

    # step 3
    pubkeyHash = hashlib.sha256(binascii.unhexlify(pubkey))
    h = hashlib.new('ripemd160')
    h.update(pubkeyHash.digest())

    # step 4
    pubkey160Hash = h.hexdigest()

    # step 5
    pubkey160HashWithVersion = ''
    for x in range(4):
      pubkey160HashWithVersion = pubkey160HashWithVersion + version[x] + pubkey160Hash[(x*10):(x*10)+10] 

    # step 6
    sha256of160hash = hashlib.sha256(binascii.unhexlify(pubkey160HashWithVersion))
    sha256of160hash.hexdigest()

    # step 7
    sha256ofPrevSha256 = hashlib.sha256(sha256of160hash.digest())

    # step 8
    checksum = sha256ofPrevSha256.hexdigest()[0:8]    

    # step 9
    xorChecksum = '{:08x}'.format(int(int(checksum, 16) ^ int(addressChecksum, 16)))

    # step 10 
    binaryAddress = pubkey160HashWithVersion + xorChecksum

    # step 11
    return base58.b58encode(binascii.unhexlify(binaryAddress))

if __name__ == '__main__':
    main()