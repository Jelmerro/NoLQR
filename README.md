NoLQR
=====

QR code generation lighter than an unladen swallow.

Welcome to NoLQR, yet another QR code generator.
I made this to learn how QR codes are made.
When I had scanned the first code successfully,
the only import I had used so far was "re".
So I decided to continue without using any,
just to see if I could.
After that, someone challenged me to add Kanji support,
which is currently added and working.
So far everything I have tested seems to work as expected,
but any feedback or issues are welcome.
The name is short for "No Library QR",
as there are no libraries needed.
It can output the qr code to the terminal,
or export an svg file of it.
I found most information in the [QR Code Tutorial by Carolyn Eby](http://www.thonky.com/qr-code-tutorial/introduction),
but I also used the version table provided [here](http://www.qrcode.com/en/about/version.html).

# Features

## Easy to use

- Generates QR codes inside the terminal or as svg
- Easy to use, only the input string is required to generate a QR code
- Optionally customize the error correction level (all 4 supported: L, M, Q or H)

## Automatically makes difficult decisions

- Uses the correct encoding mode (all 4 supported), to save space when possible
- Selects the correct QR version (all 40 sizes supported)
- Picks the easiest masking type to scan (all 8 supported)

## Supports all QR data encoding modes

- Numeric encoding support
- Alphanumeric encoding support
- Binary encoding support using utf-8 (can be changed in constants.py)
- Kanji encoding support using shift-jis

# Usage

## Basic

Output to terminal
```python
from NoLQR import QRCode

code = QRCode("data you would like to represent in a qr code")
code.out_terminal()
```
Output to svg file
```python
from NoLQR import QRCode

code = QRCode("data you would like to represent in a qr code")
code.out_svg("name of the svg file")
```

## SVG

For the svg output there are lots of options,
like changing the size and color.
```python
code.out_svg(
    filename="qr",
    dark="#222222",
    light="#ffccff",
    background="yellow")
```
All arguments besides the filename are optional.

## Custom error correction level

QRCode takes two arguments:

- `str_in` (required, must be some sort of string)
- `error_level` (optional, must be "L", "M", "Q" or "H")

Like this:

```python
code = QRCode("1234567890", "L")

code.out_terminal()
code.out_svg("numeric")
```
There are 4 error correction levels:

- L, around 7% data recovery
- M, the default level with around 15% data recovery
- Q, around 25% data recovery
- H, around 30% data recovery

## More examples

The image "version 40 numeric.png" was made after scanning:
```python
QRCode("9" * 3057, "H").out_svg("version 40 numeric")
```
3057 is the character limit for error correction H and numeric encoding.
Try increasing it to see the RuntimeError it gives.

For more examples and further details, see `example_usage.py`.

# License

This project was made by [Jelmer van Arnhem](https://github.com/Jelmerro)
and can be copied under the terms of the MIT license, see the LICENSE file for details.
