from PIL import Image
import tempfile


im = Image.open('test15.jpg')

length_x, width_y = im.size

factor = min(1, float(1024.0 / length_x))

size = int(factor * length_x), int(factor * width_y)

im_resized = im.resize(size)

temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')

temp_filename = temp_file.name

im_resized.save(temp_filename, dpi=(300, 300))

