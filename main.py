import PySimpleGUI as sg
from PySimpleGUI import LISTBOX_SELECT_MODE_MULTIPLE
import os
import functions
import const
import foldermanager as fm

folder_manager = None

layout = [
    [
        [
            [sg.Text("読み込み先フォルダ")],
            [
                sg.Input(key="input_dir"),
                sg.Button(button_text="参照", key="ask_input_dir_path"),
            ],
        ],
        [
            sg.Listbox(
                values=[],
                key="input_dir_names",
                size=(43, 10),
                select_mode=LISTBOX_SELECT_MODE_MULTIPLE,
            )
        ],
    ],
    [sg.Text("出力先フォルダ")],  # 出力先取得用パーツ
    [
        sg.Input(key="output_dir"),
        sg.Button(button_text="参照", key="ask_output_dir_path"),
    ],
    [sg.Stretch(), sg.Button("実行", key="exec", disabled=False)],
    [sg.Text("ダイアログ")],
    [sg.Output(size=(50, 5), key="dialog")]
    # 出力先取得用パーツ
    # 実行ボタン
    # ダイアログ
]

window = sg.Window(const.APP_NAME, layout)

while True:  # The Event Loop
    event, values = window.read()
    # print("event:{0} \nvalues:{1}".format(event, values))

    if event == "ask_input_dir_path":
        input_dir = functions.load_dir_path_by_filedialog()
        window["input_dir"].update(input_dir)
        folder_manager = fm.FolderManager(input_dir, is_root=True)

        # 要修正: 再描画が正しく行われない
        window["input_dir_names"].update(values=folder_manager.get_images_dir_name())

    if event == "ask_output_dir_path":
        output_dir = functions.load_dir_path_by_filedialog()
        window["output_dir"].update(output_dir)

    if event == "exec":
        input_dir_names = values["input_dir_names"]
        output_dir = values["output_dir"]

        folder_manager.update_images_dir_list(input_dir_names)

        input_dir_path_list = folder_manager.images_dir_list
        if len(input_dir_path_list) > 0 and os.path.isdir(output_dir):
            functions.save_pdfs(input_dir_path_list, output_dir)
        else:
            print("出力先と読み込み先のフォルダを選択してください.")

    if event == sg.WIN_CLOSED or event == "Exit":
        break

window.close()
