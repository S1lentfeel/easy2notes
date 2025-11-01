from pathlib import Path
from database import user_get_folder
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

def detect_lang(text):
    try:
        code = detect(text)
        if code.startswith("ru"):
            return "ru"
        if code.startswith("en"):
            return "en"
        return code
    except Exception:
        return "unknown"


def get_folders_for_user(login):
    folder_path = Path(user_get_folder(login))
    array = []

    for i in folder_path.iterdir():
        stroka = str(i).split("\\")[-1]
        array.append(f"{stroka}")

    return array


def get_file_content(path_to_file):
    with open(path_to_file, mode="r+", encoding="utf8") as file:
        strokovoi_array = ""
        for i in file.read():
            strokovoi_array += i

    return strokovoi_array


def create_file(path):
    try:
        with open("file.txt", "x+", encoding="utf-8"):
            pass
    except FileExistsError:
        pass

    