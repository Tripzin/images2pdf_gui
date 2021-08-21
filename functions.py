from PIL import Image, ImageFile, UnidentifiedImageError
import os
import glob
import re
import tkinter.filedialog
import const


def load_dir_path_by_filedialog():
    ret = tkinter.filedialog.askdirectory(initialdir=const.ROOT_DIR, mustexist=True)
    return ret


def save_pdfs(input_dir_path_list, output_dir):
    for each_dir in input_dir_path_list:
        dir_name = each_dir.get_dir_name()
        print("-" * 3 + dir_name)
        image_path_list = sorted(
            each_dir.get_image_path_list(),
            key=lambda image_path: key_of_sort(image_path),
        )
        save_pdf(output_dir, dir_name, image_path_list)
        print("-" * 3 + "output: " + dir_name + ".pdf")

    print("convert complete!!")


def get_image_path_list(dir_path):
    return glob.glob(dir_path + "/*")


def key_of_sort(file_path):
    num = re.search(r"\/(\d{1,})\.(jpg|png|bmp)$", file_path)
    if num == None:
        num = -1
    else:
        num = int(num.group(1))
    return num


def save_pdf(output_dir, file_name, image_list):
    output_path = os.path.join(output_dir, file_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_obj = []
    image_list_size = len(image_list)
    for num, img in enumerate(image_list):
        try:
            img_obj = Image.open(img).convert("RGB")
            image_obj.append(img_obj)
        except UnidentifiedImageError:
            print("{0}: can not convert to pdf.".format(img))

    image_obj[0].save(output_path + ".pdf", save_all=True, append_images=image_obj[1:])


if __name__ == "__main__":
    print("hello!")
