#!/usr/bin/env python3
import argparse
from PIL import Image


def binary_to_string(binary_str):
    """Convert a binary string into characters (8 bits per character)."""
    chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]

        # Ignore incomplete bytes
        if len(byte) == 8:
            try:
                chars.append(chr(int(byte, 2)))
            except ValueError:
                chars.append('?')  # Error tolerance

    return ''.join(chars)


def generate_border_coordinates(width, height):
    """Generate border pixel coordinates (same order as encoder)."""
    coords = []

    # Top row
    for x in range(width):
        coords.append((x, 0))

    # Right column
    for y in range(1, height - 1):
        coords.append((width - 1, y))

    # Bottom row
    if height > 1:
        for x in range(width - 1, -1, -1):
            coords.append((x, height - 1))

    # Left column
    if width > 1:
        for y in range(height - 2, 0, -1):
            coords.append((0, y))

    return coords


def extract_message(input_image_path):
    """Extract hidden message from the image border."""

    try:
        img = Image.open(input_image_path).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    width, height = img.size
    border_coords = generate_border_coordinates(width, height)

    binary_str = ""

    for x, y in border_coords:
        pixel = img.getpixel((x, y))

        # Black pixel → 0
        # White pixel → 1
        if pixel[0] < 128:
            binary_str += '0'
        else:
            binary_str += '1'

    decoded_msg = binary_to_string(binary_str)

    print("-" * 40)
    print("Raw decoded output (message may repeat):")
    print("-" * 40)
    print(decoded_msg)
    print("-" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Decode hidden message from image border."
    )

    parser.add_argument(
        "input_image",
        help="Path to the encoded image file."
    )

    args = parser.parse_args()

    extract_message(args.input_image)


if __name__ == "__main__":
    main()
