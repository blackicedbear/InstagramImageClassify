import os
import pathlib
import json
import datetime
from os.path import exists
import uuid
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.utils import plot_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.applications.xception import decode_predictions
from paddleocr import PaddleOCR
import numpy as np

model = Xception(
    include_top=True,
    weights="imagenet",
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation="softmax",
)

ocr = PaddleOCR(use_angle_cls=True, lang='en')

WRITE_TO_FILE = True

if __name__ == "__main__":
    print("Lese JSON datei ein...")
    if exists("stories_index.json"):
        print("JSON Datei vorhanden! (stories_index.json)")
        try:
            f = open("stories_index.json", "r")
            contents = f.read()
            stories_index_file = json.loads(str(contents))
            file_list_json = []
            for x in stories_index_file:
                file_list_json.append(x['filename'])
            stories_index_file_exists = True
            print("JSON Datei eingelesen.")
        except:
            stories_index_file = []
            stories_index_file_exists = False
            print("Fehler beim einlesen der Datei...")
    else:
        print("JSON Datei fehlt... Erstelle stories_index.json")
        stories_index_file = []
        stories_index_file_exists = False

    print("Lese Dateiliste ein...")
    file_list = []
    profile_list = os.listdir('stories')
    for x in profile_list:
        try:
            for y in os.listdir("stories/" + x):
                if(pathlib.Path(y).suffix == ".jpg" or pathlib.Path(y).suffix == ".webp"):
                    file_list.append(y)
        except:
            pass
    print("Dateiliste eingelesen.")

    stories_index_file_new = []
    if stories_index_file_exists == True:
        try:
            new_files = set(file_list) ^ set(file_list_json)
        except:
            pass
    else:
        new_files = file_list
    for filename in new_files:
        try:
            split = filename.split("-")
            id = uuid.uuid4().hex
            if (len(split) == 7):
                image1 = image.load_img("stories/" + split[0] + "/" + filename, target_size = (299, 299))
                transformedImage = image.img_to_array(image1)
                transformedImage = np.expand_dims(transformedImage, axis = 0)
                transformedImage = preprocess_input(transformedImage)
                prediction = model.predict(transformedImage)
                predictionLabel = decode_predictions(prediction, top = 6)
                predictionLabelNew = []
                for x in predictionLabel[0]:
                    predictionLabelNew.append(x[1])
                image_text_raw = ocr.ocr("stories/" + split[0] + "/" + filename, cls=True)
                image_text = []
                for text in image_text_raw:
                    image_text.append(text[1][0])
                time = datetime.datetime(int(split[1]), int(split[2]), int(split[3]), int(split[4].replace('h', '')), int(split[5].replace('m', '')), int(split[6].split('.')[0].replace('s', '')))
                stories_index_file.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "image_text": image_text,
                    "tags": predictionLabelNew
                })
                stories_index_file_new.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "image_text": image_text,
                    "tags": predictionLabelNew
                })
            elif (len(split) == 6):
                image1 = image.load_img("stories/" + split[0] + "/" + filename, target_size = (299, 299))
                transformedImage = image.img_to_array(image1)
                transformedImage = np.expand_dims(transformedImage, axis = 0)
                transformedImage = preprocess_input(transformedImage)
                prediction = model.predict(transformedImage)
                predictionLabel = decode_predictions(prediction, top = 6)
                predictionLabelNew = []
                for x in predictionLabel[0]:
                    predictionLabelNew.append(x[1])
                image_text_raw = ocr.ocr("stories/" + split[0] + "/" + filename, cls=True)
                image_text = []
                for text in image_text_raw:
                    image_text.append(text[1][0])
                time = datetime.datetime(int(split[1]), int(split[2]), int(split[3]), int(split[4].replace('h', '')), int(split[5].replace('m', '')))
                stories_index_file.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "image_text": image_text,
                    "tags": predictionLabelNew
                })
                stories_index_file_new.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "image_text": image_text,
                    "tags": predictionLabelNew
                })
            else:
                print(filename)
                print(split)
        except:
            pass

    if(WRITE_TO_FILE == True):
        print("Aktualisiere stories_index.json...")
        f = open("stories_index.json", "w")
        f.write(json.dumps(stories_index_file))
        f.close()
        fn = open("stories_index_new.json", "w")
        fn.write(json.dumps(stories_index_file_new))
        fn.close()
        print("stories_index.json wurde aktualisiert.")