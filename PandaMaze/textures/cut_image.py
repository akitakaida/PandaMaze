# 画像の切り分けを行う
from PIL import Image
import os 

path = os.path.dirname(os.path.abspath(__file__))

def cut_image(image_path, rows, cols, save_folder=path):
    # 画像を開く
    img = Image.open(image_path)
    img_width, img_height = img.size

    # 切り分けるサイズを計算
    tile_width = img_width // cols
    tile_height = img_height // rows

    # 画像を切り分けて保存
    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            right = (col + 1) * tile_width
            lower = (row + 1) * tile_height

            # 画像を切り出す
            tile = img.crop((left, upper, right, lower))

            # 切り出した画像を保存
            tile.save(os.path.join(save_folder, f'{row}{col}.png'))

cut_image(f'{path}/map_imgs.png', 2, 4)