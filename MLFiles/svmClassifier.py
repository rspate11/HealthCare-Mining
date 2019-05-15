import pandas as pd

# sklearn libraries
from sklearn.model_selection import train_test_split
from sklearn.svm             import SVC
from sklearn.metrics         import classification_report, confusion_matrix

kernelType = int(input("""
                        which kernel to use: \n
                        1: linear
                        2: poly
                        3: gaussian
                        4: sigmoid                        
"""))

bankdata = pd.read_csv("data/bill_authentication.csv")

# separate the features and labels
X = bankdata.drop('Class', axis=1)
y = bankdata['Class']

# split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)


# train the svm on the training data, using the "linear" kernel
kernelTypeDict = {
    1: "linear",
    2: "poly",
    3: "rbf",
    4: "sigmoid"
}
svclassifier = SVC(kernel=kernelTypeDict[kernelType])
svclassifier.fit(X_train, y_train)

# predict on the test data
y_pred = svclassifier.predict(X_test)

# find precision, recall, f1-score and support
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

