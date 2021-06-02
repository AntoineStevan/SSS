import argparse

from shamir import recover_secret


def main():
    """
        ______________________________________________________TODO______________________________________________________

        Args:

        Return:
             ()_______________________________________________TODO______________________________________________________
    """
    parser = argparse.ArgumentParser("a parser to give names and priorities")
<<<<<<< HEAD
    parser.add_argument("--present", "-p", default=[], nargs="+", help="to register names and priorities.")
=======
    parser.add_argument("--present", "-p", default=[], nargs="+", help="a list of names to reveal the code.")
>>>>>>> Shares in file + parser.

    args = parser.parse_args()

    identifiers = []
    keys = []

    for name in args.present:
        try:
            with open(f"./keys/{name.lower()}.keys", 'r') as file:
                # print(file.readline().strip(), "is here.")
                for _ in range(int(file.readline().strip())):
                    identifiers.append(int(file.readline().strip()))
                    keys.append(int(file.readline().strip()))
        except FileNotFoundError as fne:
            print(f"{name} should not be here ({fne})")

    shares = list(zip(identifiers, keys))
    for share in shares:
        print(share)

    secret = recover_secret(shares)
    print("secret:", secret, f"({len(shares)})")


if __name__ == "__main__":
    main()
