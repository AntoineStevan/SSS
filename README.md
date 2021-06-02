# Shamir's secret sharing.

## 1. Installation.
Used modules:
- `argparse`
- `difflib`
- `random`
- `functools`

## 2. Run the code.
One can find some help for the main programs by running:
- `python src/make_shares.py -h` or `python src/make_shares.py --help`
- `python src/open_vault.py -h` or `python src/open_vault.py --help`

Example. Suppose Alice, Bob and Charlie want to share 987654321, by requiring at least 2 keys and with following priorities:
- Alice has priority 3.
- Bob has priority 1.
- Charlie has priority 1.

Note: if dave has priority `n`, dave will receive `n` distinct keys.

To simulate such a scenario:
- run `python src/make_shares.py --holders alice=3 bob=1 charlie=1 -s 987654321 -m 2`

Then, if any combination of the above members is here, run `python src/open_vault.py --present member1 member2`

For example `python src/open_vault.py -p alice` or `python src/open_vault.py -p alice charlie` will unlock the secret.  
But, `python src/open_vault.py -p bob charlie` won't.
