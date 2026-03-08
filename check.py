from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
classifier = load_model("brain_tumor_detection_improved.h5")

test_dir = "./Testing"


menin = "./app_uploads/sample2.jpeg"
img = cv2.imread(menin)
img = cv2.resize(img , (224,224))
img = img / 255.0
img = np.expand_dims(img, axis=0)


Y_predicted = classifier.predict(img)
predicted_index = np.argmax(Y_predicted,axis=1)
print(predicted_index)
