from PIL import Image

im = Image.open("c:/MySpace/other/Miscellaneous/test.png")
im.show()

print(im.format, im.size, im.mode)

