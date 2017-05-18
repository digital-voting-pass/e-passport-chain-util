import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Create new elections and assign one token to every pubkey')
    parser.add_argument('--server', '-s')
    parser.add_argument('--token-name', '-n')
    parser.add_argument('--pubkey-csv', '-i')

    args = parser.parse_args()

if __name__ == '__main__':
    main()