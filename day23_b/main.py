from collections import defaultdict


def get_computers():
    """
    Returns all the connections between computers
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    computers = defaultdict(set)

    for line in lines:
        [left, right] = line.strip().split("-")
        computers[left].add(right)
        computers[right].add(left)

    return computers


def find_largest_lan_parties(party, possible, exclude, computers, parties):
    """
    Finds the largest lan parties that exist.
    Based on https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    :param party:
    :param possible:
    :param exclude:
    :param computers:
    :param parties:
    :return:
    """
    if not possible and not exclude:
        parties.append(party)
        return

    u = next(iter(possible | exclude))

    for computer in possible - computers[u]:
        find_largest_lan_parties(
            party | {computer},
            possible & computers[computer],
            exclude & computers[computer],
            computers,
            parties
        )
        possible.remove(computer)
        exclude.add(computer)


def find_largest_lan_party_password(computers):
    """
    Finds the password of the largest LAN party
    :param computers:
    :return:
    """
    parties = list()

    find_largest_lan_parties(set(), set(computers.keys()), set(), computers, parties)

    largest = max(parties, key=len)

    return get_party_password(largest)


def get_party_password(party):
    """
    Finds the password of the largest LAN party
    :param party:
    :return:
    """
    return ",".join(sorted(party))


def main():
    computers = get_computers()

    password = find_largest_lan_party_password(computers)

    print(password)


if __name__ == "__main__":
    main()
