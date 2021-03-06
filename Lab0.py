
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
import random


# Setting random seeds to keep everything deterministic.
random.seed(1618)
np.random.seed(1618)
#tf.set_random_seed(1618)   # Uncomment for TF1.
tf.random.set_seed(1618)

# Disable some troublesome logging.
#tf.logging.set_verbosity(tf.logging.ERROR)   # Uncomment for TF1.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Information on dataset.
NUM_CLASSES = 10
IMAGE_SIZE = 784

# Use these to set the algorithm to use.
#ALGORITHM = "guesser"
#ALGORITHM = "custom_net"
ALGORITHM = "tf_net"





class NeuralNetwork_2Layer():
    def __init__(self, inputSize, outputSize, neuronsPerLayer, learningRate = 0.1):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.neuronsPerLayer = neuronsPerLayer
        self.lr = learningRate
        self.W1 = np.random.randn(self.inputSize, self.neuronsPerLayer)
        self.W2 = np.random.randn(self.neuronsPerLayer, self.outputSize)

    # Activation function.
    def __sigmoid(self, x):
        #TODO: implement
        return (1 / (1 + np.exp(-x)))

    # Activation prime function.
    def __sigmoidDerivative(self, x):
        #TODO: implement
        s = 1 / (1 + np.exp(-x))
        ds = s * (1 - s)
        return ds


    # Batch generator for mini-batches. Not randomized.
    def __batchGenerator(self, l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]


    # Training with backpropagation.
    def train(self, xVals, yVals, epochs = 100, minibatches = True, mbs = 100):
        #TODO: Implement backprop. allow minibatches. mbs should specify the size of each minibatch.
        for j in range(epochs):
            if minibatches:
                xGen = self.__batchGenerator(xVals, mbs)
                yGen = self.__batchGenerator(yVals, mbs)
                for k in range(600):
                    xBatch = next(xGen)
                    yBatch = next(yGen)
                    l1out, l2out = self.__forward(xBatch)
                    l2_delta = (l2out - yBatch) * self.__sigmoidDerivative(l1out.dot(self.W2))
                    l1_delta = l2_delta.dot(self.W2.T) * self.__sigmoidDerivative(xBatch.dot(self.W1))
                    self.W2 -= l1out.T.dot(l2_delta)
                    self.W1 -= xBatch.T.dot(l1_delta)
            else:
                l1out, l2out = self.__forward(xVals)
                l2_delta = (l2out - yVals) * (l2out * (1 - l2out))
                l1_delta = l2_delta.dot(self.W2.T) * (l1out * (1 - l1out))
                self.W2 -= l1out.T.dot(l2_delta)
                self.W1 -= xVals.T.dot(l1_delta)

    # Forward pass.
    def __forward(self, input):
        layer1 = self.__sigmoid(np.dot(input, self.W1))
        layer2 = self.__sigmoid(np.dot(layer1, self.W2))
        return layer1, layer2

    # Predict.
    def predict(self, xVals):
        _, layer2 = self.__forward(xVals)
        return layer2



# Classifier that just guesses the class label.
def guesserClassifier(xTest):
    ans = []
    for entry in xTest:
        pred = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        pred[random.randint(0, 9)] = 1
        ans.append(pred)
    return np.array(ans)



#=========================<Pipeline Functions>==================================

def getRawData():
    mnist = tf.keras.datasets.mnist
    (xTrain, yTrain), (xTest, yTest) = mnist.load_data()
    print("Shape of xTrain dataset: %s." % str(xTrain.shape))
    print("Shape of yTrain dataset: %s." % str(yTrain.shape))
    print("Shape of xTest dataset: %s." % str(xTest.shape))
    print("Shape of yTest dataset: %s." % str(yTest.shape))
    return ((xTrain, yTrain), (xTest, yTest))



def preprocessData(raw):
    ((xTrain, yTrain), (xTest, yTest)) = raw
    xTrain, xTest = xTrain / 255.0, xTest / 255.0 #TODO: Add range reduction here (0-255 ==> 0.0-1.0).
    yTrainP = to_categorical(yTrain, NUM_CLASSES)
    yTestP = to_categorical(yTest, NUM_CLASSES)
    print("New shape of xTrain dataset: %s." % str(xTrain.shape))
    print("New shape of xTest dataset: %s." % str(xTest.shape))
    print("New shape of yTrain dataset: %s." % str(yTrainP.shape))
    print("New shape of yTest dataset: %s." % str(yTestP.shape))
    return ((xTrain, yTrainP), (xTest, yTestP))



def trainModel(data):
    xTrain, yTrain = data
    if ALGORITHM == "guesser":
        return None   # Guesser has no model, as it is just guessing.
    elif ALGORITHM == "custom_net":
        print("Building and training Custom_NN.")
        #TODO: Write code to build and train your custon neural net.
        model = NeuralNetwork_2Layer(IMAGE_SIZE, NUM_CLASSES, 10000)
        xTrain_mod = xTrain.reshape(60000, IMAGE_SIZE)
        model.train(xTrain_mod, yTrain)
        return model
    elif ALGORITHM == "tf_net":
        print("Building and training TF_NN.")
        #TODO: Write code to build and train your keras neural net.
        model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')])
        model.compile(optimizer='adam', loss=tf.keras.losses.categorical_crossentropy)
        model.fit(xTrain, yTrain, epochs=10)
        return model
    else:
        raise ValueError("Algorithm not recognized.")



def runModel(data, model):
    if ALGORITHM == "guesser":
        return guesserClassifier(data)
    elif ALGORITHM == "custom_net":
        print("Testing Custom_NN.")
        #TODO: Write code to run your custon neural net.
        xTest_mod = data.reshape(10000, IMAGE_SIZE)
        predict = model.predict(xTest_mod)
        one_hot = (predict == predict.max(axis=1)[:, None]).astype(int)
        return one_hot
    elif ALGORITHM == "tf_net":
        print("Testing TF_NN.")
        #TODO: Write code to run your keras neural net.
        predict = model.predict(data)
        return (predict == predict.max(axis=1)[:, None]).astype(int)
    else:
        raise ValueError("Algorithm not recognized.")



def evalResults(data, preds):   #TODO: Add F1 score confusion matrix here.
    xTest, yTest = data
    acc = 0
    matrix = np.zeros((10, 10))
    for i in range(preds.shape[0]):
        p = np.argmax(preds[i])
        y = np.argmax(yTest[i])
        matrix[p][y] += 1
        if np.array_equal(preds[i], yTest[i]):   acc = acc + 1
    accuracy = acc / preds.shape[0]
    print("Classifier algorithm: %s" % ALGORITHM)

    for j in range(10):
        tp = matrix[j][j]
        fp = np.sum(matrix, axis=1)[j] - tp
        fn = np.sum(matrix, axis=0)[j] - tp
        prec = tp / (tp + fp)
        rec = tp / (tp + fn)
        f1 = 2 * ((prec * rec) / (prec + rec))
        print(str(j) + '\tprecision: ' + str(prec) + '\trecall: ' + str(rec) + '\tf1-score: ' + str(f1))

    print("Classifier accuracy: %f%%" % (accuracy * 100))
    print()



#=========================<Main>================================================

def main():
    raw = getRawData()
    data = preprocessData(raw)
    model = trainModel(data[0])
    preds = runModel(data[1][0], model)
    evalResults(data[1], preds)



if __name__ == '__main__':
    main()
