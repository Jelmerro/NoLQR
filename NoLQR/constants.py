# Constants of NoLQR, QR code generation lighter than an unladen swallow
# Made by Jelmerro, see README.md for more details
# MIT, see LICENSE for details
# https://github.com/Jelmerro/NoLQR for updates

# Different input data modes and the mode indicator for them,
# Along with the character count indicator length
MODES = {
    "numeric": {
        "mode_indicator": "0001",
        "cc_indicator_length": {"small": 10, "medium": 12, "large": 14}
    },
    "alphanumeric": {
        "mode_indicator": "0010",
        "cc_indicator_length": {"small": 9, "medium": 11, "large": 13}
    },
    "binary": {
        "mode_indicator": "0100",
        "cc_indicator_length": {"small": 8, "medium": 16, "large": 16}
    },
    "kanji": {
        "mode_indicator": "1000",
        "cc_indicator_length": {"small": 8, "medium": 10, "large": 12}
    }
}

# The encoding type of the binary can be changed here.
# While the official QR spec defaults to iso-8859-1,
# there are some reasons to consider utf-8.
# If iso-8859-1 is used, uncommon characters can cause a UnicodeEncodeError.
# Some examples from the example_usage.py will stop working as well.
# Carolyn Eby's tutorial (see readme) mentions the possibility of using utf-8,
# and some other tutorials even recommend it over iso-8859-1.
ENCODING = "utf-8"  # utf-8 or iso-8859-1

# Alphanumeric code conversion table
# A mapping for all the possible characters in alphanumeric encoding
# This table is also used to check if the data only uses these characters.
# See util.best_mode for the implementation of this.
ALPHA_TABLE = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16,
    "H": 17, "I": 18, "J": 19, "K": 20, "L": 21, "M": 22, "N": 23, "O": 24,
    "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30, "V": 31, "W": 32,
    "X": 33, "Y": 34, "Z": 35, " ": 36, "$": 37, "%": 38, "*": 39, "+": 40,
    "-": 41, ".": 42, "/": 43, ":": 44
}

