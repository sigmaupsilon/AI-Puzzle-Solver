import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier


def run_nn_model(hidden_layers_sizes: int, x_train, x_test, y_train, y_test):
    print("Single-layer model ran using " + str(hidden_layers_sizes) + " neurons")

    # Create grid of X Y coordinate values
    grid = np.empty((0, 2), int)
    for i in range(70):
        for j in range(70):
            grid = np.append(grid, np.array([[i, j]]), axis=0)

    # Make a prediction on the test data.
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)
    grid = scaler.transform(grid)

    mlp = MLPClassifier(hidden_layer_sizes=hidden_layers_sizes)
    mlp.fit(x_train, y_train)

    train_pred = mlp.predict(x_train)

    test_pred = mlp.predict(x_test)

    grid_pred = mlp.predict(grid)

    # Count mismatches and build colormap for points
    cmapped_points = [0, np.empty(0)]
    for i in range(x_train.shape[0]):
        mismatch = False

        if class_val[i] != train_pred[i]:
            cmapped_points[0] += 1
            mismatch = True

        if train_pred[i] == 1 and not mismatch:
            cmapped_points[1] = np.append(cmapped_points[1], np.array(["1"]), axis=0)
        elif train_pred[i] == 1 and mismatch:
            cmapped_points[1] = np.append(cmapped_points[1], np.array(["1 Mismatch"]), axis=0)
        elif train_pred[i] == 0 and not mismatch:
            cmapped_points[1] = np.append(cmapped_points[1], np.array(["0"]), axis=0)
        else:
            cmapped_points[1] = np.append(cmapped_points[1], np.array(["0 Mismatch"]), axis=0)

    # Plot Training Prediction Data
    cdict = {"0": "k", "0 Mismatch": "b", "1": "r", "1 Mismatch": "m"}
    for g in np.unique(cmapped_points[1]):
        ix = np.where(cmapped_points[1] == g)
        plt.scatter(x_train[ix[0], 0], x_train[ix[0], 1], c=cdict[g], label=g)

    plt.text(2, 2, "Mismatches = " + str(cmapped_points[0]), fontsize=12, color='g')
    plt.legend()

    # Display Test Data Results
    print('\nTest Data Results')

    print('\nConfusion Matrix:')
    print(confusion_matrix(y_test, test_pred))

    print('\nPerformance Metrics:')
    print(classification_report(y_test, test_pred))

    # Grid Prediction Reshaping
    y_grid_pred = grid_pred.reshape((70, 70))

    # Add colormap to grid
    cmap = colors.ListedColormap(['black', 'red'])
    bounds = [0, 0.5, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Display grid and scatter data
    plt.figure()
    plt.imshow(y_grid_pred, cmap=cmap, norm=norm)

    plt.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    plt.xticks(np.arange(0, 69, 1), [])
    plt.yticks(np.arange(0, 69, 1), [])

    plt.show()


if __name__ == "__main__":
    # Read Excel data
    dataset = pd.read_excel(r"HW3Data.xlsx")

    # Assign variables for x and y along with class
    coord = dataset.drop('Class', axis=1)
    class_val = dataset['Class']

    # Create training and test data
    x_train, x_test, y_train, y_test = train_test_split(coord, class_val, test_size=0.30)

    run_nn_model(2, x_train, x_test, y_train, y_test)
    run_nn_model(6, x_train, x_test, y_train, y_test)
