DEPTH = 2000


def get_secrets():
    """
    Returns a list of secrets from the puzzle
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [int(line) for line in lines]


def evolve(secret):
    """
    Evolves the secret number
    :param secret:
    :return:
    """
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))

    return secret


def mix(a, secret):
    """
    Mixes the secret number with a
    :param a:
    :param secret:
    :return:
    """
    return a ^ secret


def prune(secret):
    """
    Prunes the secret number
    :param secret:
    :return:
    """
    return secret % 16777216


def find_most_bananas(secrets, depth):
    """
    Finds the most bananas one could get
    yummy...
    :param secrets:
    :param depth:
    :return:
    """
    sums = dict()

    for secret in secrets:
        seen = set()

        a = secret
        b = evolve(a)
        c = evolve(b)
        d = evolve(c)
        e = evolve(d)

        for _ in range(depth - 4):
            a, b, c, d, e = b, c, d, e, evolve(e)

            db = (b % 10) - (a % 10)
            dc = (c % 10) - (b % 10)
            dd = (d % 10) - (c % 10)
            de = (e % 10) - (d % 10)

            sequence = (db, dc, dd, de)

            if sequence in seen:
                continue

            seen.add(sequence)

            sums[sequence] = sums.setdefault(sequence, 0) + e % 10

    return max(sums.values())


def main():
    secrets = get_secrets()

    total = find_most_bananas(secrets, DEPTH)

    print(total)


if __name__ == "__main__":
    main()
