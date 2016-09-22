import csv
import cv2
import os
import numpy as np
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import Model
from keras.layers import BatchNormalization
from keras.layers import Input, Dense, Dropout, Flatten, Convolution2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator


def net(input_shape):
    input_img = Input(input_shape)
    # convolutional layers: (N_kernels, h_kernel, W_kernel)
    conv = BatchNormalization()(input_img)
    conv = Convolution2D(8, 5, 5, activation='relu', border_mode='same')(conv)
    conv = MaxPooling2D((2, 2), strides=(2, 2))(conv)
    # conv = Dropout(0.25)(conv)
    conv = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(conv)
    conv = MaxPooling2D((2, 2), strides=(2, 2))(conv)
    conv = Dropout(0.1)(conv)
    conv = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(conv)
    conv = MaxPooling2D((2, 2), strides=(2, 2))(conv)
    conv = Dropout(0.15)(conv)
    conv = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(conv)
    conv = MaxPooling2D((2, 2), strides=(2, 2))(conv)
    conv = Dropout(0.2)(conv)
    conv = Convolution2D(32, 3, 3, activation='relu', border_mode='valid')(conv)
    # conv = MaxPooling2D((2, 2), strides=(2, 2))(conv)
    conv = Dropout(0.25)(conv)
    fc = Flatten()(conv)

    # fully connected layers: (N_newrons)
    # fc = Dense(16, activation='relu')(fc)
    # # fc = Dropout(0.25)(fc)
    fc = Dense(1, activation='sigmoid')(fc)
    model = Model(input=input_img, output=fc)

    return model


def train():
    ###
    # getting dataset from raw csv:
    dataset_path = '/home/nate/Downloads/Challenge_FST_Train_classifier.csv'
    reader = csv.reader(open(dataset_path, 'rb'),delimiter=',')
    dataset = np.array(list(reader)[1:])#.astype('float')
    p = []
    y = []
    for sample in dataset:
        p.append(sample[1].split(' '))
        y.append(sample[0].split(' '))

    p = np.array(p, dtype='float32') / 255
    y = np.array(y, dtype='uint8')

    ###
    # reshaping to image (from 1D):
    x = np.zeros((len(p), 1, 48, 48), dtype='float32')
    for i in range(len(p)):
        pp = np.reshape(p[i], (48, 48, 1))
        x[i] = np.transpose(pp, (2, 0, 1))
        # print x[i]#.astype('uint8')
        # cv2.imshow('x', pp)
        # cv2.waitKey(0)

    ###
    # neural net trainer:
    model_description = 'model_weights'
    size_batch = 32
    epoches_number = 10000
    validation_portion = 0.1833

    # training / validation separation:
    data_length = len(x)
    X_train = x[:int(1 - validation_portion * data_length)]
    Y_train = y[:int(1 - validation_portion * data_length)]
    X_test = x[int(1 - validation_portion * data_length):]
    Y_test = y[int(1 - validation_portion * data_length):]

    # compiling net object:
    input_shape = X_train[0].shape
    model = net(input_shape)
    model.summary()

    optimizer_method = 'adam'
    model.compile(loss='binary_crossentropy', optimizer=optimizer_method, metrics=['accuracy'])

    EarlyStopping(monitor='val_loss', patience=0, verbose=1)
    checkpointer = ModelCheckpoint(model_description + '.hdf5', verbose=1, save_best_only=True)

    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=20,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    # compute quantities required for featurewise normalization
    # (std, mean, and principal components if ZCA whitening is applied)
    datagen.fit(X_train)

    # fit the model on the batches generated by datagen.flow()
    model.fit_generator(datagen.flow(X_train, Y_train, shuffle=True, batch_size=size_batch),
                        nb_epoch=epoches_number, verbose=1, validation_data=(X_test, Y_test),
                        callbacks=[checkpointer], class_weight=None, max_q_size=10, samples_per_epoch=len(X_train))


def emotion_detector(input_images_list):

    # fit to net:
    input_shape = (48, 48)
    output_images_list = []
    for image in input_images_list:
        shape = image.shape
        output_images_size = shape[:2]
        if shape[2] > 1:
            image = cv2.cvtColot(image, cv2.BGR2GRAY)
        # shrinking oversized images:
        if image.shape[0] > input_shape[0] or image.shape[1] > input_shape[1]:
            if image.shape[0] > image.shape[1]:
                scale = 1.0 * input_shape[0] / image.shape[0]
            else:
                scale = 1.0 * input_shape[1] / image.shape[1]
            image = cv2.resize(image.copy(), input_shape)
            output_images_size = image.shape[:2]

        border_type = cv2.BORDER_REPLICATE
        # getting image size:
        h_max, w_max = input_shape  # output_size
        h, w = output_images_size
        w_shift = w_max - w
        h_shift = h_max - h
        output_image = cv2.copyMakeBorder(image.copy(), h_shift/2, h_shift/2, w_shift/2, w_shift/2, border_type)
        output_image = cv2.resize(output_image, input_shape)
        output_image = np.transpose(output_image, (2, 0, 1))
        output_image.append(output_image)
        output_images_list = np.array(output_images_list, dtype='float32')/255

    # run test on image list:
    model = net(input_shape)
    current_directory_name = os.getcwd()
    model.load_weights(os.path.join(current_directory_name, 'model_weights.hdf5'))
    optimizer_method = 'adam'
    model.compile(loss='binary_crossentropy', optimizer=optimizer_method, metrics=['accuracy'])
    probability = model.predict_proba(output_images_list, batch_size=len(output_images_list))
    classes = model.predict_classes(output_images_list, batch_size=len(output_images_list))

    return probability, classes

train()