# Generic version information
# Data sizes in bits for the different ECC Levels (L, M, Q, H)
# The version string or mask pattern (pattern)
# Location of the alignment patterns (alignment)
VERSIONS = {
    1: {
        "alignment": [],
        "L": 152,
        "M": 128,
        "Q": 104,
        "H": 72
    },
    2: {
        "alignment": [6, 18],
        "L": 272,
        "M": 224,
        "Q": 176,
        "H": 128
    },
    3: {
        "alignment": [6, 22],
        "L": 440,
        "M": 352,
        "Q": 272,
        "H": 208
    },
    4: {
        "alignment": [6, 26],
        "L": 640,
        "M": 512,
        "Q": 384,
        "H": 288
    },
    5: {
        "alignment": [6, 30],
        "L": 864,
        "M": 688,
        "Q": 496,
        "H": 368
    },
    6: {
        "alignment": [6, 34],
        "L": 1088,
        "M": 864,
        "Q": 608,
        "H": 480
    },
    7: {
        "alignment": [6, 22, 38],
        "pattern": "000111110010010100",
        "L": 1248,
        "M": 992,
        "Q": 704,
        "H": 528
    },
    8: {
        "alignment": [6, 24, 42],
        "pattern": "001000010110111100",
        "L": 1552,
        "M": 1232,
        "Q": 880,
        "H": 688
    },
    9: {
        "alignment": [6, 26, 46],
        "pattern": "001001101010011001",
        "L": 1856,
        "M": 1456,
        "Q": 1056,
        "H": 800
    },
    10: {
        "alignment": [6, 28, 50],
        "pattern": "001010010011010011",
        "L": 2192,
        "M": 1728,
        "Q": 1232,
        "H": 976
    },
    11: {
        "alignment": [6, 30, 54],
        "pattern": "001011101111110110",
        "L": 2592,
        "M": 2032,
        "Q": 1440,
        "H": 1120
    },
    12: {
        "alignment": [6, 32, 58],
        "pattern": "001100011101100010",
        "L": 2960,
        "M": 2320,
        "Q": 1648,
        "H": 1264
    },
    13: {
        "alignment": [6, 34, 62],
        "pattern": "001101100001000111",
        "L": 3424,
        "M": 2672,
        "Q": 1952,
        "H": 1440
    },
    14: {
        "alignment": [6, 26, 46, 66],
        "pattern": "001110011000001101",
        "L": 3688,
        "M": 2920,
        "Q": 2088,
        "H": 1576
    },
    15: {
        "alignment": [6, 26, 48, 70],
        "pattern": "001111100100101000",
        "L": 4184,
        "M": 3320,
        "Q": 2360,
        "H": 1784
    },
    16: {
        "alignment": [6, 26, 50, 74],
        "pattern": "010000101101111000",
        "L": 4712,
        "M": 3624,
        "Q": 2600,
        "H": 2024
    },
    17: {
        "alignment": [6, 30, 54, 78],
        "pattern": "010001010001011101",
        "L": 5176,
        "M": 4056,
        "Q": 2936,
        "H": 2264
    },
    18: {
        "alignment": [6, 30, 56, 82],
        "pattern": "010010101000010111",
        "L": 5768,
        "M": 4504,
        "Q": 3176,
        "H": 2504
    },
    19: {
        "alignment": [6, 30, 58, 86],
        "pattern": "010011010100110010",
        "L": 6360,
        "M": 5016,
        "Q": 3560,
        "H": 2728
    },
    20: {
        "alignment": [6, 34, 62, 90],
        "pattern": "010100100110100110",
        "L": 6888,
        "M": 5352,
        "Q": 3880,
        "H": 3080
    },
    21: {
        "alignment": [6, 28, 50, 72, 94],
        "pattern": "010101011010000011",
        "L": 7456,
        "M": 5712,
        "Q": 4096,
        "H": 3248
    },
    22: {
        "alignment": [6, 26, 50, 74, 98],
        "pattern": "010110100011001001",
        "L": 8048,
        "M": 6256,
        "Q": 4544,
        "H": 3536
    },
    23: {
        "alignment": [6, 30, 54, 78, 102],
        "pattern": "010111011111101100",
        "L": 8752,
        "M": 6880,
        "Q": 4912,
        "H": 3712
    },
    24: {
        "alignment": [6, 28, 54, 80, 106],
        "pattern": "011000111011000100",
        "L": 9392,
        "M": 7312,
        "Q": 5312,
        "H": 4112
    },
    25: {
        "alignment": [6, 32, 58, 84, 110],
        "pattern": "011001000111100001",
        "L": 10208,
        "M": 8000,
        "Q": 5744,
        "H": 4304
    },
    26: {
        "alignment": [6, 30, 58, 86, 114],
        "pattern": "011010111110101011",
        "L": 10960,
        "M": 8496,
        "Q": 6032,
        "H": 4768
    },
    27: {
        "alignment": [6, 34, 62, 90, 118],
        "pattern": "011011000010001110",
        "L": 11744,
        "M": 9024,
        "Q": 6464,
        "H": 5024
    },
    28: {
        "alignment": [6, 26, 50, 74, 98, 122],
        "pattern": "011100110000011010",
        "L": 12248,
        "M": 9544,
        "Q": 6968,
        "H": 5288
    },
    29: {
        "alignment": [6, 30, 54, 78, 102, 126],
        "pattern": "011101001100111111",
        "L": 13048,
        "M": 10136,
        "Q": 7288,
        "H": 5608
    },
    30: {
        "alignment": [6, 26, 52, 78, 104, 130],
        "pattern": "011110110101110101",
        "L": 13880,
        "M": 10984,
        "Q": 7880,
        "H": 5960
    },
    31: {
        "alignment": [6, 30, 56, 82, 108, 134],
        "pattern": "011111001001010000",
        "L": 14744,
        "M": 11640,
        "Q": 8264,
        "H": 6344
    },
    32: {
        "alignment": [6, 34, 60, 86, 112, 138],
        "pattern": "100000100111010101",
        "L": 15640,
        "M": 12328,
        "Q": 8920,
        "H": 6760
    },
    33: {
        "alignment": [6, 30, 58, 86, 114, 142],
        "pattern": "100001011011110000",
        "L": 16568,
        "M": 13048,
        "Q": 9368,
        "H": 7208
    },
    34: {
        "alignment": [6, 34, 62, 90, 118, 146],
        "pattern": "100010100010111010",
        "L": 17528,
        "M": 13800,
        "Q": 9848,
        "H": 7688
    },
    35: {
        "alignment": [6, 30, 54, 78, 102, 126, 150],
        "pattern": "100011011110011111",
        "L": 18448,
        "M": 14496,
        "Q": 10288,
        "H": 7888
    },
    36: {
        "alignment": [6, 24, 50, 76, 102, 128, 154],
        "pattern": "100100101100001011",
        "L": 19472,
        "M": 15312,
        "Q": 10832,
        "H": 8432
    },
    37: {
        "alignment": [6, 28, 54, 80, 106, 132, 158],
        "pattern": "100101010000101110",
        "L": 20528,
        "M": 15936,
        "Q": 11408,
        "H": 8768
    },
    38: {
        "alignment": [6, 32, 58, 84, 110, 136, 162],
        "pattern": "100110101001100100",
        "L": 21616,
        "M": 16816,
        "Q": 12016,
        "H": 9136
    },
    39: {
        "alignment": [6, 26, 54, 82, 110, 138, 166],
        "pattern": "100111010101000001",
        "L": 22496,
        "M": 17728,
        "Q": 12656,
        "H": 9776
    },
    40: {
        "alignment": [6, 30, 58, 86, 114, 142, 170],
        "pattern": "101000110001101001",
        "L": 23648,
        "M": 18672,
        "Q": 13328,
        "H": 10208
    }
}

