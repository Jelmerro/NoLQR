# Util file of NoLQR, QR code generation lighter than an unladen swallow
# Made by Jelmerro, see README.md for more details
# MIT, see LICENSE for details
# https://github.com/Jelmerro/NoLQR for updates

from . import constants


def best_mode(data):
    """ Picks the best mode for the input data

    If the data only contains digits, use numeric.
    If the data can be encoded using alphanumeric, use it.
    To decide between kanji and binary,
    the data is encoded in utf-8 or iso-8859-1 first.
    If there is a single character that doesn't fit,
    the data will be encoded with shift-jis.
    If that works, the encoding mode will be kanji,
    but if it fails, binary will be used.
    Binary is the default, when none of the other modes would work.
    During the encoding of kanji,
    the mode might switch back to binary when needed.
    """
    if data.isdigit():
        return "numeric"
    if all(c in set(constants.ALPHA_TABLE) for c in data):
        return "alphanumeric"
    total_length = 0
    for character in data.encode(constants.ENCODING):
        total_length += len("{:08b}".format(character))
    if total_length > len(data) * 8:
        try:
            data.encode("shift-jis")
            return "kanji"
        except UnicodeEncodeError:
            pass
    return "binary"


def total_bits(version, mode, number_of_characters):
    """ Calculates the total number of bits

    Depending on the mode,
    the number of bits per character is different.
    For (alpha)numeric the characters are encoded in groups.
    This means that if the data doesn't fit perfecly,
    the length for the last character(s) is more.
    Mode indicator takes up 4 bits.
    Character count indictor takes up 16 bits at the most.
    The number of data bits is added and forms the total bits.
    """
    total = 0
    if mode == "numeric":
        total += 10 * int(number_of_characters / 3)
        if number_of_characters % 3 == 1:
            total += 4
        if number_of_characters % 3 == 2:
            total += 7
    if mode == "alphanumeric":
        total += 11 * int(number_of_characters / 2)
        if number_of_characters % 2 == 1:
            total += 6
    if mode == "binary":
        total += 8 * number_of_characters
    if mode == "kanji":
        total += 13 * number_of_characters
    return 4 + character_count_indicator_length(mode, version) + total


def version(mode, number_of_characters, error_level):
    """ Calculates the best version

    The amount of data a version can hold,
    depends on the error correction level.
    The length of the data of a version,
    is compared to the storage capacity.
    If it doesn't fit, the next version will be tried.
    When the data doesn't fit any version,
    a RuntimeError informs the user of this.
    """
    for i in range(1, 41):
        total = total_bits(i, mode, number_of_characters)
        if total <= constants.VERSIONS[i][error_level]:
            return i
    if error_level == "L":
        raise RuntimeError("Provided data too big for any QR version")
    raise RuntimeError("Provided data too big for any QR version, "
                       "try a lower error correction level than "
                       "{}".format(error_level))


def character_count_indicator_length(mode, version):
    """ Calculates the character count indicator length

    Depending on the version used,
    the length of the indicator is different.
    """
    size = ""
    if version < 10:
        size = "small"
    elif version > 26:
        size = "large"
    else:
        size = "medium"
    return constants.MODES[mode]["cc_indicator_length"][size]


def width(version):
    """ Calculates the width of a version

    The width of version 1 is 21, version 2 is 25, 3 is 29 etc.
    """
    return 17 + 4 * version

def character_count_indicator(mode, number_of_characters, version):
    """ Generates the character count indicator

    First the desired length is set,
    which will be used in the formatter string.
    Lastly the formatter string is filled with the character count.
    """
    desired_length = character_count_indicator_length(mode, version)
    formatter = "{{:0{}b}}".format(desired_length)
    indicator = formatter.format(number_of_characters)
    return indicator


