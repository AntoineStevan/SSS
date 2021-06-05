"""
The following Python implementation of Shamir's Secret Sharing is
released into the Public Domain under the terms of CC0 and OWFa:
https://creativecommons.org/publicdomain/zero/1.0/
http://www.openwebfoundation.org/legal/the-owf-1-0-agreements/owfa-1-0

See the bottom few lines for usage. Tested on Python 2 and 3.
"""

import random
import functools

# 12th Mersenne Prime
# (for this application we want a known prime number as close as
# possible to our security level; e.g.  desired security level of 128
# bits -- too large and all the ciphertext is large; too small and
# security is compromised)
import numpy as np

from utils import strad

_PRIME = 2 ** 127 - 1
# 13th Mersenne Prime is 2**521 - 1

_RINT = functools.partial(random.SystemRandom().randint, 0)


def _combine_bytes(_bytes):
    """
        Takes an array of bytes and combine them into a single integer. This operation wan be seen as a concatenation
        of the binary representations of the bytes.

        Args:
            _bytes (list of integers 0 <= i <= 255): the bytes to combine.

        Return:
             (int) the final integer, e.g. if one wants to combine 24, 3 and 217,
                the result will be 24*1 + 3*256^2 + 217*256^3.
    """
    return np.sum(np.array(_bytes) * np.array([256**k for k in range(len(_bytes))]))


def _decombine_integer(integer):
    """
        Decombines an integer into an array of bytes, such that integer = _combine_bytes(_decombine_integer(integer)).

        Args:
            integer (int): the integer to decombine.

        Return:
             (list of integers 0 <= i <= 255) the list of bytes composing the original integer.
    """
    _bytes = []
    while integer > 0:
        _bytes.append(integer % 256)
        integer //= 256
    return _bytes


def cut_into_chunks(secret, chunk_size=-1):
    """
        Cuts a given secret into chunk of given size.

        Args:
            secret (str): the secret to cut in parts.

        Return:
             (list of integers) the list of chunk secrets.
    """
    s_bytes = [ord(byte) for byte in secret]

    if chunk_size < 1:
        if strad(secret).__class__.__name__ == "int":
            return int(secret)
        else:
            return _combine_bytes(s_bytes)

    if strad(secret).__class__.__name__ == "int":
        s_bytes = _decombine_integer(int(secret))

    head_bytes_length = len(s_bytes) % chunk_size
    chunks = [s_bytes[:head_bytes_length]] if head_bytes_length else []
    for i in range(head_bytes_length, len(s_bytes), chunk_size):
        chunks += [s_bytes[i:i+chunk_size]]

    return [_combine_bytes(chunk) for chunk in chunks]


def _eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    """
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


def make_random_shares(secret, minimum, shares, prime=_PRIME):
    """
    Generates a random shamir pool for a given secret, returns share points.
    """
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")

    poly = [secret] + [_RINT(prime - 1) for i in range(minimum - 1)]
    points = [(i, _eval_at(poly, i, prime)) for i in range(1, shares + 1)]
    return points


def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    """Compute num / den modulo prime p

    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"

    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(np.product([x - o for o in others]))
        dens.append(np.product([cur - o for o in others]))
    den = np.product(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p


def recover_secret(shares, prime=_PRIME):
    """
    Recover the secret from share points
    (x, y points on the polynomial).
    """
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)
