import os
import pathlib
import json
import uuid
import datetime
from os.path import exists
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.utils import plot_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.applications.xception import decode_predictions
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

WRITE_TO_FILE = True

if __name__ == "__main__":
    print("Lese JSON datei ein...")
    if exists("posts_index.json"):
        print("JSON Datei vorhanden! (posts_index.json)")
        try:
            f = open("posts_index.json", "r")
            contents = f.read()
            posts_index_file = json.loads(str(contents))
            file_list_json = []
            for x in posts_index_file:
                file_list_json.append(x['filename'])
            posts_index_file_exists = True
            print("JSON Datei eingelesen.")
        except:
            posts_index_file = []
            posts_index_file_exists = False
            print("Fehler beim einlesen der Datei...")
    else:
        print("JSON Datei fehlt... Erstelle posts_index.json")
        posts_index_file = []
        posts_index_file_exists = False

    print("Lese Dateiliste ein...")
    file_list = []
    profile_list = os.listdir('posts')
    for x in profile_list:
        try:
            for y in os.listdir("posts/" + x):
                if(pathlib.Path(y).suffix == ".jpg" or pathlib.Path(y).suffix == ".webp"):
                    file_list.append(y)
        except:
            pass
    print("Dateiliste eingelesen.")

    posts_index_file_new = []
    if posts_index_file_exists == True:
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
            if (len(split) == 8):
                image1 = image.load_img("posts/" + split[0] + "/" + filename, target_size = (299, 299))
                transformedImage = image.img_to_array(image1)
                transformedImage = np.expand_dims(transformedImage, axis = 0)
                transformedImage = preprocess_input(transformedImage)
                prediction = model.predict(transformedImage)
                predictionLabel = decode_predictions(prediction, top = 6)
                predictionLabelNew = []
                for x in predictionLabel[0]:
                    predictionLabelNew.append(x[1])
                time = datetime.datetime(int(split[2]), int(split[3]), int(split[4]), int(split[5].replace('h', '')), int(split[6].replace('m', '')), int(split[7].split('.')[0].replace('s', '')))
                posts_index_file.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "fid": split[1],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "tags": predictionLabelNew
                })
                posts_index_file_new.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "fid": split[1],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "tags": predictionLabelNew
                })
            elif (len(split) == 7):
                image1 = image.load_img("posts/" + split[0] + "/" + filename, target_size = (299, 299))
                transformedImage = image.img_to_array(image1)
                transformedImage = np.expand_dims(transformedImage, axis = 0)
                transformedImage = preprocess_input(transformedImage)
                prediction = model.predict(transformedImage)
                predictionLabel = decode_predictions(prediction, top = 6)
                predictionLabelNew = []
                for x in predictionLabel[0]:
                    predictionLabelNew.append(x[1])
                time = datetime.datetime(int(split[1]), int(split[2]), int(split[3]), int(split[4].replace('h', '')), int(split[5].replace('m', '')), int(split[6].split('.')[0].replace('s', '')))
                posts_index_file.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "tags": predictionLabelNew
                })
                posts_index_file_new.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "tags": predictionLabelNew
                })
            elif (len(split) == 6):
                image1 = image.load_img("posts/" + split[0] + "/" + filename, target_size = (299, 299))
                transformedImage = image.img_to_array(image1)
                transformedImage = np.expand_dims(transformedImage, axis = 0)
                transformedImage = preprocess_input(transformedImage)
                prediction = model.predict(transformedImage)
                predictionLabel = decode_predictions(prediction, top = 6)
                predictionLabelNew = []
                for x in predictionLabel[0]:
                    predictionLabelNew.append(x[1])
                time = datetime.datetime(int(split[1]), int(split[2]), int(split[3]), int(split[4].replace('h', '')), int(split[5].split('.')[0].replace('m', '')))
                posts_index_file.append({
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "tags": predictionLabelNew
                })
                posts_index_file_new.append({
                    "id": id,
                    "filename": filename,
                    "profile": split[0],
                    "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
                    "fdatetime": str(time),
                    "timestamp": time.timestamp(),
                    "tags": predictionLabelNew
                })
            else:
                print(filename)
                print(split)
        except:
            pass

    if(WRITE_TO_FILE == True):
        print("Aktualisiere posts_index.json...")
        f = open("posts_index.json", "w")
        f.write(str(posts_index_file).replace('(', '{').replace(')', '}').replace("'", '"'))
        f.close()
        fn = open("posts_index_new.json", "w")
        fn.write(str(posts_index_file_new).replace('(', '{').replace(')', '}').replace("'", '"'))
        fn.close()
        print("posts_index.json wurde aktualisiert.")