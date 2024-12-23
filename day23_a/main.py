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


def find_lan_parties(computers):
    """
    Finds LAN parties of 3
    :param computers:
    :return:
    """
    lan_parties = list()

    for computer, connections in computers.items():
        for connection in connections:
            intersection = connections.intersection(computers[connection])

            for intersect in intersection:
                party = {computer, connection, intersect}

                if party in lan_parties:
                    continue

                lan_parties.append(party)

    return lan_parties


def count_parties_with_t(lan_parties):
    """
    Count the amount of parties that have a computer that starts with 't'
    :param lan_parties:
    :return:
    """
    total = 0

    for party in lan_parties:
        for computer in party:
            if not computer.startswith("t"):
                continue

            total += 1
            break

    return total


def main():
    computers = get_computers()

    lan_parties = find_lan_parties(computers)

    total = count_parties_with_t(lan_parties)

    print(total)


if __name__ == "__main__":
    main()
