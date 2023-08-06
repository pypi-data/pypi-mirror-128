import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


def createConfusionMatrix(test,predition):
    """[summary]

    Args:
        test ([type]): [description]
        predition ([type]): [description]
    """
    cm = confusion_matrix(test, predition)
    plt.figure()
    sns.heatmap(cm/np.sum(cm),annot=True,fmt='.2%',cmap="Reds")