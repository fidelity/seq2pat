import keras
import keras.backend as K
from keras import layers
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, Concatenate
from keras.models import Model, Sequential
from keras import initializers, regularizers, optimizers, layers

def shallow_NN(num_features, num_classes, layer_nodes=[512], optimizer='adam'):
    
    model = Sequential()
    model.add(Input(shape=(num_features)))
    for i in range(len(layer_nodes)):
        model.add(Dense(layer_nodes[i], activation="sigmoid"))
    model.add(Dense(num_classes, activation="softmax"))

    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=['accuracy'])
    
    return model

def vanilla_LSTM(vocab_size, embedding_dim, num_lstm_units, input_len, num_classes, 
                 layer_nodes=[512], optimizer='adam'):
    
    model = Sequential()
    model.add(Input(shape=(input_len,)))
    model.add(Embedding(vocab_size, embedding_dim))
    model.add(LSTM(units=num_lstm_units))  
    for i in range(len(layer_nodes)):
        model.add(Dense(layer_nodes[i], activation="sigmoid"))
    model.add(Dense(num_classes, activation="softmax"))

    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=['accuracy'])
    
    return model

def pat_LSTM(vocab_size, embedding_dim, num_lstm_units, input_len, num_pattern_features,
                 num_classes, layer_nodes=[512], optimizer='adam'):
    
    input_lstm = Input(shape=(input_len,))
    input_pat_feat = Input(shape=(num_pattern_features))
    
    lstm = Embedding(vocab_size, embedding_dim)(input_lstm)
    output_lstm = LSTM(units=num_lstm_units)(lstm)
    
    merged_nodes = Concatenate(axis=-1)([output_lstm, input_pat_feat])
    
    for i in range(len(layer_nodes)):
        merged_nodes = Dense(layer_nodes[i], activation="sigmoid")(merged_nodes)
        
    output = Dense(num_classes, activation="softmax")(merged_nodes)
    
    model = Model(inputs=[input_lstm, input_pat_feat], outputs=output)

    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=['accuracy'])
    
    return model

def keras_categorical(y, num_class):
    return keras.utils.to_categorical(y, num_classes=num_class)

# Customize early stopper
class CustomStopper(keras.callbacks.EarlyStopping):
    # add argument for starting epoch
    def __init__(self, monitor='val_loss', min_delta=0, patience=0, verbose=0, mode='auto', 
                 start_epoch=40, restore_best_weights=False):
        super().__init__(monitor=monitor, min_delta=min_delta, patience=patience, verbose=verbose,
                         mode=mode, restore_best_weights=restore_best_weights)
        self.start_epoch = start_epoch

    def on_epoch_end(self, epoch, logs=None):
        if epoch > self.start_epoch:
            super().on_epoch_end(epoch, logs)