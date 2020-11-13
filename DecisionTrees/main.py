import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import tree
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

if __name__ == "__main__":
    dataset = pd.read_excel(r"HW3Data.xlsx")

    # Assign variables for x and y along with class
    coord = dataset.drop('Class', axis=1)
    class_val = dataset['Class']

    # Create training and test data
    X_train, X_test, y_train, y_test = train_test_split(coord, class_val, test_size=0.30)

    # Train the decision tree algorithm
    classifier = DecisionTreeClassifier()
    model_fit = classifier.fit(X_train, y_train)

    # Make a prediction on the test data.
    y_xlsx_pred = classifier.predict(X_test)

    # Display Results
    print('\nExcel Results')

    print('\nDecision Tree:')
    text_representation = tree.export_text(model_fit)
    print(text_representation)

    print('\nConfusion Matrix:')
    print(confusion_matrix(y_test, y_xlsx_pred))

    print('\nClassification Report:')
    print(classification_report(y_test, y_xlsx_pred))

    # Create grid of X Y coordinate values
    grid = np.empty((0, 2), int)
    for i in range(70):
        for j in range(70):
            grid = np.append(grid, np.array([[i, j]]), axis=0)
    print(grid)

    # Initialize grid dataframe and predictions
    grid_df = pd.DataFrame(grid, columns=["X", "Y"])
    y_grid_pred = classifier.predict(grid_df).reshape((70, 70))

    # Add colormap to grid
    cmap = colors.ListedColormap(['blue', 'red'])
    bounds = [0, 0.5, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Display grid and scatter data
    fig, ax = plt.subplots(nrows=2)
    ax[0].imshow(y_grid_pred, cmap=cmap, norm=norm)

    ax[0].grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    ax[0].set_xticks(np.arange(0, 69, 1))
    ax[0].set_yticks(np.arange(0, 69, 1))
    ax[0].set_xticklabels([])
    ax[0].set_yticklabels([])

    x_vals = dataset["X"]
    y_vals = dataset["Y"]

    ax[1].scatter(x_vals, y_vals, color='k', s=2)

    plt.show()
