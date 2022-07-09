from PIL import Image
import os

directory = '../pieces_img'

empty_img = Image.new(mode="RGBA", size=(45, 45), color="#ffffff00")

empty_img.save(os.path.join(directory, 'empty.png'))
