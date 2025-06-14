# Script d'entraînement du modèle IA - ne pas exécuter dans l'app
"""aisoft-training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TscXHBeQIdDOvHkhfFGfY82O8ySJTwOi
"""

from google.colab import drive
drive.mount('/content/drive')




import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam

# Paramètres
dataset_path = '/content/drive/MyDrive/aisoft/dataset/weapons'
IMG_SIZE = 224
BATCH_SIZE = 16  # Augmentation raisonnable du batch size
EPOCHS = 20      # Plus d'epochs pour un meilleur entraînement
NUM_CLASSES = len(os.listdir(dataset_path))

print(f"Nombre de classes détectées : {NUM_CLASSES}")

# Générateurs avec prétraitement adapté et augmentations plus riches
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    horizontal_flip=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    shear_range=0.2,
    brightness_range=[0.8,1.2]
)

val_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)

# Chargement du modèle ResNet50 sans la tête, avec poids ImageNet
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))

# On débloque les dernières couches pour fine-tuning
base_model.trainable = True
for layer in base_model.layers[:140]:
    layer.trainable = False

# Ajout de la tête personnalisée
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compilation avec un learning rate plus faible pour fine-tuning
model.compile(
    optimizer=Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Entraînement
# history = model.fit(
#     train_generator,
#     epochs=EPOCHS,
#     validation_data=val_generator
# )

# Sauvegarde
# model.save('/content/drive/MyDrive/aisoft/dataset/aisoft_resnet_finetuned.h5')
# print("Modèle sauvegardé dans aisoft/")