# Main file of NoLQR, QR code generation lighter than an unladen swallow
# Made by Jelmerro, see README.md for more details
# MIT, see LICENSE for details
# https://github.com/Jelmerro/NoLQR for updates

from . import constants, util


class QRCode():

    def __init__(self, str_in, error_level="M"):
        """ Init for QRCode

        Calls all methods (steps) required to generate a QR code.
        After all steps, the QR code will be stored as a data matrix.
        To generate an output from the matrix,
        call any method prefixed with "out_".
        """
        if error_level.upper() not in list("LMQH"):
            raise ValueError("Invalid error level, use L, M (default), Q or H")
        self.err_lvl = error_level.upper()
        self.generate_data(str_in)
        self.static_matrix = []
        for i in range(0, self.width):
            self.static_matrix.append([])
            for _ in range(0, self.width):
                self.static_matrix[i].append(None)
        self.add_finder_patterns()
        self.add_alignment_patterns()
        self.add_timer_patterns()
        self.static_matrix[self.width-8][8] = 1
        self.add_version_information()
        self.generate_data_matrix()
        self.merge_matrixes()
        self.apply_mask_and_finish_format()

    def encode_input(self, str_in):
        """ Encodes the input string using different modes

        Depending on the result of util.best_mode,
        The input string is encoded with either:
        numeric, alphanumeric, binary or kanji.
        Each of these modes has a different way to encode the data,
        and all of them are implemented below.
        The mode indicator and the character count indicator,
        are added before data, to form the data string.
        """
        out = ""
        data_length = 0
        if self.mode == "numeric":
            for group in [str_in[i:i+3] for i in range(0, len(str_in), 3)]:
                if len(group) == 3:
                    out += "{:010b}".format(int(group))
                if len(group) == 2:
                    out += "{:07b}".format(int(group))
                if len(group) == 1:
                    out += "{:04b}".format(int(group))
                data_length += len(group)
        if self.mode == "alphanumeric":
            alpha_codes = []
            for group in [str_in[i:i+2] for i in range(0, len(str_in), 2)]:
                for character in group:
                    alpha_codes.append(constants.ALPHA_TABLE[character])
            for i in range(0, len(alpha_codes), 2):
                if i + 1 < len(alpha_codes):
                    number = alpha_codes[i] * 45 + alpha_codes[i + 1]
                    out += "{:011b}".format(number)
                    data_length += 2
                else:
                    out += "{:06b}".format(alpha_codes[i])
                    data_length += 1
        if self.mode == "binary":
            for character in str_in.encode(constants.ENCODING):
                out += "{:08b}".format(character)
                data_length += 1
        if self.mode == "kanji":
            characters = []
            for item in str_in:
                characters.append(item.encode("shift-jis"))
            bytes = ""
            for character in characters:
                if len(character.hex()) == 4:
                    bytes += character.hex()
                else:
                    # when mixing other alphabets with kanji:
                    # binary encoding should be used instead of kanji
                    # otherwise data will be lost
                    self.mode = "binary"
                    return self.encode_input(str_in)
            for group in [bytes[i:i+4] for i in range(0, len(bytes), 4)]:
                hex_code = int(group, 16)
                subtractor = ""
                if hex_code > int("8140", 16) and hex_code < int("9ffc", 16):
                    subtractor = "8140"
                elif hex_code > int("e040", 16) and hex_code < int("ebbf", 16):
                    subtractor = "c140"
                else:
                    # when containing unsupported:
                    # binary encoding should be used instead of kanji
                    # otherwise data will be lost
                    self.mode = "binary"
                    return self.encode_input(str_in)
                hex_code = "{:04x}".format(hex_code - int(subtractor, 16))
                sig_bit = int(hex_code[:2], 16)
                ins_bit = int(hex_code[2:], 16)
                hex_code = (sig_bit * int("c0", 16)) + ins_bit
                out += "{:013b}".format(hex_code)
                data_length += 1
        self.version = util.version(self.mode, data_length, self.err_lvl)
        return "{}{}{}".format(
            constants.MODES[self.mode]["mode_indicator"],
            util.character_count_indicator(
                self.mode,
                data_length,
                self.version),
            out)

    def generate_data(self, str_in):
        """ Generates the data from the input string

        First picks the best mode and calls encode_input.
        After that, zeros are padded as explained in util.pad_zeros.
        Next the data is split in codewords (each containing 8 bits).
        These are used to generate the data blocks and error blocks.
        The result will be interleaved,
        and some remainer bits are added.
        The amount is always between 0 and 8,
        so 8 are added (overflow bits won't be added anyway).
        """
        self.mode = util.best_mode(str_in)
        data = self.encode_input(str_in)
        self.width = util.width(self.version)
        max_bytes = constants.VERSIONS[self.version][self.err_lvl]
        data = util.pad_zeros(data, max_bytes)
        codewords = [data[i:i+8] for i in range(0, len(data), 8)]
        info = constants.ERROR_CORRECTION_BLOCKS[self.version][self.err_lvl]
        data_blocks, error_blocks = util.generate_blocks(codewords, info)
        result = util.interleave_codewords(data_blocks, error_blocks)
        self.data = result + "0"*8

    def add_finder_patterns(self):
        """ Adds the finder patterns to the matrix

        In the top-left, top-right and bottom-left corner,
        a finder pattern is needed.
        This consists of a black 3x3 square,
        with a white border around that,
        with another black border around that.
        This 7x7 pattern has a white line between the data.
        The ranges in the loops below are even bigger,
        because they also reserve space for the format string.
        """
        for y in range(0, 9):
            for x in range(0, 9):
                self.static_matrix[y][x] = 0
        for y in range(self.width-8, self.width):
            for x in range(0, 9):
                self.static_matrix[y][x] = 0
        for y in range(0, 9):
            for x in range(self.width-8, self.width):
                self.static_matrix[y][x] = 0
        for base_x, base_y in [[0, 0], [self.width-7, 0], [0, self.width-7]]:
            for x in range(base_x, base_x+7):
                self.static_matrix[base_y][x] = 1
                self.static_matrix[base_y+6][x] = 1
            for y in range(base_y, base_y+7):
                self.static_matrix[y][base_x] = 1
                self.static_matrix[y][base_x+6] = 1
            for y in range(base_y+2, base_y+5):
                for x in range(base_x+2, base_x+5):
                    self.static_matrix[y][x] = 1

    def add_alignment_patterns(self):
        """ Adds the alignment patterns to the matrix

        The alignment patterns are added in different locations,
        depending on the version of the qr code.'
        It consists of a black pixel,
        with a white border around that,
        with another black border around that.
        The result is a 5x5 square pattern.
        In constants, a list of numbers is stored.
        This is a list of x/y positions,
        as each number can be either x or y,
        and all combination will receive an alignment pattern.
        The patterns are not added however,
        in any place which would overlap a reserved area.
        """
        patterns = constants.VERSIONS[self.version]["alignment"]
        for base_x in patterns:
            for base_y in patterns:
                if not self.static_matrix[base_y][base_x]:
                    for y in range(base_y-2, base_y+3):
                        for x in range(base_x-2, base_x+3):
                            self.static_matrix[y][x] = 0
                    for y in range(base_y-2, base_y+3):
                        self.static_matrix[y][base_x-2] = 1
                    for x in range(base_x-2, base_x+3):
                        self.static_matrix[base_y-2][x] = 1
                    for y in range(base_y-2, base_y+3):
                        self.static_matrix[y][base_x+2] = 1
                    for x in range(base_x-2, base_x+3):
                        self.static_matrix[base_y+2][x] = 1
                    self.static_matrix[base_y][base_x] = 1

    def add_timer_patterns(self):
        """ Adds the timer pattern to the matrix

        The timer pattern is a dotted line,
        which is added between the finder patterns.
        No conflict calculation with the alignment patterns is done,
        because this dotted line is part of the pattern.
        """
        for x in range(6, self.width-8, 2):
            self.static_matrix[6][x] = 1
            self.static_matrix[6][x+1] = 0
        for y in range(6, self.width-8, 2):
            self.static_matrix[y][6] = 1
            self.static_matrix[y+1][6] = 0

    def add_version_information(self):
        """ Adds the version information to the matrix

        This is only needed for version 7 and up,
        and consists of a 3x6 area near the finder patterns.
        The bits are added from most significant to least,
        so the index starts at 17 and goes down from there.
        """
        if self.version > 6:
            pattern = constants.VERSIONS[self.version]["pattern"]
            index = 17
            for y in range(0, 6):
                for x in range(self.width-11, self.width-8):
                    self.static_matrix[y][x] = int(pattern[index])
                    index -= 1
            index = 17
            for x in range(0, 6):
                for y in range(self.width-11, self.width-8):
                    self.static_matrix[y][x] = int(pattern[index])
                    index -= 1

    def generate_data_matrix(self):
        """ Generates the data matrix

        The data is added in a zig-zag pattern,
        starting in the bottom right corner.
        Each zig-zag is two bits/pixels wide.
        Once the top is reached, move two to the left,
        and add the data in a zig-zag going down.
        If a reserved bit is found,
        skip it, and add the data bit in the next suitable location.
        This is done for all the data and the entire matrix,
        with one exception for the vertical timing pattern.
        This column is skipped altogether,
        and the zig-zag pattern will continue one bit to the left.
        """
        self.data_matrix = []
        for i in range(0, self.width):
            self.data_matrix.append([])
            for _ in range(0, self.width):
                self.data_matrix[i].append(None)
        for base_x in range(self.width-1, 0, -2):
            for base_y in range(self.width-1, -1, -1):
                if base_x < 8:
                    x = base_x - 1
                else:
                    x = base_x
                if base_x % 4 == 2:
                    y = self.width - base_y - 1
                else:
                    y = base_y
                if self.data and self.static_matrix[y][x] is None:
                    self.data_matrix[y][x] = int(self.data[:1])
                    self.data = self.data[1:]
                if x > 0 and self.data and self.static_matrix[y][x-1] is None:
                    self.data_matrix[y][x-1] = int(self.data[:1])
                    self.data = self.data[1:]

    def merge_matrixes(self):
        """ Merge the data and the static matrix

        When this method is called,
        all patterns are in the static matrix,
        and all data is in the data matrix.
        This method simply merges the two matrixes,
        into a single matrix.
        """
        self.matrix = []
        for i in range(0, self.width):
            self.matrix.append([])
            for j in range(0, self.width):
                self.matrix[i].append(self.static_matrix[i][j])
        for x in range(0, self.width):
            for y in range(0, self.width):
                if self.matrix[y][x] is None:
                    self.matrix[y][x] = self.data_matrix[y][x]

    def apply_mask_and_finish_format(self):
        """ Apply mask and finish overall formatting

        Each masking pattern is applied separately,
        and the best one is picked.
        This is done by calculating a score,
        for each of the different mask patterns.
        There are four penalty rules for that:
        - Single line with same colored bits (column or row)
            This gives a penalty for each group of 5 or more.
            The penalty is 3 for a group of 5,
            and 1 more for every next same colored bit.
            This is tested for horizontal and vertical lines.
        - 2x2 area of same colored bits
            This gives a penalty for ALL 2x2 groups,
            even if they are part of another group.
            Every 2x2 square has a penalty of 3.
        - Similar bits to a finder pattern (column or row)
            This gives a penalty for all 10111010000 or 00001011101.
            Each time these bits are found, add 40 to the penalty.
            This is tested for horizontal and vertical lines.
        - A large amount of dark or light bits
            If the percentage of dark modules is not near 50,
            add a penalty of 10 for every 5 percent (rounded down).
            This means, 4.9 percent results in 0, but 5.0 in 10.

        After calculating the score for all different mask patterns,
        the mask pattern with the lowest score is used.
        The format string was already added in the process,
        because the penalty rules also apply to the format bits.
        """
        matrixes = []
        scores = []
        for m in range(0, 8):
            matrixes.append([])
            scores.append(0)
            for i in range(0, self.width):
                matrixes[m].append([])
                for j in range(0, self.width):
                    matrixes[m][i].append(self.matrix[i][j])
        masks = [
            lambda x, y: (x + y) % 2 == 0,
            lambda x, y: y % 2 == 0,
            lambda x, y: x % 3 == 0,
            lambda x, y: (x + y) % 3 == 0,
            lambda x, y: (int(y / 2) + int(x / 3)) % 2 == 0,
            lambda x, y: (x * y) % 2 + (x * y) % 3 == 0,
            lambda x, y: ((x * y) % 3 + x * y) % 2 == 0,
            lambda x, y: ((x * y) % 3 + x + y) % 2 == 0
        ]
        for m in range(0, 8):
            for x in range(0, self.width):
                for y in range(0, self.width):
                    if self.data_matrix[y][x] is not None and masks[m](x, y):
                        matrixes[m][y][x] = (self.data_matrix[y][x]+1) % 2
            matrixes[m] = util.add_format_info(
                matrixes[m],
                self.width,
                constants.FORMAT_STRING[self.err_lvl][m])
            for direction in [0, 1]:
                total_black = 0
                counter_white = 0
                counter_black = 0
                ss1 = ""
                ss2 = ""
                for x_or_y1 in range(0, self.width):
                    for x_or_y2 in range(0, self.width):
                        if direction:
                            current_position = matrixes[m][x_or_y1][x_or_y2]
                        else:
                            current_position = matrixes[m][x_or_y2][x_or_y1]
                        if current_position == 1:
                            counter_white = 0
                            counter_black += 1
                            total_black += 1
                        else:
                            counter_white += 1
                            counter_black = 0
                        if counter_white == 5 or counter_black == 5:
                            scores[m] += 3
                        elif counter_white > 5 or counter_black > 5:
                            scores[m] += 1
                        if current_position == int("10111010000"[len(ss1)]):
                            ss1 += str(current_position)
                            if len(ss1) == 11:
                                scores[m] += 40
                                ss1 = ""
                        else:
                            ss1 = ""
                        if current_position == int("00001011101"[len(ss2)]):
                            ss2 += str(current_position)
                            if len(ss2) == 11:
                                scores[m] += 40
                                ss2 = ""
                        else:
                            ss2 = ""
            for x in range(0, self.width-1):
                for y in range(0, self.width-1):
                    if matrixes[m][y+1][x] == 1 and matrixes[m][y+1][x+1] == 1:
                        if matrixes[m][y][x] == 1 and matrixes[m][y][x+1] == 1:
                            scores[m] += 3
                    if matrixes[m][y+1][x] == 0 and matrixes[m][y+1][x+1] == 0:
                        if matrixes[m][y][x] == 0 and matrixes[m][y][x+1] == 0:
                            scores[m] += 3
            percentage = (total_black / (self.width * self.width)) * 100
            if percentage > 50:
                scores[m] += int((percentage - 50) / 5) * 10
            elif percentage < 50:
                scores[m] += int((50 - percentage) / 5) * 10
        self.matrix = matrixes[scores.index(min(scores))]

    def out_terminal(self, inverted=True):
        """ Output to terminal

        Output the QR Code to the terminal.
        Simply loops over the matrix two lines at the time,
        and prints the suitable character (█, ▄, ▀ or a space).
        """
        if inverted:
            EMPTY = "█"
            TOP = "▄"
            BOTTOM = "▀"
            FULL = " "
        else:
            EMPTY = " "
            TOP = "▀"
            BOTTOM = "▄"
            FULL = "█"
        print(EMPTY*(self.width+4))
        for row in range(0, self.width, 2):
            out = EMPTY*2
            for p in range(0, self.width):
                if row+1 == self.width:
                    if self.matrix[row][p]:
                        out += TOP
                    else:
                        out += EMPTY
                elif self.matrix[row][p] and self.matrix[row+1][p]:
                    out += FULL
                elif self.matrix[row][p]:
                    out += TOP
                elif self.matrix[row+1][p]:
                    out += BOTTOM
                else:
                    out += EMPTY
            out += EMPTY*2
            print(out)
        print(EMPTY*(len(self.matrix)+4))

    def out_svg(self,
                filename,
                dark="black",
                light="white",
                background="white"):
        """ Output as an svg

        Output the QR Code to an svg file.
        Loops over the matrix, and makes a rect for each square.
        Also makes a colored background.
        Custom colors and sizes can be provided as arguments.
        """
        filename = filename.rstrip()
        if not filename.endswith(".svg"):
            filename = "{}.svg".format(filename)
        rect = '    <rect x="{}" y="{}" height="{}" width="{}" fill="{}" />\n'
        out = '<?xml version="1.0" encoding="UTF-8" ?>\n'
        out += '<!-- Generated with NoLQR, QR code generation lighter ' \
            'than an unladen swallow -->\n'
        out += '<!-- Visit https://github.com/Jelmerro/NoLQR ' \
            'for updates and details -->\n'
        out += '<svg height="{}" width="{}" xmlns="http://www.w3.org/' \
            '2000/svg" version="1.1">\n'.format(self.width+4, self.width+4)
        out += rect.format(0, 0, self.width+4, self.width+4, background)
        for row in range(0, self.width):
            for col in range(0, self.width):
                out += rect.format(
                    2 + row, 2 + col, 1, 1,
                    dark if self.matrix[col][row] else light)
        with open(filename, "w") as f:
            f.write(out + "</svg>")
