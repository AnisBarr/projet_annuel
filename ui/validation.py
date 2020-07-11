import cv2
import numpy as np
import copy
import math
import tensorflow as tf

list = ["A_test.jpg","D_test.jpg","G_test.jpg","J_test.jpg","M_test.jpg","O_test.jpg","R_test.jpg","T_test.jpg","W_test.jpg","Z_test.jpg","B_test.jpg","E_test.jpg","H_test.jpg","K_test.jpg","nothing_test.jpg","P_test.jpg","space_test.jpg","U_test.jpg","X_test.jpg","C_test.jpg","F_test.jpg","I_test.jpg","L_test.jpg","N_test.jpg","Q_test.jpg","S_test.jpg","V_test.jpg","Y_test.jpg"]
list = sorted(list)
print(list)

model = tf.keras.models.load_model("../logs/mo_model1_aug_True_act_relu_do_0.2_l2_0.0_op_adam_lr_0.001_mome_0.01_15-04-2020_02:20:30/my_model.h5")

for elt in list :
    img = cv2.imread("../resources/test_set/"+elt)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64,64))
    cv2.imshow('original_rezized', resized)
    
    reshaped = np.reshape(resized,(-1,64,64,1))
    data = np.asarray(reshaped, dtype = "float32")/255
    arry = model.predict(data)
    print(elt,np.argmax(arry))

import time
time.sleep(10)


A_test.jpg 24
B_test.jpg 1
C_test.jpg 2
D_test.jpg 3
E_test.jpg 4
F_test.jpg 5
G_test.jpg 6
H_test.jpg 7
I_test.jpg 8
J_test.jpg 9
K_test.jpg 10
L_test.jpg 11
M_test.jpg 12
N_test.jpg 13
O_test.jpg 14
P_test.jpg 15
Q_test.jpg 16
R_test.jpg 17
S_test.jpg 18
T_test.jpg 8
U_test.jpg 20
V_test.jpg 21
W_test.jpg 22
X_test.jpg 23
Y_test.jpg 24
Z_test.jpg 25
nothing_test.jpg 1
space_test.jpg 26