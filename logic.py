from pathlib import Path
from database import user_get_folder
from langdetect import detect, DetectorFactory
import os
import face_recognition
import cv2
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


def update_file_content(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception:
        pass


def get_base_dir():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    return str(BASE_DIR)


def capture_face_encoding():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Невозможно открыть камеру")
        
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Capture Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    cap.release()
    cv2.destroyAllWindows()

    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) == 0:
        raise Exception("Лица не обнаружено")

    encodings = face_recognition.face_encodings(frame, face_locations)
    return encodings[0]

def recognize_face(known_encodings):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Невозможно открыть камеру")

    print("Looking for face...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Recognize Face', frame)

        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) > 0:
            encodings = face_recognition.face_encodings(frame, face_locations)
            for encoding in encodings:
                matches = face_recognition.compare_faces(known_encodings, encoding)
                if True in matches:
                    cap.release()
                    cv2.destroyAllWindows()
                    return True
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False