from PIL import Image, ImageFile, UnidentifiedImageError
import os
import glob
import re
from tqdm import tqdm
import tkinter.filedialog
import const


def load_dir_path_by_filedialog():
    ret = tkinter.filedialog.askdirectory(initialdir=const.ROOT_DIR, mustexist=True)
    return ret


def is_exist_images_under_this_dir_path(dir_path):
    """
    与えられたdir_path下は画像か、フォルダか判断する
    """
    # TODO: 判断ロジックは適切？
    if len(get_child_dir_names(dir_path)) > 0:
        return False
    else:
        return True


def get_dir_name(dir_path):
    return os.path.basename(dir_path)


def get_child_dir_names(dir_path):
    """
    与えられたdir_path下のディレクトリの名前のリストを返す
    """
    return [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]


def get_child_file_names(dir_path):
    """
    与えられたdir_path下のファイルの名前のリストを返す
    """
    return [
        f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
    ]


def save_pdfs(input_dir, inputs_dir_name, output_dir):
    # TODO: input_dir とinputs_dir_nameの関係がごちゃごちゃしているので治す
    dir_path_list = glob.glob(input_dir + "/" + "*")
    for dir_path in dir_path_list:
        dir_name = get_dir_name(dir_path)
        if dir_name in inputs_dir_name:
            print("-" * 3 + dir_name)
            image_path_list = sorted(
                get_image_path_list(dir_path),
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