# Error correction and block information
# For each error level, the following numbers are stored:
# number of EC codewords per block
# number of block for group 1
# number of data codewords in each group 1 block
# number of block for group 2
# number of data codewords in each group 2 block
ERROR_CORRECTION_BLOCKS = {
    1: {
        "L": [7, 1, 19, 0, 0],
        "M": [10, 1, 16, 0, 0],
        "Q": [13, 1, 13, 0, 0],
        "H": [17, 1, 9, 0, 0]
    },
    2: {
        "L": [10, 1, 34, 0, 0],
        "M": [16, 1, 28, 0, 0],
        "Q": [22, 1, 22, 0, 0],
        "H": [28, 1, 16, 0, 0]
    },
    3: {
        "L": [15, 1, 55, 0, 0],
        "M": [26, 1, 44, 0, 0],
        "Q": [18, 2, 17, 0, 0],
        "H": [22, 2, 13, 0, 0]
    },
    4: {
        "L": [20, 1, 80, 0, 0],
        "M": [18, 2, 32, 0, 0],
        "Q": [26, 2, 24, 0, 0],
        "H": [16, 4, 9, 0, 0]
    },
    5: {
        "L": [26, 1, 108, 0, 0],
        "M": [24, 2, 43, 0, 0],
        "Q": [18, 2, 15, 2, 16],
        "H": [22, 2, 11, 2, 12]
    },
    6: {
        "L": [18, 2, 68, 0, 0],
        "M": [16, 4, 27, 0, 0],
        "Q": [24, 4, 19, 0, 0],
        "H": [28, 4, 15, 0, 0]
    },
    7: {
        "L": [20, 2, 78, 0, 0],
        "M": [18, 4, 31, 0, 0],
        "Q": [18, 2, 14, 4, 15],
        "H": [26, 4, 13, 1, 14]
    },
    8: {
        "L": [24, 2, 97, 0, 0],
        "M": [22, 2, 38, 2, 39],
        "Q": [22, 4, 18, 2, 19],
        "H": [26, 4, 14, 2, 15]
    },
    9: {
        "L": [30, 2, 116, 0, 0],
        "M": [22, 3, 36, 2, 37],
        "Q": [20, 4, 16, 4, 17],
        "H": [24, 4, 12, 4, 13]
    },
    10: {
        "L": [18, 2, 68, 2, 69],
        "M": [26, 4, 43, 1, 44],
        "Q": [24, 6, 19, 2, 20],
        "H": [28, 6, 15, 2, 16]
    },
    11: {
        "L": [20, 4, 81, 0, 0],
        "M": [30, 1, 50, 4, 51],
        "Q": [28, 4, 22, 4, 23],
        "H": [24, 3, 12, 8, 13]
    },
    12: {
        "L": [24, 2, 92, 2, 93],
        "M": [22, 6, 36, 2, 37],
        "Q": [26, 4, 20, 6, 21],
        "H": [28, 7, 14, 4, 15]
    },
    13: {
        "L": [26, 4, 107, 0, 0],
        "M": [22, 8, 37, 1, 38],
        "Q": [24, 8, 20, 4, 21],
        "H": [22, 12, 11, 4, 12]
    },
    14: {
        "L": [30, 3, 115, 1, 116],
        "M": [24, 4, 40, 5, 41],
        "Q": [20, 11, 16, 5, 17],
        "H": [24, 11, 12, 5, 13]
    },
    15: {
        "L": [22, 5, 87, 1, 88],
        "M": [24, 5, 41, 5, 42],
        "Q": [30, 5, 24, 7, 25],
        "H": [24, 11, 12, 7, 13]
    },
    16: {
        "L": [24, 5, 98, 1, 99],
        "M": [28, 7, 45, 3, 46],
        "Q": [24, 15, 19, 2, 20],
        "H": [30, 3, 15, 13, 16]
    },
    17: {
        "L": [28, 1, 107, 5, 108],
        "M": [28, 10, 46, 1, 47],
        "Q": [28, 1, 22, 15, 23],
        "H": [28, 2, 14, 17, 15]
    },
    18: {
        "L": [30, 5, 120, 1, 121],
        "M": [26, 9, 43, 4, 44],
        "Q": [28, 17, 22, 1, 23],
        "H": [28, 2, 14, 19, 15]
    },
    19: {
        "L": [28, 3, 113, 4, 114],
        "M": [26, 3, 44, 11, 45],
        "Q": [26, 17, 21, 4, 22],
        "H": [26, 9, 13, 16, 14]
    },
    20: {
        "L": [28, 3, 107, 5, 108],
        "M": [26, 3, 41, 13, 42],
        "Q": [30, 15, 24, 5, 25],
        "H": [28, 15, 15, 10, 16]
    },
    21: {
        "L": [28, 4, 116, 4, 117],
        "M": [26, 17, 42, 0, 0],
        "Q": [28, 17, 22, 6, 23],
        "H": [30, 19, 16, 6, 17]
    },
    22: {
        "L": [28, 2, 111, 7, 112],
        "M": [28, 17, 46, 0, 0],
        "Q": [30, 7, 24, 16, 25],
        "H": [24, 34, 13, 0, 0]
    },
    23: {
        "L": [30, 4, 121, 5, 122],
        "M": [28, 4, 47, 14, 48],
        "Q": [30, 11, 24, 14, 25],
        "H": [30, 16, 15, 14, 16]
    },
    24: {
        "L": [30, 6, 117, 4, 118],
        "M": [28, 6, 45, 14, 46],
        "Q": [30, 11, 24, 16, 25],
        "H": [30, 30, 16, 2, 17]
    },
    25: {
        "L": [26, 8, 106, 4, 107],
        "M": [28, 8, 47, 13, 48],
        "Q": [30, 7, 24, 22, 25],
        "H": [30, 22, 15, 13, 16]
    },
    26: {
        "L": [28, 10, 114, 2, 115],
        "M": [28, 19, 46, 4, 47],
        "Q": [28, 28, 22, 6, 23],
        "H": [30, 33, 16, 4, 17]
    },
    27: {
        "L": [30, 8, 122, 4, 123],
        "M": [28, 22, 45, 3, 46],
        "Q": [30, 8, 23, 26, 24],
        "H": [30, 12, 15, 28, 16]
    },
    28: {
        "L": [30, 3, 117, 10, 118],
        "M": [28, 3, 45, 23, 46],
        "Q": [30, 4, 24, 31, 25],
        "H": [30, 11, 15, 31, 16]
    },
    29: {
        "L": [30, 7, 116, 7, 117],
        "M": [28, 21, 45, 7, 46],
        "Q": [30, 1, 23, 37, 24],
        "H": [30, 19, 15, 26, 16]
    },
    30: {
        "L": [30, 5, 115, 10, 116],
        "M": [28, 19, 47, 10, 48],
        "Q": [30, 15, 24, 25, 25],
        "H": [30, 23, 15, 25, 16]
    },
    31: {
        "L": [30, 13, 115, 3, 116],
        "M": [28, 2, 46, 29, 47],
        "Q": [30, 42, 24, 1, 25],
        "H": [30, 23, 15, 28, 16]
    },
    32: {
        "L": [30, 17, 115, 0, 0],
        "M": [28, 10, 46, 23, 47],
        "Q": [30, 10, 24, 35, 25],
        "H": [30, 19, 15, 35, 16]
    },
    33: {
        "L": [30, 17, 115, 1, 116],
        "M": [28, 14, 46, 21, 47],
        "Q": [30, 29, 24, 19, 25],
        "H": [30, 11, 15, 46, 16]
    },
    34: {
        "L": [30, 13, 115, 6, 116],
        "M": [28, 14, 46, 23, 47],
        "Q": [30, 44, 24, 7, 25],
        "H": [30, 59, 16, 1, 17]
    },
    35: {
        "L": [30, 12, 121, 7, 122],
        "M": [28, 12, 47, 26, 48],
        "Q": [30, 39, 24, 14, 25],
        "H": [30, 22, 15, 41, 16]
    },
    36: {
        "L": [30, 6, 121, 14, 122],
        "M": [28, 6, 47, 34, 48],
        "Q": [30, 46, 24, 10, 25],
        "H": [30, 2, 15, 64, 16]
    },
    37: {
        "L": [30, 17, 122, 4, 123],
        "M": [28, 29, 46, 14, 47],
        "Q": [30, 49, 24, 10, 25],
        "H": [30, 24, 15, 46, 16]
    },
    38: {
        "L": [30, 4, 122, 18, 123],
        "M": [28, 13, 46, 32, 47],
        "Q": [30, 48, 24, 14, 25],
        "H": [30, 42, 15, 32, 16]
    },
    39: {
        "L": [30, 20, 117, 4, 118],
        "M": [28, 40, 47, 7, 48],
        "Q": [30, 43, 24, 22, 25],
        "H": [30, 10, 15, 67, 16]
    },
    40: {
        "L": [30, 19, 118, 6, 119],
        "M": [28, 18, 47, 31, 48],
        "Q": [30, 34, 24, 34, 25],
        "H": [30, 20, 15, 61, 16]
    }
}

