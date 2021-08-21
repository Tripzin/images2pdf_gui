# -*- coding: utf-8 -*-
import os
import glob


class FolderManager:
    dir_path = ""
    images_dir_list = []
    is_root = False

    def __init__(self, dir_path, is_root=False):
        self.dir_path = dir_path
        self.is_root = is_root
        self.init_images_dir_list()

    def get_dir_path(self):
        return self.dir_path

    def get_dir_name(self):
        """
        ディレクトリパスから最も階層の深いディレクトリの名前を返す
        """
        return os.path.basename(self.dir_path)

    def is_exist_child_dir(self):
        """
        ディレクトリパス下にディレクトリが存在するか判断する
        """
        childrens = glob.glob(self.dir_path + "/*")
        for each_child in childrens:
            if os.path.isdir(each_child):
                return True
        else:
            return False

    def init_images_dir_list(self):
        """
        画像が含まれるディレクトリパスのリストをメンバ変数にセットする
        """
        if self.is_exist_child_dir():
            childrens = glob.glob(self.dir_path + "/*")
            for each_child in childrens:
                temp_fm = FolderManager(each_child)
                self.images_dir_list.append(temp_fm)
        else:
            if self.is_root == True:
                self.images_dir_list.append(self)

    def update_images_dir_list(self, selected_images_dir_names):
        temp_filtering_images_dir_list = list(
            filter(
                lambda elm: elm.get_dir_name() in selected_images_dir_names,
                self.images_dir_list,
            )
        )
        self.images_dir_list = temp_filtering_images_dir_list

    def get_images_dir_name(self):
        temp = []
        for each_elm in self.images_dir_list:
            temp.append(each_elm.get_dir_name())
        return temp

    def get_image_path_list(self):
        if self.is_exist_child_dir():
            raise FileNotFoundError("ディレクトリ下に画像が存在しません")
        else:
            return glob.glob(self.dir_path + "/*")


if __name__ == "__main__":
    test_path = "./source"
    manager = FolderManager(test_path, is_root=True)
