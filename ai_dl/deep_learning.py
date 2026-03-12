import glob 
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.xception import preprocess_input,Xception
from tensorflow.keras.optimizers import Adam
from sklearn.utils.class_weight import compute_class_weigh
train_dir = "./Training"
test_dir = "./Testing"
from sklearn.utils import class_weight
import numpy as np

idg = ImageDataGenerator(
    preprocessing_function = preprocess_input,
    rotation_range = 25,
    validation_split = 0.2,
    zoom_range = 0.2,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    horizontal_flip = True
)

train = idg.flow_from_directory(
    train_dir,
    target_size = (224,224),
    batch_size=32,
    validation_split=0.2,
    class_mode = 'categorical',
    shuffle = True,
    subset = 'training'
)

val = idg.flow_from_directory(
    train_dir,
    target_size = (224,224),
    batch_size=32,
    class_mode='categorical',
    subset = 'validation',
)

class_weight = compute_class_weight(
    class_weight = 'balanced',
    classes = np.unique(train.classes),
    y = train.classes
)

IMAGE_SIZE = [224,224]

xception = Xception(
    include_top = False,
    input_shape = IMAGE_SIZE + [3],
    weights = 'imagenet',
)

for l in xception.layers:
    l.trainable = False

for l in xception.layers[-60:]:
    l.trainable = True

x = xception.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)

last_layer = Dense(4 , activation='softmax')(x)
model = Model(
    inputs = xception.input, 
    outputs = last_layer
)
model.compile(
    optimizer = Adam(learning_rate = 0.0001),
    loss = 'categorical_crossentropy',
    metrics = ['accuracy']
)

early_stop = EarlyStopping(
    patience = 5,
    restore_best_weights = True,
    monitor = 'val_loss'
)

reduce_lr = ReduceLROnPlateau(
    monitor = 'val_loss',
    patience = 3,
    factor = 0.3,
    min_lr = 1e-6
)
model.fit(
    train,
    validation_data = val,
    class_weight = class_weight,
    callbacks = [early_stop,reduce_lr],
    epochs = 40
)
model.save("brain_tumor_detection_improved.h5")