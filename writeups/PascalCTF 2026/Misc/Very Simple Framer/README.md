# **Very Simple Framer**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

------

## Overview

- **Category**: Steganography
- **Difficulty**: Easy
- **Key Concept**: Border pixel steganography using binary encoding
- **Goal**: Extract the hidden message from an image by analyzing border pixel values

------

## Challenge Description

​	I decided to make a simple framer application, obviously with the help of my dear friend, you really think I would write that stuff?

## 1. Challenge Analysis

### Understanding the Encoder Logic

The application hides data using image steganography. Instead of modifying the main image content, the encoder creates a one-pixel border around the original image and stores binary data along that border.

The encoding process works as follows:

1. Convert the input message into a binary string.
2. Create a new image that is two pixels larger in both width and height.
3. Paste the original image into the center of the new image.
4. Traverse the outer border pixels in a fixed order.
5. Encode binary values using pixel colors:
   - Black pixel `(0,0,0)` represents binary `0`
   - White pixel `(255,255,255)` represents binary `1`

The traversal order of border pixels is critical because it determines how the message is stored and later reconstructed.

------

## 2. Decoder Development

To solve the challenge, I replicated the encoder traversal logic and extracted pixel values from the image border.

### Extracting Border Coordinates

The first step was to recreate the exact border traversal function:

```python
def generate_border_coordinates(width, height):
    coords = []

    for x in range(width):
        coords.append((x, 0))

    for y in range(1, height - 1):
        coords.append((width - 1, y))

    if height > 1:
        for x in range(width - 1, -1, -1):
            coords.append((x, height - 1))

    if width > 1:
        for y in range(height - 2, 0, -1):
            coords.append((0, y))

    return coords
```

This ensures the decoder reads pixels in the same order used during encoding.

------

### Converting Pixels to Binary

Each border pixel is inspected and translated into binary data:

```python
if pixel[0] < 128:
    binary_str += '0'
else:
    binary_str += '1'
```

To increase tolerance against color variations, the decoder checks only the red channel value.

------

### Reconstructing the Hidden Message

The collected binary string is then split into groups of 8 bits, which are converted back into ASCII characters:

```
def binary_to_string(binary_str):
    chars = []

    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]

        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))

    return ''.join(chars)
```

------

## 3. Final Solution

Running the decoder against the challenge image successfully reveals the hidden message embedded along the border pixels.

Since the encoder repeats the binary message if the border is longer than the data, the decoded output may contain repeated text.

```
pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}pascalCTF{Wh41t_wh0_4r
```

The solution works because the decoding process perfectly mirrors the encoder logic.

## Key Takeaways

- Border pixels can be used as a covert channel for hiding data.
- Maintaining identical traversal order is critical in steganography decoding.
- Small visual modifications can conceal meaningful information without altering the visible content.

## Referensces

- Basic Steganography Concepts