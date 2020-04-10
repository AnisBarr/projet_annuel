import numpy as np
path = "../resources/np_array/"
list = ["x_train_float_gray_aug.npy","y_train_float_gray_aug.npy","x_test_float_gray_aug.npy","y_test_float_gray_aug.npy"]

for elt in list :
    print (elt)
    tmp = np.load(path+elt)
    print(tmp.shape)
    for el in tmp :
        print(el)
        print(el.shape)
    

