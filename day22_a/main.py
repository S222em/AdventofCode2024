DEPTH = 2000


def get_secrets():
    """
    Returns a list of secrets from the puzzle
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [int(line) for line in lines]


def find_secret_number_after(secret, depth):
    """
    Finds the secret number after x amount of evolves
    :param secret:
    :param depth:
    :return:
    """
    for _ in range(depth):
        secret = evolve(secret)

    return secret


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


def sum_secrets(secrets, depth):
    """
    Sums all secret numbers after x amount of evolves for each
    :param secrets:
    :param depth:
    :return:
    """
    total = 0

    for secret in secrets:
        total += find_secret_number_after(secret, depth)

    return total


def main():
    secrets = get_secrets()

    total = sum_secrets(secrets, DEPTH)

    print(total)


if __name__ == "__main__":
    main()
