import numpy as np
path = "../resources/np_array/"
list = ["x_train_my.npy","y_train_my.npy","x_test_my.npy","y_test_my.npy"]

for elt in list :
    print (elt)
    tmp = np.load(path+elt)
    print(tmp.shape)
    for el in tmp :
        print(el)
        print(el.shape)
    

