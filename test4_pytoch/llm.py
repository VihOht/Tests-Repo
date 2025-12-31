import numpy as np

def euclidian_dist(x1, x2):
    return [np.sqrt(np.sum((x1 - xi)**2)) for xi in x2]


def count_occurrences(l):
    occur = {}
    for el in l:
        if el in occur:
            occur[el] += 1
        else:
            occur[el] = 1
    
    tuple_occur = list(sorted(occur.items(), reverse=True, key=lambda t: t[1]))
    return tuple_occur

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
    
def Relu(x):
    return np.maximum(0, x)

class KNN:
    def __init__(self, k):
        self.k = k
        
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        
    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        return predictions
        
    def _predict(self, x):
        # Calculate distances
        distances = euclidian_dist(x, self.X_train)
        
        # Calculate the nearest k
        nearest_indices = np.argsort(distances)[:self.k]
        nearest_labels = [self.y_train[i] for i in nearest_indices]
        
        # Count occurrences
        frequencies = count_occurrences(nearest_labels)
        return frequencies[0][0]

class LinearRegression:
    def __init__(self, lr=0.001, n_iters=10000):
        self.n_iters = n_iters
        self.lr = lr
        self.bias = None
        self.weights = None
        
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        self._train(X, y)
        
        
    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        return predictions
    
    def _predict(self, x):
        return np.sum(x * self.weights) + self.bias
        
        
    def _train(self, X_train, y_train):
        for i in range(self.n_iters):
            # Forward
            pred_y = self.predict(X_train)
            
            # Calculate loss and optimize
            loss = self.fn(y_train, pred_y, X_train)
            if i % max(1, int(self.n_iters * 0.2)) == 0:
                print("Loss: " + str(loss))
    
    def fn(self, y_target, y, X):
        loss, dw, db = self._calcMSQ(y_target, y, X)
        self.weights = self.weights - self.lr * dw
        self.bias = self.bias - self.lr * db
        return loss
            
            
            
    def _calcMSQ(self, y_target, y, X):
        dy = y - y_target
        n = len(y)
        loss = (1/n) * np.sum(dy**2)
        dw = (1/n) * 2 * np.dot(X.transpose(), dy)
        db = (1/n) * 2 * np.sum(dy)
        return loss, dw, db
    
    def score(self, X_test, y_test):
        y_pred = self.predict(X_test)
        y_pred = np.array(y_pred)
        y_test = np.array(y_test)
        ss_res = np.sum((y_test - y_pred) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2_score = 1 - (ss_res / ss_tot)
        return r2_score
    

class LogisticRegression:
    def __init__(self, lr=0.001, n_iters=10000):
        self.n_iters = n_iters
        self.lr = lr
        self.bias = None
        self.weights = None
        
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        self._train(X, y)
        
        
    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        class_preds = [1 if p >= 0.5 else 0 for p in predictions]
        return class_preds
    
    def _predict(self, x):
        linear_output = np.sum(x * self.weights) + self.bias
        return sigmoid(linear_output)
    
    def _train(self, X_train, y_train):
        for i in range(self.n_iters):
            # Forward
            pred_y = self.predict(X_train)
            
            # Calculate loss and optimize
            loss = self.fn(y_train, pred_y, X_train)
            if i % max(1, int(self.n_iters * 0.2)) == 0:
                print("Loss: " + str(loss))
    
    def fn(self, y_target, y, X):
        loss, dw, db = self._calcLogLoss(y_target, y, X)
        self.weights = self.weights - self.lr * dw
        self.bias = self.bias - self.lr * db
        return loss
    
    def _calcLogLoss(self, y_target, y, X):
        n = len(y)
        dy = y - y_target
        loss = - (1/n) * np.sum(y_target * np.log(y) + (1 - y_target) * np.log(1 - y))
        dw = (1/n) * np.dot(X.T, dy)
        db = (1/n) * np.sum(dy)
        return loss, dw, db



# Functions and it's derivatives
class FModel():
    def __init__(self):
        self.result = None
        self.derivative = None
    
    def pred(self):
        pass
    
    def __call__(self, X: np.ndarray) -> np.ndarray:
        self.result = self.pred(X)
        self.derivative = self.der(X)
        return self.result
    
    def update(self):
        pass
    
    def der(self):
        pass

class LinearF(FModel):
    def __init__(self, in_features):
        self.id = None
        self.weights = np.random.rand(in_features)
        self.bias = np.random.rand(1)
        
    def update(self, dw, db, lr):
        self.weights -= lr * dw
        self.bias -= lr * db
        
    def der(self, X):
        return (self.weights, X)

    def pred(self, X):
        return [self._pred(x) for x in X]
    
    def _pred(self, x):
        return np.sum(x * self.weights) + self.bias
    
class ReluF(FModel):
    def der(self, X):
        return (X > 0).astype(int)
    def pred(self, X):
        return np.where(X > 0, X, 0)
        

class ModelBase:
    def __init__(self):
        self.fn = None
        self.fnd = None
        self.fnr = None

    def forward(self, X):
        pass

    def backward(self, y):
        pass
    
class Models0():
    linear1 = LinearF(in_features=2)
    linear2 = LinearF(in_features=1)
    
    def __init__(self):
        self.results = []
        self.gradients = []
        self.X = None
        self.lr = 0.01
    
    def forward(self, X):
        self.X = X
        x = self.sequence(X, linear1=self.linear1, linear2=self.linear2)
        return x
    
    def sequence(self, X, **args):
        result = X
        for name, layer in args.items():
            layer_output = layer(result)
            self.results.append({'name': name, 'output': layer_output})
            result = layer_output
        # transpose and remove extra brackets
        result = np.array(result).flatten()
        return result

    def fn(self, y_true, y_pred):
        loss = np.mean((y_true - y_pred) ** 2)
        dy = np.sum(y_pred - y_true) * (2 / len(y_true))
        return loss, dy
    
    def backward(self):
        self.results.reverse()
        y = self.forward(self.X)
        loss, dy = self.fn(y_true=np.array([1, 2, 3]), y_pred=y)
        print(f"Loss: {dy}")
        self.gradients.append(dy)
        for res in self.results:
            name = res['name']
            output = res['output']
            print(f"Backward through layer: {name}")
            print(f"Output during forward: {output}")
            
            layer = getattr(self, name)
            derivative = layer.derivative
            result = layer.result
            
            if isinstance(layer, LinearF):
                dw, db = derivative
                dtw = self.gradients[-1] * dw
                self.gradients.append(dtw)
                dtb = self.gradients[-2]
                self.gradients.append(dtb)
                print(f"dw: {dw}, db: {db}")
                
                layer.update(dtw, dtb, self.lr)
            print(f"Layer result: {result}")
            print(f"Derivative: {derivative}")


