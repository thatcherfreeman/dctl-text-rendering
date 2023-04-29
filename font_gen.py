import json
from argparse import ArgumentParser
import numpy as np

def convert_pentacom_to_bitmap(arr, width):
    out = []
    for row in arr:
        out_row = []
        for i in range(width):
            flag = 1 << i
            if row & flag > 0:
                out_row.append(1)
            else:
                out_row.append(0)
        out.append(out_row)
    return out

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Converts fonts to bitmaps."
    )
    parser.add_argument(
        "font_file",
        help="File containing your font, exported from https://www.pentacom.jp/pentacom/bitfontmaker2/",
    )
    args = parser.parse_args()

    # Read the specified file.
    with open(args.font_file, 'r') as f:
        font_dict = json.load(f)

    # Get dimensions
    letter_area = int(font_dict['letterspace'])
    letter_height = len(font_dict['65']) # Assume 'A' is in the dict
    max_val = np.max([v for _, v in font_dict.items() if type(v) == list])
    letter_width = int(np.floor(np.log2(max_val)))
    print(max_val)
    print(f"Detected letter area {letter_area}, with width {letter_width} and height {letter_height}")

    # Trim out keys that don't look like an int.
    char_dict = {}
    for c, arr in font_dict.items():
        try:
            d = int(c)
            if d < 128:
                char_dict[d] = arr
        except ValueError:
            # Ignore keys that don't look like numbers
            continue

    # Fill low ascii values with zeros for safety.
    font_array = np.zeros((max(char_dict.keys())+1, letter_height), dtype=int)
    for c, arr in char_dict.items():
        font_array[c] = arr

    # Precompute width of each character.
    font_width_array = np.floor(np.log2(np.max(font_array, axis=1))).astype(int) if np.max(arr) > 0 else letter_width
    font_width_array[np.max(font_array, axis=1) == 0] = letter_width

    # Convert our font arrays to strings.
    np.set_printoptions(threshold=np.inf)
    out = np.array2string(font_array, separator=',', formatter={'int': lambda x: f"{x:d}"})
    font_width_str = np.array2string(font_width_array, separator=',', formatter={'int': lambda x: f"{x:d}"})

    # Generate C code.
    f = open(f'{font_dict["name"]}.h', 'w')
    f.write(
f"""
#define FONT_WIDTH {letter_width}
#define FONT_HEIGHT {letter_height}
#define FONT_LENGTH {font_array.shape[0]}

__CONSTANT__ int font_widths[FONT_LENGTH] = {font_width_str.replace('[', '{').replace(']', '}')};
__CONSTANT__ int font[FONT_LENGTH][FONT_HEIGHT] = {out.replace('[', '{').replace(']', '}')};
"""
    )
    f.close()
