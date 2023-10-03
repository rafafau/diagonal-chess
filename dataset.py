import ai
import board
import pieces
import numpy as np
import random
import main
import tensorflow


import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.utils as utils
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.callbacks as callbacks
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import models
from keras.models import Sequential
from keras.layers import Dense



def build_model(conv_size, conv_depth):
    board3d = layers.Input(shape=(17, 8, 8))

    # adding the convolutional layers
    x = board3d
    for _ in range(conv_depth):
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, 'relu')(x)
    x = layers.Dense(1, 'sigmoid')(x)

    return models.Model(inputs=board3d, outputs=x)


def build_model_residual(conv_size, conv_depth):
    board3d = layers.Input(shape=(17, 8, 8))

    # adding the convolutional layers
    x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(board3d)
    for _ in range(conv_depth):
        previous = x
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Add()([x, previous])
        x = layers.Activation('relu')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(1, 'sigmoid')(x)

    return models.Model(inputs=board3d, outputs=x)

def get_dataset(name):
	container = np.load(name)
	x_train, y_train = container['x_train'], container['y_train']
	# y_train = np.asarray(y_train / abs(y_train).max() / 2 + 0.5, dtype=np.float32)
	return x_train, y_train


def model_save(model):
    model.compile(optimizer=optimizers.Adam(5e-4), loss='mean_squared_error')
    model.summary()
    checkpoint_filepath = '/tmp/model.h5'
    model_checkpointing_callback = ModelCheckpoint(
        filepath = checkpoint_filepath,
        # save_best_only= True,
    )
    model.fit(x_train, y_train,
            batch_size=2048,
            epochs=1000,
            verbose=1,
            validation_split=0.1,
            callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                        callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4),model_checkpointing_callback])

    model.save('model.h5', save_format="h5")    


def random_board(max_depth=200):
    chessboard = board.Board.new()
    depth = random.randrange(0, max_depth)
    maximazing = True
    for _ in range(depth):
        if maximazing:
            maximazing = False
            all_moves = list(chessboard.get_possible_moves(pieces.Piece.WHITE))
            random_move = random.choice(all_moves)
            chessboard.perform_move(random_move)
            if chessboard.is_checked(pieces.Piece.BLACK):
                break
        else:
            maximazing = True
            all_moves = list(chessboard.get_possible_moves(pieces.Piece.BLACK))
            random_move = random.choice(all_moves)
            chessboard.perform_move(random_move)
            if chessboard.is_checked(pieces.Piece.WHITE):
                break

    if maximazing:
        score = ai.AI.get_ai_move(chessboard, pieces.Piece.WHITE)[1]
    else:
        score = ai.AI.get_ai_move(chessboard, pieces.Piece.BLACK)[1]

    return chessboard.split_dims(chessboard, maximazing), score


# chessboard = board.Board.new()
# split = chessboard.split_dims(chessboard, True)
# x_train_arr = np.array([split], dtype=np.float32)
# score = ai.Heuristics.get_material_score(chessboard)
# y_train_arr = np.array([score], dtype=np.float32)
# np.savez('dataset.npz', x_train=x_train_arr, y_train=y_train_arr)
# print(y_train_arr)

# for n in range(200):
#     random.seed(n)
#     rand_board, score = random_board()
#     x_train_arr = np.array([rand_board], dtype=np.float32)
#     y_train_arr = np.array([score], dtype=np.float32)
#     for n in range(9):
#         rand_board, score = random_board()
#         x_train_arr = np.append(x_train_arr, np.array([rand_board], dtype=np.float32), axis=0)
#         y_train_arr = np.append(y_train_arr, [score])
#     x_train, y_train = get_dataset("dataset.npz")
#     x_train = np.append(x_train, x_train_arr, axis=0)
#     y_train = np.append(y_train, y_train_arr, axis=0)
#     print(len(y_train))
#     np.savez('dataset.npz', x_train=x_train, y_train=y_train)
    

x_train, y_train = get_dataset("dataset.npz")
print(y_train[:10])
y_train = np.asarray(y_train / abs(y_train).max() / 2 + 0.5, dtype=np.float32)

model = build_model_residual(32, 4)
model_save(model)