def interleave_codewords(data_blocks, error_blocks):
    """ Interleaves all the codeblocks

    First the data codewords for each block are added as follows:
    block 1 word 1
    block 2 word 1
    block 1 word 2
    etc.
    The length of the blocks is version depended,
    and even in the same version there can be different sized blocks.
    After all data blocks have been interleaved,
    the same is done for all error blocks.
    The error blocks will be added after all data blocks.
    """
    biggest_block = len(max(data_blocks, key=len))
    output = ""
    for i in range(0, biggest_block):
        for block in data_blocks:
            if i < len(block):
                output += block[i]
    biggest_block = len(max(error_blocks, key=len))
    for i in range(0, biggest_block):
        for block in error_blocks:
            if i < len(block):
                output += block[i]
    return output


def add_format_info(matrix, width, format_string):
    """ Adds the format string to the matrix

    There are two location in the matrix,
    where the format string will be placed.
    One around the topleft finder pattern,
    and the other is next to the other two finder patterns.
    The format string itself is provided as an argument,
    and are stored in the constants.
    """
    x = 8
    for base_y in range(0, 15):
        if base_y > 7:
            y = base_y + width - 15
        elif base_y > 5:
            y = base_y + 1
        else:
            y = base_y
        matrix[y][x] = int(format_string[14 - base_y])
    y = 8
    for base_x in range(0, 15):
        if base_x > 7:
            x = base_x + width - 15
        elif base_x > 5:
            x = base_x + 1
        else:
            x = base_x
        matrix[y][x] = int(format_string[base_x])
    return matrix


def generate_blocks(codewords, info):
    """ Spread the codewords across blocks

    All the codewords are be placed into blocks,
    and the error blocks are generated from them.
    """
    data_blocks = []
    error_blocks = []
    block_index = 0
    word_index = 0
    for block in range(0, info[1]):
        data_blocks.append([])
        for _ in range(0, info[2]):
            data_blocks[block_index].append(codewords[word_index])
            word_index += 1
        error_blocks.append(new_error_block(data_blocks[block_index], info))
        block_index += 1
    for block in range(0, info[3]):
        data_blocks.append([])
        for _ in range(0, info[4]):
            data_blocks[block_index].append(codewords[word_index])
            word_index += 1
        error_blocks.append(new_error_block(data_blocks[block_index], info))
        block_index += 1
    return data_blocks, error_blocks


def new_error_block(data_block, info):
    """ Create a new error correction block

    Creates a new error correction block,
    according to the Reed-Solomon error correction.
    The process itself is very complicated,
    and more information on it can be found online.
    """
    block = data_block[:]
    for item in block:
        block[block.index(item)] = int(item, 2)
    block.extend([0] * (info[0]))
    gen_result = [0] * len(constants.POLYNOMIALS[info[0]])
    for i in data_block:
        coefficient = block.pop(0)
        if coefficient == 0:
            continue
        alpha_exp = constants.GALOIS_INV[coefficient]
        for n in range(len(constants.POLYNOMIALS[info[0]])):
            gen_result[n] = alpha_exp + constants.POLYNOMIALS[info[0]][n]
            gen_result[n] = constants.GALOIS[gen_result[n] % 255]
            block[n] = gen_result[n] ^ block[n]
    if len(block) < len(data_block):
        block.extend([0] * (len(data_block) - len(block)))
    for item in block:
        block[block.index(item)] = "{:08b}".format(item)
    return block


def pad_zeros(data, max_bytes):
    """ Pad extra zeros and data

    If the data capacity isn't fully used,
    a terminator pattern is added at the end (0000).
    When there is less than 4 bits left,
    the rest of the space is filled with zeros.
    After that, the data is filled with zeros,
    to make the length a multiple of eight.
    When there is still space left,
    the "no data" pattern is added:
    (11101100 and 00010001 alternated)
    """
    spare_bits = max_bytes - len(data)
    if spare_bits > 4:
        data += "0" * 4
    else:
        data += "0" * spare_bits
    if len(data) % 8 != 0:
        pad_to_eight_number = 8 - len(data) % 8
        data += "0" * pad_to_eight_number
    while len(data) < max_bytes:
        data += "11101100"
        if len(data) < max_bytes:
            data += "00010001"
    return data
