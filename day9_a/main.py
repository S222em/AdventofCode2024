def get_disk_map():
    """
    Returns the disk map
    :return:
    """
    with open("puzzle.txt") as file:
        disk_map = file.read().strip()

    return disk_map


def expand_disk_map_into_blocks(disk_map):
    """
    Expands the disk map into blocks.
    ABAB where A = file size and b = free size
    :param disk_map:
    :return:
    """
    file_count = 0
    blocks = list()

    for i, size in enumerate(disk_map):
        is_file = i % 2 == 0
        block_id = file_count if is_file else None
        blocks.extend([block_id] * int(size))
        if is_file:
            file_count += 1

    return blocks


def move_blocks(blocks):
    """
    Moves blocks from the end to the first free space until no blocks are left.
    :param blocks:
    :return:
    """
    j = 0

    for i, block in enumerate(reversed(blocks)):
        if block is None:
            continue

        j = advance_until_empty_block(j, blocks)

        if j >= len(blocks) - i - 1:
            break

        blocks[-i - 1], blocks[j] = blocks[j], blocks[-i - 1]

    return blocks


def advance_until_empty_block(j, blocks):
    """
    Advances index j until an empty block is reached
    :param j:
    :param blocks:
    :return:
    """
    while j < len(blocks):
        if blocks[j] is None:
            break

        j += 1

    return j


def get_checksum(blocks):
    """
    Calculates the filesystem checksum for the given blocks
    :param blocks:
    :return:
    """
    checksum = 0

    for i, block in enumerate(blocks):
        if block is None:
            break

        checksum += i * block

    return checksum


def main():
    disk_map = get_disk_map()

    blocks = expand_disk_map_into_blocks(disk_map)

    blocks = move_blocks(blocks)

    checksum = get_checksum(blocks)

    print(checksum)


if __name__ == "__main__":
    main()