# Polynomials table used for the error correction
POLYNOMIALS = {
    7: [87, 229, 146, 149, 238, 102, 21],
    10: [251, 67, 46, 61, 118, 70, 64, 94, 32, 45],
    13: [74, 152, 176, 100, 86, 100, 106, 104, 130, 218, 206, 140, 78],
    15: [8, 183, 61, 91, 202, 37, 51, 58, 58, 237, 140, 124, 5, 99, 105],
    16: [120, 104, 107, 109, 102, 161, 76, 3,
         91, 191, 147, 169, 182, 194, 225, 120],
    17: [43, 139, 206, 78, 43, 239, 123, 206,
         214, 147, 24, 99, 150, 39, 243, 163, 136],
    18: [215, 234, 158, 94, 184, 97, 118, 170,
         79, 187, 152, 148, 252, 179, 5, 98, 96, 153],
    20: [17, 60, 79, 50, 61, 163, 26, 187, 202, 180,
         221, 225, 83, 239, 156, 164, 212, 212, 188, 190],
    22: [210, 171, 247, 242, 93, 230, 14, 109, 221, 53, 200,
         74, 8, 172, 98, 80, 219, 134, 160, 105, 165, 231],
    24: [229, 121, 135, 48, 211, 117, 251, 126, 159, 180, 169, 152,
         192, 226, 228, 218, 111, 0, 117, 232, 87, 96, 227, 21],
    26: [173, 125, 158, 2, 103, 182, 118, 17, 145, 201, 111, 28, 165, 53,
         161, 21, 245, 142, 13, 102, 48, 227, 153, 145, 218, 70],
    28: [168, 223, 200, 104, 224, 234, 108, 180, 110, 190, 195, 147, 205, 27,
         232, 201, 21, 43, 245, 87, 42, 195, 212, 119, 242, 37, 9, 123],
    30: [41, 173, 145, 152, 216, 31, 179, 182, 50, 48,
         110, 86, 239, 96, 222, 125, 42, 173, 226, 193,
         224, 130, 156, 37, 251, 216, 238, 40, 192, 180]
}

