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

plot_model(model, to_file='output/xception_model.jpg')

imageFolder = 'input/'
filePath = imageFolder + 'bird.jpg'
image1 = image.load_img(filePath, target_size = (299, 299))

transformedImage = image.img_to_array(image1)

transformedImage = np.expand_dims(transformedImage, axis = 0)

transformedImage = preprocess_input(transformedImage)

prediction = model.predict(transformedImage)

predictionLabel = decode_predictions(prediction, top = 5)
print(predictionLabel)