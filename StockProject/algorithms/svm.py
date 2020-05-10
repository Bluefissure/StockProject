import pandas as pd
from numpy.random import shuffle
from sklearn import svm
import joblib
from sklearn import metrics

inputfile = './data'
outputfile1 = './AMZN_out1.csv'
outputfile2 = './AMZN_out2.csv'


def readData():
    data = pd.read_csv(inputfile, encoding='utf8')
    data = data.as_matrix().astype(float)
    shuffle(data)
    data_train = data[:int(0.8 * len(data)), :]
    data_test = data[int(0.8 * len(data)):, :]
    return data_train, data_test


def train(data_train, data_test):
    x_train = data_train[:, 2:] * 30
    y_train = data_train[:, 0].astype(int)
    x_test = data_test[:, 2:] * 30
    y_test = data_test[:, 0].astype(int)

    model = svm.SVC(C=1.0, kernel='rbf', gamma='auto', decision_function_shape='ovr', cache_size=500)

    model.fit(x_train, y_train)
    joblib.dump(model, './Models/WaterEval_svm.model')
    return x_train, y_train, x_test, y_test


def eval(x_train, y_train, x_test, y_test):
    model = joblib.load('./Models/WaterEval_svm.model')
    print("Train Score：" + str(model.score(x_train, y_train)))
    print("Test Score：" + str(model.score(x_test, y_test)))

    cm_train = metrics.confusion_matrix(y_train, model.predict(x_train))
    cm_test = metrics.confusion_matrix(y_test, model.predict(x_test))
    pd.DataFrame(cm_train, index=range(1, 6), columns=range(1, 6)).to_csv(outputfile1)
    pd.DataFrame(cm_test, index=range(1, 6), columns=range(1, 6)).to_csv(outputfile2)


if __name__ == '__main__':
    data_train, data_test = readData()
    x_train, y_train, x_test, y_test = train(data_train, data_test)
    eval(x_train, y_train, x_test, y_test)