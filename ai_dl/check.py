test_dir = "./Testing"
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
class Check_Tumor:
    def check(self,file_path :str):
        classifier = load_model("brain_tumor_detection_improved.h5")
        image = f"./../backend/{file_path}"
        img = cv2.imread(image)
        img = cv2.resize(img , (224,224))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        Y_predicted = classifier.predict(img)
        predicted_index = np.argmax(Y_predicted,axis=1)
        print(predicted_index)
        if predicted_index == 0 :
            return "Glioma"
        elif predicted_index == 1:
            return "Meningioma"
        elif predicted_index == 2:
            return "No Tumor"
        else:
            return "Pituitary"