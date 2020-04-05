import numpy as np
path = "/home/anis/hdd/stockage/data_projet_annuel/data_asl/train_set/"
list = ["x_train_2.npy","y_train_2.npy","x_test_2.npy","y_test_2.npy"]

for elt in list :
    print (elt)
    tmp = np.load(path+elt)
    print(tmp.shape)

    print(tmp[tmp.shape[0]-1])

