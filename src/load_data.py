from PIL import Image
import numpy as np
import os
import random
import cv2
import copy
import math


def resize_and_save(path,path_save, list_all,end_floder):
    data_set_train_x = np.empty((128756, 64, 64),dtype='float32')
    data_set_train_y = np.empty((128756, 1),dtype='float32')

    data_set_test_x = np.empty((32220, 64, 64),dtype='float32')
    data_set_test_y = np.empty((32220, 1),dtype='float32')
    

    global_count_train=0
    global_count_test=0


    for lettre in list_all :

        path_tmp=path+lettre
        path_resize=path_tmp+end_floder
        
        list_all_file_in_lettre = os.listdir(path_resize)

        nb_train = int((len(list_all_file_in_lettre)*80)/100)
        nb_test = len(list_all_file_in_lettre) - nb_train
        print(lettre+" train: "+str(nb_train)+" test "+str(nb_test)+" len :"+str(len(list_all_file_in_lettre))+" total : "+str(nb_test+nb_train))

        list_file_test = random.sample(list_all_file_in_lettre,nb_test)
        list_file_train = list(set(list_all_file_in_lettre) - set(list_file_test))
        
        print(len(list_file_test),len(list_file_train),len(list_all_file_in_lettre),len(list_file_test)+len(list_file_train))




        for file_train in list_file_train:
            # print(file_train)
            img = Image.open(os.path.join(path_resize, file_train))
            # img = img.convert("RGB")
            img = img.resize((64, 64), Image.ANTIALIAS)
            
            data = np.asarray(img)
            data_augment = cv2.flip(data, 1)

            data_set_train_x[global_count_train] = data
            data_set_train_y[global_count_train] = np.array([list_all.index(lettre)])

            data_set_train_x[global_count_train+1] = data_augment
            data_set_train_y[global_count_train+1] = np.array([list_all.index(lettre)])

            global_count_train+=2
            
            print(data.shape)
            print(lettre+" train "+str(global_count_train)+"/128756")


        for file_test in list_file_test:
            img = Image.open(os.path.join(path_resize, file_test))
            # img = img.convert("RGB")
            img = img.resize((64, 64), Image.ANTIALIAS)

            data=np.asarray(img)
            data_augment = cv2.flip(data, 1)

            data_set_test_x[global_count_test] = data
            data_set_test_y[global_count_test] = np.array([list_all.index(lettre)])

            data_set_test_x[global_count_test+1] = data_augment
            data_set_test_y[global_count_test+1] = np.array([list_all.index(lettre)])

            global_count_test+=2
            
            print(data.shape)
            print(lettre+" test "+str(global_count_test)+"/32220")


    np.save(path_save+"/x_train_float_gray_aug", data_set_train_x)
    np.save(path_save+"/y_train_float_gray_aug", data_set_train_y)

    np.save(path_save+"/x_test_float_gray_aug", data_set_test_x)
    np.save(path_save+"/y_test_float_gray_aug", data_set_test_y)




def removeBG(frame,bgModel,learningRate,bgSubThreshold):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


def transformation(list_all,path,end_floder_front):
    bgSubThreshold = 100
    learningRate = 0
    

    for lettre in list_all :

        path_tmp=path+lettre
        list_all_file_in_lettre = os.listdir(path_tmp)
        path_save = path_tmp + end_floder_front

        os.mkdir(path_save)

        print(lettre)

        for file in list_all_file_in_lettre:
            img = cv2.imread(os.path.join(path_tmp, file))
            bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
            ret = removeBG(img,bgModel,learningRate,bgSubThreshold)
            cv2.imshow('t',ret)
            cv2.imwrite(os.path.join(path_save, file),ret)



if __name__ == "__main__":
    

    path = "../resources/train_set/"
    path_save = "../resources/np_array/"
    end_floder = "_gray"
    end_floder_front = "_front"
    list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space"]

    # transformation(list_all,path,end_floder_front)
    resize_and_save(path, path_save, list_all,end_floder)

    # bgSubThreshold = 100
    # learningRate = 0
    # bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
    # img = cv2.imread(os.path.join(path+"A", "A_P_hgr1_id01_2.jpg" ))
    
    # black = np.zeros((500,500,3))
    # removeBG(black,bgModel,learningRate,bgSubThreshold)
    # ret = removeBG(img,bgModel,learningRate,bgSubThreshold)
    

    # cv2.imwrite(os.path.join(path_save, file),img)











# this functions is used to get the mean of size in all the data sets

def means_size(path , list_all):
    list_1 =[]
    list_2 =[]
    list_img=[]
       
    for lettre in list_all :
        path_tmp=path+lettre
        for file in os.listdir(path_tmp):
            img = Image.open(os.path.join(path_tmp, file))
            list_img.append(np.asarray(img))
            list_1.append(img.size[0])
            list_2.append(img.size[1])
            print(file,img.size[0],img.size[1])

        np.mean(list_1),np.mean(list_2),len(list_1)

    return (np.mean(list_1),np.mean(list_2),len(list_1))

# (124.07182258665672, 155.63995527394707, 80490)