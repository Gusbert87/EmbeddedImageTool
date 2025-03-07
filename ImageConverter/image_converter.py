from PyQt6.QtWidgets import QMessageBox
from PIL import Image, UnidentifiedImageError
import numpy as np

class Algorythm:
    to565 = 0
    to5bit = 1
    to8bit = 2

def get_c_array(flat_array, width, height, i="image", bit = 8):
    if(bit == 16):
        c_array_str = ",\n\t".join(", ".join(f"0x{val:04X}" for val in flat_array[i:i+16]) for i in range(0, len(flat_array), 16))#16))
    else:
        c_array_str = ",\n\t".join(", ".join(f"0x{val:02X}" for val in flat_array[i:i+16]) for i in range(0, len(flat_array), 16))#16))
    
    c_output = f"""#define {i.upper()}_WIDTH {width}\n#define {i.upper()}_HEIGHT {height}\nconst uint{bit}_t {i}[{i.upper()}_WIDTH*{i.upper()}_HEIGHT] = {{\n\t{c_array_str}\n}};\n"""

    return c_output

def convert(images, alg = Algorythm.to565):
    convert_alg = ...
    bits = ...
    if alg == Algorythm.to565:
        convert_alg = to_565_array
        bits = 16
        print("565")
    elif alg == Algorythm.to5bit:
        convert_alg = to_5bit_greyscale_array
        bits = 8
        print("5 bit")
    elif alg == Algorythm.to8bit:
        convert_alg = to_8bit_greyscale_array
        bits = 8
        print("8 bit")

    else:
        return
    c_arrays = []
    if isinstance(images, list):
        for i, image in enumerate(images):
            output_array, w, h = convert_alg(image.image)
            output_text = get_c_array(output_array, w, h, image.name.split('.')[0], 8)
            c_arrays.append(f"// Image {i+1}: {image.name}\n{output_text}\n")
    else:
        output_array, w, h = convert_alg(images.image)
        output_text = get_c_array(output_array, w, h, images.name.split('.')[0], 8)
        c_arrays.append(f"// Image {i+1}: {images.name}\n{output_text}\n")

    final_output = "#ifndef IMAGES_H\n#define IMAGES_H\n\n" + "\n\n".join(c_arrays) + "\n\n#endif"
    return final_output




def to_565_array(img):
    img = img.convert("RGB")#img.convert("RGB")  # Ensure RGB mode
    width, height = img.size
    pixels = np.array(img)

    array_565 = ( ((pixels[:, :, 0] & 0xF8).astype(np.uint16) << 8) | (pixels[:, :, 1] & 0xFC).astype(np.uint16) << 3 | (pixels[:, :, 2] >> 3).astype(np.uint16)).astype(np.uint16)
    
    flat_array = array_565.flatten()

    return flat_array, width, height

def to_5bit_greyscale_array(img):
    img = img.convert("L")#img.convert("RGB")  # Ensure RGB mode
    width, height = img.size
    pixels = np.array(img)
    
    grayscale_5bit = (pixels[:, : ] >> 3).astype(np.uint8)  # Take top 5 bits of red
    
    flat_array = grayscale_5bit.flatten()

    return flat_array, width, height


def to_8bit_greyscale_array(img):
    img = img.convert("L")#img.convert("RGB")  # Ensure RGB mode
    width, height = img.size
    pixels = np.array(img)
    
    grayscale_8bit = (pixels[:, : ]).astype(np.uint8)
    
    flat_array = grayscale_8bit.flatten()

    return flat_array, width, height