# Galois table used for the error correction
GALOIS = [
    1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152,
    45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78,
    156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140, 5,
    10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161, 95, 190, 97,
    194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240, 253, 231, 211,
    187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226, 217, 175,
    67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206, 129, 31, 62,
    124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204, 133, 23, 46,
    92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84, 168, 77, 154, 41,
    82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115, 230, 209, 191, 99,
    198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171,
    75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65, 130, 25, 50,
    100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166, 81, 162, 89,
    178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72,
    144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176,
    125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1
]
GALOIS_INV = [
    None, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100,
    224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138,
    101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181,
    194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191,
    139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136, 54, 208,
    148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64, 30, 66,
    182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94,
    155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87, 7, 112,
    192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24, 227, 165,
    153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46, 55, 63,
    209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242,
    86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45,
    67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108, 161,
    59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95,
    176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215, 79, 174, 213,
    233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175
]

# Format string for the different error levels (LMQH) and mask patterns (0-7).
FORMAT_STRING = {
    "L": ["111011111000100", "111001011110011", "111110110101010",
          "111100010011101", "110011000101111", "110001100011000",
          "110110001000001", "110100101110110"],
    "M": ["101010000010010", "101000100100101", "101111001111100",
          "101101101001011", "100010111111001", "100000011001110",
          "100111110010111", "100101010100000"],
    "Q": ["011010101011111", "011000001101000", "011111100110001",
          "011101000000110", "010010010110100", "010000110000011",
          "010111011011010", "010101111101101"],
    "H": ["001011010001001", "001001110111110", "001110011100111",
          "001100111010000", "000011101100010", "000001001010101",
          "000110100001100", "000100000111011"]
}
