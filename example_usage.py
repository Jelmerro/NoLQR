from NoLQR import QRCode

# numeric encoding with 7% data recovery (L)
code = QRCode("1234567890", "L")
print(code.version)  # you can access a lot of extra info about the qr
print(code.mode)  # including the encoding mode used
print(code.err_lvl)
print(code.matrix)  # and the data matrix itself
# lastly output the qr to the terminal
code.out_terminal()

# alphanumeric encoding with 15% data recovery (M, default)
code = QRCode("1234567890+CAPITAL LETTERS AND OTHER STUFF...")
# you can also disable the inverted output for the terminal printing
code.out_terminal(False)
# you can even output the qr code as an svg
code.out_svg("alphanumeric.svg")

# binary encoding with 25% data recovery (Q)
code = QRCode(
    "A string thats actually readable, but it will "
    "take up more space as binary data", "Q")
code.out_terminal()

# binary encoding with 15% data recovery (M, default)
QRCode("༼つ◕_◕༽つ").out_terminal()

# kanji encoding with 30% data recovery (H)
code = QRCode(error_level="H", str_in="こんにちは")
code.out_terminal()
# you can customize a lot using the svg output mode
code.out_svg(
    filename="kanji",
    dark="#333333",
    light="#ccccff",
    background="orange")

# binary encoding with 15% data recovery (M, default)
code = QRCode(
    "こんにちは, if you mix kanji with other alphabets or unsupported characters, "
    "it will encode the string as binary data.")
code.out_terminal()
code.out_svg("binary.svg")
