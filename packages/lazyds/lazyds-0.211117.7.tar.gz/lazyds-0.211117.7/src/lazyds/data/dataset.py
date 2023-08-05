from arff2pandas import a2p
from idict import idict
from pandas import read_csv, DataFrame
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import fetch_openml


def Dataset(name="wdbc"):
    return idict(dataset(name))


def dataset(name="wdbc"):
    X, y = fetch_openml(name, return_X_y=True)
    return {"X": X, "y": y}


def File(name="iris.arff"):
    """
    >>> File()
    {
        "df": "«{'sepallength@REAL': {0: 5.1, 1: 4.9, 2: 4.7, 3: 4.6, 4: 5.0, 5: 5.4, 6: 4.6, 7: 5.0, 8: 4.4, 9: 4.9, 10: 5.4, 11: 4.8, 12: 4.8, 13: 4.3, 14: 5.8, 15: 5.7, 16: 5.4, 17: 5.1, 18: 5.7, 19: 5.1, 20: 5.4, 21: 5.1, 22: 4.6, 23: 5.1, 24: 4.8, 25: 5.0, 26: 5.0, 27: 5.2, 28: 5.2, 29: 4.7, 30: 4.8, 31: 5.4, 32: 5.2, 33: 5.5, 34: 4.9, 35: 5.0, 36: 5.5, 37: 4.9, 38: 4.4, 39: 5.1, 40: 5.0, 41: 4.5, 42: 4.4, 43: 5.0, 44: 5.1, 45: 4.8, 46: 5.1, 47: 4.6, 48: 5.3, 49: 5.0, 50: 7.0, 51: 6.4, 52: 6.9, 53: 5.5, 54: 6.5, 55: 5.7, 56: 6.3, 57: 4.9, 58: 6.6, 59: 5.2, 60: 5.0, 61: 5.9, 62: 6.0, 63: 6.1, 64: 5.6, 65: 6.7, 66: 5.6, 67: 5.8, 68: 6.2, 69: 5.6, 70: 5.9, 71: 6.1, 72: 6.3, 73: 6.1, 74: 6.4, 75: 6.6, 76: 6.8, 77: 6.7, 78: 6.0, 79: 5.7, 80: 5.5, 81: 5.5, 82: 5.8, 83: 6.0, 84: 5.4, 85: 6.0, 86: 6.7, 87: 6.3, 88: 5.6, 89: 5.5, 90: 5.5, 91: 6.1, 92: 5.8, 93: 5.0, 94: 5.6, 95: 5.7, 96: 5.7, 97: 6.2, 98: 5.1, 99: 5.7, 100: 6.3, 101: 5.8, 102: 7.1, 103: 6.3, 104: 6.5, 105: 7.6, 106: 4.9, 107: 7.3, 108: 6.7, 109: 7.2, 110: 6.5, 111: 6.4, 112: 6.8, 113: 5.7, 114: 5.8, 115: 6.4, 116: 6.5, 117: 7.7, 118: 7.7, 119: 6.0, 120: 6.9, 121: 5.6, 122: 7.7, 123: 6.3, 124: 6.7, 125: 7.2, 126: 6.2, 127: 6.1, 128: 6.4, 129: 7.2, 130: 7.4, 131: 7.9, 132: 6.4, 133: 6.3, 134: 6.1, 135: 7.7, 136: 6.3, 137: 6.4, 138: 6.0, 139: 6.9, 140: 6.7, 141: 6.9, 142: 5.8, 143: 6.8, 144: 6.7, 145: 6.7, 146: 6.3, 147: 6.5, 148: 6.2, 149: 5.9}, 'sepalwidth@REAL': {0: 3.5, 1: 3.0, 2: 3.2, 3: 3.1, 4: 3.6, 5: 3.9, 6: 3.4, 7: 3.4, 8: 2.9, 9: 3.1, 10: 3.7, 11: 3.4, 12: 3.0, 13: 3.0, 14: 4.0, 15: 4.4, 16: 3.9, 17: 3.5, 18: 3.8, 19: 3.8, 20: 3.4, 21: 3.7, 22: 3.6, 23: 3.3, 24: 3.4, 25: 3.0, 26: 3.4, 27: 3.5, 28: 3.4, 29: 3.2, 30: 3.1, 31: 3.4, 32: 4.1, 33: 4.2, 34: 3.1, 35: 3.2, 36: 3.5, 37: 3.1, 38: 3.0, 39: 3.4, 40: 3.5, 41: 2.3, 42: 3.2, 43: 3.5, 44: 3.8, 45: 3.0, 46: 3.8, 47: 3.2, 48: 3.7, 49: 3.3, 50: 3.2, 51: 3.2, 52: 3.1, 53: 2.3, 54: 2.8, 55: 2.8, 56: 3.3, 57: 2.4, 58: 2.9, 59: 2.7, 60: 2.0, 61: 3.0, 62: 2.2, 63: 2.9, 64: 2.9, 65: 3.1, 66: 3.0, 67: 2.7, 68: 2.2, 69: 2.5, 70: 3.2, 71: 2.8, 72: 2.5, 73: 2.8, 74: 2.9, 75: 3.0, 76: 2.8, 77: 3.0, 78: 2.9, 79: 2.6, 80: 2.4, 81: 2.4, 82: 2.7, 83: 2.7, 84: 3.0, 85: 3.4, 86: 3.1, 87: 2.3, 88: 3.0, 89: 2.5, 90: 2.6, 91: 3.0, 92: 2.6, 93: 2.3, 94: 2.7, 95: 3.0, 96: 2.9, 97: 2.9, 98: 2.5, 99: 2.8, 100: 3.3, 101: 2.7, 102: 3.0, 103: 2.9, 104: 3.0, 105: 3.0, 106: 2.5, 107: 2.9, 108: 2.5, 109: 3.6, 110: 3.2, 111: 2.7, 112: 3.0, 113: 2.5, 114: 2.8, 115: 3.2, 116: 3.0, 117: 3.8, 118: 2.6, 119: 2.2, 120: 3.2, 121: 2.8, 122: 2.8, 123: 2.7, 124: 3.3, 125: 3.2, 126: 2.8, 127: 3.0, 128: 2.8, 129: 3.0, 130: 2.8, 131: 3.8, 132: 2.8, 133: 2.8, 134: 2.6, 135: 3.0, 136: 3.4, 137: 3.1, 138: 3.0, 139: 3.1, 140: 3.1, 141: 3.1, 142: 2.7, 143: 3.2, 144: 3.3, 145: 3.0, 146: 2.5, 147: 3.0, 148: 3.4, 149: 3.0}, 'petallength@REAL': {0: 1.4, 1: 1.4, 2: 1.3, 3: 1.5, 4: 1.4, 5: 1.7, 6: 1.4, 7: 1.5, 8: 1.4, 9: 1.5, 10: 1.5, 11: 1.6, 12: 1.4, 13: 1.1, 14: 1.2, 15: 1.5, 16: 1.3, 17: 1.4, 18: 1.7, 19: 1.5, 20: 1.7, 21: 1.5, 22: 1.0, 23: 1.7, 24: 1.9, 25: 1.6, 26: 1.6, 27: 1.5, 28: 1.4, 29: 1.6, 30: 1.6, 31: 1.5, 32: 1.5, 33: 1.4, 34: 1.5, 35: 1.2, 36: 1.3, 37: 1.5, 38: 1.3, 39: 1.5, 40: 1.3, 41: 1.3, 42: 1.3, 43: 1.6, 44: 1.9, 45: 1.4, 46: 1.6, 47: 1.4, 48: 1.5, 49: 1.4, 50: 4.7, 51: 4.5, 52: 4.9, 53: 4.0, 54: 4.6, 55: 4.5, 56: 4.7, 57: 3.3, 58: 4.6, 59: 3.9, 60: 3.5, 61: 4.2, 62: 4.0, 63: 4.7, 64: 3.6, 65: 4.4, 66: 4.5, 67: 4.1, 68: 4.5, 69: 3.9, 70: 4.8, 71: 4.0, 72: 4.9, 73: 4.7, 74: 4.3, 75: 4.4, 76: 4.8, 77: 5.0, 78: 4.5, 79: 3.5, 80: 3.8, 81: 3.7, 82: 3.9, 83: 5.1, 84: 4.5, 85: 4.5, 86: 4.7, 87: 4.4, 88: 4.1, 89: 4.0, 90: 4.4, 91: 4.6, 92: 4.0, 93: 3.3, 94: 4.2, 95: 4.2, 96: 4.2, 97: 4.3, 98: 3.0, 99: 4.1, 100: 6.0, 101: 5.1, 102: 5.9, 103: 5.6, 104: 5.8, 105: 6.6, 106: 4.5, 107: 6.3, 108: 5.8, 109: 6.1, 110: 5.1, 111: 5.3, 112: 5.5, 113: 5.0, 114: 5.1, 115: 5.3, 116: 5.5, 117: 6.7, 118: 6.9, 119: 5.0, 120: 5.7, 121: 4.9, 122: 6.7, 123: 4.9, 124: 5.7, 125: 6.0, 126: 4.8, 127: 4.9, 128: 5.6, 129: 5.8, 130: 6.1, 131: 6.4, 132: 5.6, 133: 5.1, 134: 5.6, 135: 6.1, 136: 5.6, 137: 5.5, 138: 4.8, 139: 5.4, 140: 5.6, 141: 5.1, 142: 5.1, 143: 5.9, 144: 5.7, 145: 5.2, 146: 5.0, 147: 5.2, 148: 5.4, 149: 5.1}, 'petalwidth@REAL': {0: 0.2, 1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.4, 6: 0.3, 7: 0.2, 8: 0.2, 9: 0.1, 10: 0.2, 11: 0.2, 12: 0.1, 13: 0.1, 14: 0.2, 15: 0.4, 16: 0.4, 17: 0.3, 18: 0.3, 19: 0.3, 20: 0.2, 21: 0.4, 22: 0.2, 23: 0.5, 24: 0.2, 25: 0.2, 26: 0.4, 27: 0.2, 28: 0.2, 29: 0.2, 30: 0.2, 31: 0.4, 32: 0.1, 33: 0.2, 34: 0.1, 35: 0.2, 36: 0.2, 37: 0.1, 38: 0.2, 39: 0.2, 40: 0.3, 41: 0.3, 42: 0.2, 43: 0.6, 44: 0.4, 45: 0.3, 46: 0.2, 47: 0.2, 48: 0.2, 49: 0.2, 50: 1.4, 51: 1.5, 52: 1.5, 53: 1.3, 54: 1.5, 55: 1.3, 56: 1.6, 57: 1.0, 58: 1.3, 59: 1.4, 60: 1.0, 61: 1.5, 62: 1.0, 63: 1.4, 64: 1.3, 65: 1.4, 66: 1.5, 67: 1.0, 68: 1.5, 69: 1.1, 70: 1.8, 71: 1.3, 72: 1.5, 73: 1.2, 74: 1.3, 75: 1.4, 76: 1.4, 77: 1.7, 78: 1.5, 79: 1.0, 80: 1.1, 81: 1.0, 82: 1.2, 83: 1.6, 84: 1.5, 85: 1.6, 86: 1.5, 87: 1.3, 88: 1.3, 89: 1.3, 90: 1.2, 91: 1.4, 92: 1.2, 93: 1.0, 94: 1.3, 95: 1.2, 96: 1.3, 97: 1.3, 98: 1.1, 99: 1.3, 100: 2.5, 101: 1.9, 102: 2.1, 103: 1.8, 104: 2.2, 105: 2.1, 106: 1.7, 107: 1.8, 108: 1.8, 109: 2.5, 110: 2.0, 111: 1.9, 112: 2.1, 113: 2.0, 114: 2.4, 115: 2.3, 116: 1.8, 117: 2.2, 118: 2.3, 119: 1.5, 120: 2.3, 121: 2.0, 122: 2.0, 123: 1.8, 124: 2.1, 125: 1.8, 126: 1.8, 127: 1.8, 128: 2.1, 129: 1.6, 130: 1.9, 131: 2.0, 132: 2.2, 133: 1.5, 134: 1.4, 135: 2.3, 136: 2.4, 137: 1.8, 138: 1.8, 139: 2.1, 140: 2.4, 141: 2.3, 142: 1.9, 143: 2.3, 144: 2.5, 145: 2.3, 146: 1.9, 147: 2.0, 148: 2.3, 149: 1.8}, 'class@{Iris-setosa,Iris-versicolor,Iris-virginica}': {0: 'Iris-setosa', 1: 'Iris-setosa', 2: 'Iris-setosa', 3: 'Iris-setosa', 4: 'Iris-setosa', 5: 'Iris-setosa', 6: 'Iris-setosa', 7: 'Iris-setosa', 8: 'Iris-setosa', 9: 'Iris-setosa', 10: 'Iris-setosa', 11: 'Iris-setosa', 12: 'Iris-setosa', 13: 'Iris-setosa', 14: 'Iris-setosa', 15: 'Iris-setosa', 16: 'Iris-setosa', 17: 'Iris-setosa', 18: 'Iris-setosa', 19: 'Iris-setosa', 20: 'Iris-setosa', 21: 'Iris-setosa', 22: 'Iris-setosa', 23: 'Iris-setosa', 24: 'Iris-setosa', 25: 'Iris-setosa', 26: 'Iris-setosa', 27: 'Iris-setosa', 28: 'Iris-setosa', 29: 'Iris-setosa', 30: 'Iris-setosa', 31: 'Iris-setosa', 32: 'Iris-setosa', 33: 'Iris-setosa', 34: 'Iris-setosa', 35: 'Iris-setosa', 36: 'Iris-setosa', 37: 'Iris-setosa', 38: 'Iris-setosa', 39: 'Iris-setosa', 40: 'Iris-setosa', 41: 'Iris-setosa', 42: 'Iris-setosa', 43: 'Iris-setosa', 44: 'Iris-setosa', 45: 'Iris-setosa', 46: 'Iris-setosa', 47: 'Iris-setosa', 48: 'Iris-setosa', 49: 'Iris-setosa', 50: 'Iris-versicolor', 51: 'Iris-versicolor', 52: 'Iris-versicolor', 53: 'Iris-versicolor', 54: 'Iris-versicolor', 55: 'Iris-versicolor', 56: 'Iris-versicolor', 57: 'Iris-versicolor', 58: 'Iris-versicolor', 59: 'Iris-versicolor', 60: 'Iris-versicolor', 61: 'Iris-versicolor', 62: 'Iris-versicolor', 63: 'Iris-versicolor', 64: 'Iris-versicolor', 65: 'Iris-versicolor', 66: 'Iris-versicolor', 67: 'Iris-versicolor', 68: 'Iris-versicolor', 69: 'Iris-versicolor', 70: 'Iris-versicolor', 71: 'Iris-versicolor', 72: 'Iris-versicolor', 73: 'Iris-versicolor', 74: 'Iris-versicolor', 75: 'Iris-versicolor', 76: 'Iris-versicolor', 77: 'Iris-versicolor', 78: 'Iris-versicolor', 79: 'Iris-versicolor', 80: 'Iris-versicolor', 81: 'Iris-versicolor', 82: 'Iris-versicolor', 83: 'Iris-versicolor', 84: 'Iris-versicolor', 85: 'Iris-versicolor', 86: 'Iris-versicolor', 87: 'Iris-versicolor', 88: 'Iris-versicolor', 89: 'Iris-versicolor', 90: 'Iris-versicolor', 91: 'Iris-versicolor', 92: 'Iris-versicolor', 93: 'Iris-versicolor', 94: 'Iris-versicolor', 95: 'Iris-versicolor', 96: 'Iris-versicolor', 97: 'Iris-versicolor', 98: 'Iris-versicolor', 99: 'Iris-versicolor', 100: 'Iris-virginica', 101: 'Iris-virginica', 102: 'Iris-virginica', 103: 'Iris-virginica', 104: 'Iris-virginica', 105: 'Iris-virginica', 106: 'Iris-virginica', 107: 'Iris-virginica', 108: 'Iris-virginica', 109: 'Iris-virginica', 110: 'Iris-virginica', 111: 'Iris-virginica', 112: 'Iris-virginica', 113: 'Iris-virginica', 114: 'Iris-virginica', 115: 'Iris-virginica', 116: 'Iris-virginica', 117: 'Iris-virginica', 118: 'Iris-virginica', 119: 'Iris-virginica', 120: 'Iris-virginica', 121: 'Iris-virginica', 122: 'Iris-virginica', 123: 'Iris-virginica', 124: 'Iris-virginica', 125: 'Iris-virginica', 126: 'Iris-virginica', 127: 'Iris-virginica', 128: 'Iris-virginica', 129: 'Iris-virginica', 130: 'Iris-virginica', 131: 'Iris-virginica', 132: 'Iris-virginica', 133: 'Iris-virginica', 134: 'Iris-virginica', 135: 'Iris-virginica', 136: 'Iris-virginica', 137: 'Iris-virginica', 138: 'Iris-virginica', 139: 'Iris-virginica', 140: 'Iris-virginica', 141: 'Iris-virginica', 142: 'Iris-virginica', 143: 'Iris-virginica', 144: 'Iris-virginica', 145: 'Iris-virginica', 146: 'Iris-virginica', 147: 'Iris-virginica', 148: 'Iris-virginica', 149: 'Iris-virginica'}}»",
        "id": "7V_bdb0596bdac3a55eaa5e738d23b88294dfaea",
        "ids": "7V_bdb0596bdac3a55eaa5e738d23b88294dfaea"
    }
    """
    return idict(file(name))


def file(name="iris.arff"):
    if name.endswith(".arff"):
        with open(name) as f:
            return {"df": a2p.load(f)}
    elif name.endswith(".csv"):
        return {"df": read_csv(name)}


# def save(name=None):
# DataFrame({
#     'power@NUMERIC':[0.5,0.2],
#     'label@{good,bad}':['good','bad']
# })
# with open('sample.arff','w') as f:
#     a2p.dump(df,f)
#
#
# import pandas as pd
# df = pd.DataFrame({
#     'power@NUMERIC':[0.5,0.2],
#     'label@{good,bad}':['good','bad']
# })
# print(a2p.dumps(df))

def df2np(df):
    """
    >>> from lazyds.learning.supervised.classification.rf import rf
    >>> from idict import let
    >>> d = File() >> df2np >> let(rf, n=1)
    >>> d.model
    RandomForestClassifier(n_estimators=1)
    """
    le = LabelEncoder()
    X = df.drop(df.columns[[-1]], axis=1)
    y = le.fit_transform(df[df.columns[-1]])
    # raise Exception({"X": X, "y": y})
    return {"X": X, "y": y}
