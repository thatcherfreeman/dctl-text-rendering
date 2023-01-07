# DCTL Text Rendering

This repository shows how to render text in a DCTL for DaVinci Resolve.

## Installation

1. Clone/download the repository to your computer somewhere.
2. (Optional) Create a virtual environment with something like `python -m venv dctl-text-rendering`, then activate with `source dctl-text-rendering/bin/activate`
3. Run `pip install -r requirements.txt`
4. Go to http://www.pentacom.jp/pentacom/bitfontmaker2/gallery/ and click "Copy & edit" on one of the fonts you like
5. Click the "Data Import/Export" button in the top right of the font editor, copy the whole text box into a file somewhere like the `font.txt` file in this repo.
6. Navigate back here, run `python font_gen.py font.txt` (replacing `font.txt` with the name of your exported font if it's different)
7. The python script will generate a `.h` file. Go to `Text Rendering.dctl` and replace the `#include` statement with the name of the new `.h` file (it matches the name of your downloaded font!).
8. Move the `Text Rendering.dctl` and the `.h` file to your Resolve LUT folder, restart resolve, and see it in action in the DCTL effect!
