from llm import KNN, LinearRegression
from sklearn import datasets
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# Classification with KNN
# cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

# iris = datasets.load_iris()
# X, y = iris.data, iris.target

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

# plt.figure()
# plt.scatter(X_train[:,2], X_train[:,3], c=y_train, cmap=cmap, edgecolors='k', s=20)



# model = KNN(k=5)
# model.fit(X_train, y_train)

# predictions = model.predict(X_test)
# acc = np.sum(predictions == y_test) / len(y_test)
# print(f'Accuracy: {acc*100:.2f}%')

# plt.scatter(X_test[:,2], X_test[:,3], c=predictions, cmap=cmap, s=30)
# plt.show()

# Linear Regression with gradient descent

X, y = datasets.make_regression(n_samples=100, n_features=1, noise=20, random_state=1234)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

plt.scatter(X_train[:,0], y_train, color="b", marker='o', s=30)



model_1 = LinearRegression()
model_1.fit(X_train, y_train)
predictions = model_1.predict(X_test)
acc = np.sum(predictions == X_test)

plt.scatter(X_test[:,0], predictions, color="r", marker="x")
plt.show()