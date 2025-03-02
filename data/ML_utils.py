# cross validation
import numpy as np
from sklearn.model_selection import KFold

def kfold_split(good_matrices, bad_matrices, n_splits=10, shuffle=True, random_state=None):
    good_labels = np.ones(len(good_matrices))  # Label 1 for good_matrices
    bad_labels = np.zeros(len(bad_matrices))   # Label 0 for bad_matrices
    
    # Combine data and labels
    X = np.vstack((good_matrices, bad_matrices))
    y = np.concatenate((good_labels, bad_labels))
    
    kf = KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
    
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        yield X_train, X_test, y_train, y_test
