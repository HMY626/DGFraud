import numpy as np
from sklearn.model_selection import train_test_split
import scipy.io as sio
import scipy.sparse as sp


# symmetrically normalize adjacency matrix
def normalize_adj(adj):
    adj = adj + sp.eye(adj.shape[0])
    adj = sp.coo_matrix(adj)
    rowsum = np.array(adj.sum(1))
    d_inv_sqrt = np.power(rowsum, -0.5).flatten()
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.
    d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
    return adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt).A


def read_data_dzdp():
    index = list(range(9067))
    y = np.loadtxt('data/label.txt')
    X_train, X_test, y_train, y_test = train_test_split(index, y, stratify=y, test_size=0.4,
                                                        random_state=48, shuffle=True)

    return X_train, y_train, X_test, y_test


def load_data_dblp(path='data/DBLP4057_GAT_with_idx_tra200_val_800.mat'):
    data = sio.loadmat(path)
    truelabels, features = data['label'], data['features'].astype(float)
    N = features.shape[0]
    rownetworks = [data['net_APA'] - np.eye(N), data['net_APCPA'] - np.eye(N), data['net_APTPA'] - np.eye(N)]
    y = truelabels
    index = range(len(y))
    X_train, X_test, y_train, y_test = train_test_split(index, y, stratify=y, test_size=0.4, random_state=48,
                                                        shuffle=True)

    return rownetworks, features, X_train, y_train, X_test, y_test
