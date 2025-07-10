import numpy as np

class SpamClassifier:
    def __init__(self, learning_rate=0.001, num_iterations=1000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = 0.0

    def train(self, x_data, y):
        # Gets number of samples
        num_samples = x_data.shape[0]
        # Gets number of features
        num_features = x_data.shape[1]

        # Initialise the weight and bias (Step 1)
        self.weights = np.zeros(num_features)
        self.bias = 0.0

        # Gradient Descent
        for iteration in range(self.num_iterations):
            # Finds z for the sigmoid equation (Step 2)
            z = -(np.dot(x_data, self.weights) + self.bias)
            # Sigmoid Function (Step 2)
            y_hat = 1 / (1 + np.exp(z))

            # Calculate Error (Step 3)
            error = y_hat - y

            # Update the gradient Descent (Step 4)
            dw = np.dot(x_data.T, error) / num_samples
            db = np.mean(error)

            # Update the weights and bias (Step 5)
            self.weights = self.weights - self.learning_rate * dw
            self.bias = self.bias - self.learning_rate * db

    def predict(self, x_input):
        z = -(np.dot(x_input, self.weights) + self.bias)
        probs = 1 / (1 + np.exp(z))

        return np.round(probs >= 0.5).astype(int)

def create_classifier():
    spam_model = SpamClassifier(learning_rate=0.1, num_iterations=2500)

    training_spam = np.loadtxt(open("data/training_spam.csv"), delimiter=",").astype(int)

    X_train = training_spam[:, 1:]
    y_train = training_spam[:, 0]

    spam_model.train(X_train, y_train)
    return spam_model

classifier = create_classifier()