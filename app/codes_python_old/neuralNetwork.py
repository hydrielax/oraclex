import numpy as np

class NeuralNetwork(object):
    def __init__(self, n_layerInput, n_layerHidden, n_layerFinal, learNate):
        self.input = n_layerInput
        self.hidden = n_layerHidden
        self.ans = n_layerFinal
        self.learningRate = learNate

        self.w1 = np.random.randn(n_layerHidden, n_layerInput)
        self.w2 = np.random.randn(n_layerFinal, n_layerHidden)
        self.b1 = np.random.randn(n_layerHidden, 1)
        self.b2 = np.random.randn(n_layerFinal, 1)

        # self.w1 = np.array([[1,1],[1,1]])
        # self.w2 = np.array([[2, 2], [2, 2], [2, 2]])
        # self.b1 = np.array([[2], [2]])
        # self.b2 = np.array([[1], [1], [1]])

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def sigmoid_dev(self, x):
        return self.sigmoid(x)*(1-self.sigmoid(x))

    def forwardProp(self, input):
        self.Xsig = self.sigmoid(input)
        self.z2 = np.dot(self.w1, self.Xsig) + self.b1
        self.a2 = self.sigmoid (self.z2)
        self.z3 = np.dot(self.w2, self.a2) + self.b2
        self.a3 = self.sigmoid(self.z3)
        return self.a3

    def backwardProp(self, a3, y, input):
        self.dC_da3 = (a3-y)  # Transformation colonne
        self.da3_dz3 = self.sigmoid_dev(self.z3)
        self.dz3_dw1 = self.a2

        self.gradC_w2_p1 =  np.dot((self.da3_dz3), (self.a2).T)
        self.gradC_w2 = self.gradC_w2_p1* (self.dC_da3.reshape(1,-1)[0][:, np.newaxis]) #Multiply lines of gradC_w2_p1 for (a3-y)
        self.gradC_b2 = (self.dC_da3)*(self.da3_dz3)


        self.intermediate = np.dot( (self.da3_dz3.T)*(self.dC_da3.T), self.w2)
        self.intermediate2 = np.dot((self.intermediate).T, self.sigmoid(input).reshape(1,-1)) # Multiply lines of intermediate for input

        self.sigZ1 = self.sigmoid_dev(self.z2)
        self.gradC_w1 = self.intermediate2 * (self.sigZ1.reshape(1,-1)[0][:,np.newaxis]) # Multiply lines of intermediate2 for sigma'(1)

        self.gradC_b1 = (self.intermediate.T)*(self.sigZ1)

        # Propagation

        self.w1 -= (self.learningRate)*self.gradC_w1
        self.w2 -= (self.learningRate)*self.gradC_w2

        self.b1 -= (self.learningRate)*self.gradC_b1
        self.b2 -= (self.learningRate)*self.gradC_b2

    def train(self, input, y):
        a3 = self.forwardProp(input)
        self.backwardProp(a3,y,input)
        return np.square(a3-y)

# a = np.array([[2, 2], [5, 3], [4,4]])
# b = np.array([0,1,2])
#
# c = np.array([[1,2, 3]])
# d = np.array([[4,5]])
#
# print ( a )
# print ( a * b[:, np.newaxis] )

NN = NeuralNetwork(2,5,3, 0.1)

X = np.array([[2,3], [5,4], [9,9]])
y = np.array([[0.1,0.1,0.1], [0.2,0.2,0.2], [0.3,0.9,0.9]])
I = np.array([[0],[2],[2]])

a3 = np.array([[0.99328288],[0.99328288],[0.99328288]])
j = 0

c1 = 10;
c2 = 10;
print (10**-6)

while (c2 > 10**-6 ):
    for i in range(3):
        p = NN.train(X[i].reshape(-1,1), y[i].reshape(-1,1))

    c1 = c2
    c2 = np.mean(p)
    j += 1

    if(j % 1000 == 0):
        print(j)
        print(c1)
        print(c2)


print(NN.forwardProp(X[0].reshape(-1,1)))
print(NN.forwardProp(X[1].reshape(-1,1)))
print(NN.forwardProp(X[2].reshape(-1,1)))