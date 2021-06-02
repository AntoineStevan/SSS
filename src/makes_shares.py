import argparse
from shamir import make_random_shares
from utils import StoreDictKeyPair


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
<<<<<<< HEAD
    parser.add_argument("--secret", "-s", type=int, default=123456789)
    parser.add_argument("--minimum_shares", "-m", type=int, default=3)
=======
    parser.add_argument("--secret", "-s", type=int, default=123456789,
                        help="the secret to be shared (int) (default: 123456789)")
    parser.add_argument("--minimum_shares", "-m", type=int, default=3,
                        help="the number of keys required to crack the secret (int) (default: 3)")
>>>>>>> Shares in file + parser.

    args = parser.parse_args()

    nb_shares = sum([v for k, v in args.holders.items()])
    shares = make_random_shares(args.secret, minimum=args.minimum_shares, shares=nb_shares)

    print('Shares:')
    if shares:
        for share in shares:
            print(f"{share[0]} -> {share[1]}")

    for k, v in args.holders.items():
        with open(f"./keys/{k.lower()}.keys", "w") as file:
            file.write(k + '\n')
            file.write(str(v) + '\n')
            for _ in range(v):
                identifier, key = shares.pop(0)
                file.write(str(identifier) + '\n')
                file.write(str(key) + '\n')


if __name__ == "__main__":
    main()
