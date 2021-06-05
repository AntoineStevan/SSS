import argparse
import os

from shamir import make_random_shares, cut_into_chunks
from utils import StoreDictKeyPair, purify_text


def main():
    """
        ______________________________________________________TODO______________________________________________________

        Args:

        Return:
             ()_______________________________________________TODO______________________________________________________
    """
    parser = argparse.ArgumentParser("a parser to give names and priorities")
    parser.add_argument("--holders", "-H", action=StoreDictKeyPair, nargs="*",
                        metavar="KEY=VAL", help="to register names and priorities.")
    parser.add_argument("--secret", "-s", default=123456789, type=int,
                        help="the secret to be shared (int) (default: 123456789)")
    parser.add_argument("--name", "-n", default="secret", type=str,
                        help="the name of the secret (str) (default: 'secret')")
    parser.add_argument("--minimum_shares", "-m", type=int, default=3,
                        help="the number of keys required to crack the secret (int) (default: 3)")

    args = parser.parse_args()
    secret = args.secret

    nb_shares = sum([v for _, v in args.holders.items()])
    shares = make_random_shares(secret, minimum=args.minimum_shares, shares=nb_shares)

    for k, v in args.holders.items():
        print(f"{k}, here are your shares of the secret '{args.secret}' labeled '{args.name}'")

        directory = os.path.join(k.lower(), args.name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, "keys"), "w") as file:
            file.write(k + '\n')
            file.write(str(v) + '\n')

            for _ in range(v):
                identifier, key = shares.pop(0)
                file.write(str(identifier) + '\n')
                file.write(str(key) + '\n')
                print(f"\t- id: {identifier}, key: {key}")
        print()

    print(f"{', '.join(list(args.holders.keys()))}, the shares for your secret"
          f"({args.secret}) have been saved inside your personal vaults, under the '{args.name}' name.")


if __name__ == "__main__":
    main()
