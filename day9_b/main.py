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


def move_files(blocks: list[int]):
    """
    Moves files from the end to the first free space the whole file will fit in.
    :param blocks:
    :return:
    """
    last_file_id = None
    file_id = None
    file_end = None

    # Locate range of files in descending file_id order
    for i, block in enumerate(reversed(blocks)):
        if file_id is not None and file_id != block:
            blocks = move_file(len(blocks) - i, file_end + 1, blocks)
            last_file_id = file_id
            file_id = None

        if block is None:
            continue

        # Only reset the end of the file if the current block is smaller than the last_file_id
        # In case it's equal or larger we have already attempted to move this file
        if file_id is None and (last_file_id is None or block < last_file_id):
            file_id = block
            file_end = len(blocks) - i - 1

    return blocks


def move_file(start, end, blocks):
    """
    Moves a single file into the first available space the file fits in
    :param start:
    :param end:
    :param blocks:
    :return:
    """
    file_size = end - start

    free_start = None
    free_end = None

    # Find the first free space that is able to fit the whole file
    for i, block in enumerate(blocks):
        # We only want to move the file to the left, so if we go past the end of the file we stop.
        if i >= end:
            break

        # If we have found a large enough space we exit.
        if free_start is not None and i - free_start >= file_size:
            free_end = i
            break

        if block is not None:
            free_start = None
            continue

        if free_start is None:
            free_start = i

    if free_end is None:
        return blocks

    # Swap the empty space with the file
    blocks[free_start:free_end], blocks[start:end] = blocks[start:end], blocks[free_start:free_end]

    return blocks


def get_checksum(blocks):
    """
    Calculates the filesystem checksum for the given blocks
    :param blocks:
    :return:
    """
    checksum = 0

    for i, block in enumerate(blocks):
        if block is None:
            continue

        checksum += i * block

    return checksum


def main():
    disk_map = get_disk_map()

    blocks = expand_disk_map_into_blocks(disk_map)

    blocks = move_files(blocks)

    checksum = get_checksum(blocks)

    print(checksum)


if __name__ == "__main__":
    main()
