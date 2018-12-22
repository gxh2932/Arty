import tensorflow.keras
from tensorflow.keras.layers import Activation, Dense, Input, TimeDistributed, LSTM, Dropout, Lambda
from tensorflow.keras.models import Model

def create_model():    
    layer_in = Input(batch_shape=(1, None), dtype='uint8')
    
    _ = Lambda(lambda x: tensorflow.keras.backend.one_hot(x, 256))(layer_in)
    
    _ = LSTM(512, recurrent_activation='sigmoid', return_sequences=True, stateful=True)(_)
    _ = LSTM(512, recurrent_activation='sigmoid', return_sequences=True, stateful=True)(_)
    _ = LSTM(512, recurrent_activation='sigmoid', return_sequences=True, stateful=True)(_)
    
    _ = TimeDistributed(Dense(256))(_)
    layer_out = Activation('softmax')(_)
    
    model = Model(inputs=[layer_in], outputs=[layer_out])
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model
