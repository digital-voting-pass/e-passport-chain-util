# digital-voting-pass-util

Simple command line utility to manage elections and voting tokens on the blockchain. Determines the wallet address for every public key listed in the CSV and issues a batch of new tokens with the given name. These tokens are distributed over the wallets.

Works seamlessly with Multichain.

## Usage

```
python create_elections.py -n gemeenteraadsverkiezingen-2018-ons-dorp -i data/pubkeys.csv
```