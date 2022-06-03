from tensorflow.keras import Sequential, layers

def initialize_model(X):

    #################################
    #  1 - Model architecture       #
    #################################

    model = Sequential()

    # Input Layer
    model.add(layers.Dense(20, activation='relu', input_dim = X.shape[-1]))

    # Hidden Layers
    model.add(layers.Dense(15, activation='relu'))
    model.add(layers.Dense(15, activation='relu'))
    model.add(layers.Dense(20, activation='relu'))

    # Predictive Layer
    model.add(layers.Dense(1, activation='linear'))

    ##################################
    #  2 - Our recommended compiler  #
    ##################################

    model.compile(optimizer='adam',
                  loss='msle')

    return model
