
# # for i in os.listdir(glioma_path_training):
# #     print(f"Reading {i} in glioma")
# #     img = cv2.imread(os.path.join(glioma_path_training , i))
# #     if img is None:
# #         continue
# #     img = cv2.resize(img , (224,224))
# #     img = img / 255.0
# #     X.append(img)
# #     Y.append("glioma")
# # for i in os.listdir(meningioma_path_training):
# #     print(f"Reading {i} in meningioma")
# #     img = cv2.imread(os.path.join(meningioma_path_training,i))
# #     if img is None:
# #         continue
# #     img = cv2.resize(img , (224,224))
# #     img = img / 255.0

# #     X.append(img)
# #     Y.append("meningioma")
# # for i in os.listdir(notumor_path_training):
# #     print(f"Reading {i} in notumor")
# #     img = cv2.imread(os.path.join(notumor_path_training,i))
# #     if img is None:
# #         continue
# #     img = cv2.resize(img , (224,224))
# #     img = img / 255.0
# #     X.append(img)
# #     Y.append("notumor")
# # for i in os.listdir(pituitary_path_training):
# #     print(f"Reading {i} in pituitary")
# #     img = cv2.imread(os.path.join(pituitary_path_training,i))
# #     if img is None:
# #         continue
# #     img = cv2.resize(img , (224,224))
# #     img = img / 255.0
# #     X.append(img)
# #     Y.append("pituitary")

# # le = LabelEncoder()
# # Y = le.fit_transform(Y)
# # Y_to_int = to_categorical(Y)
# # X = np.array(X)
# # Y_to_int = np.array(Y_to_int) 

# # X_train,X_test,Y_train,Y_test = train_test_split(X,Y_to_int,test_size=0.2,random_state = 42)















# idg = ImageDataGenerator(
#     rescale = 1./255,
#     validation_split = 0.2
# )
# train = idg.flow_from_directory(
#     train_dir,
#     target_size=(224,224),
#     batch_size=64,
#     class_mode = 'categorical',        
#     subset='training',
#     shuffle = True,
#     seed = 42
# )
# val = idg.flow_from_directory(
#     train_dir,
#     batch_size=32,
#     subset='validation',
#     target_size=(224,224),
#     class_mode='categorical',
#     shuffle = False
# )

# test = ImageDataGenerator(rescale=1./255).flow_from_directory(
#     test_dir,
#     target_size=(224,224),
#     batch_size=32,
#     shuffle=False,
#     class_mode='categorical'
# )

# classifier = Sequential()
# classifier.add(Conv2D(32,(3,3) , activation='relu' , input_shape=(224,224,3)))
# classifier.add(MaxPooling2D(pool_size=(2,2)))
# classifier.add(Dropout(0.2))
# classifier.add(Conv2D(64,(3,3) , activation='relu' ))
# classifier.add(MaxPooling2D(pool_size=(2,2)))
# classifier.add(Dropout(0.2))
# classifier.add(Conv2D(128,(3,3) , activation='relu' ))
# classifier.add(MaxPooling2D(pool_size=(2,2)))
# classifier.add(Dropout(0.3))
# classifier.add(Conv2D(128,(3,3) , activation='relu'))
# classifier.add(MaxPooling2D(pool_size=(2,2)))
# classifier.add(Dropout(0.2))
# classifier.add(Flatten())
# classifier.add(Dense(128,activation='relu'))
# classifier.add(Dropout(0.5))
# classifier.add(Dense(4,activation='softmax'))

# classifier.compile(
#     optimizer='adam',
#     loss='categorical_crossentropy',
#     metrics=['accuracy']
# )
# early_stop = keras.callbacks.EarlyStopping(
#     monitor="val_accuracy",     
#     patience=10,                
#     restore_best_weights=True,    
#     verbose=1,                 
#     min_delta=0.001,              
#     mode="max"               
# )

# classifier.fit(
#     train,
#     epochs=22,
#     validation_data = val,
#     callbacks = [early_stop]
#     )
# classifier.save("brain_tumor_model.h5")


# test = ImageDataGenerator(rescale=1./255).flow_from_directory(
#     test_dir,
#     target_size=(224,224),
#     batch_size=32,
#     shuffle=True,
#     class_mode='categorical'
# )

# Y_label = test.labels
# print(Y_label[:10])
# print(predicted_index[:10])

# from sklearn.metrics import classification_report,confusion_matrix

# print(confusion_matrix(Y_label,predicted_index))

# print(classification_report(Y_label,predicted_index))   