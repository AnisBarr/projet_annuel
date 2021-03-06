from PIL import Image
import numpy as np
import os
import random
import cv2
import copy
import math

# 164061
def resize_and_save(list_path,path_save, list_all,end_floder):
    data_set_train_x = np.empty((335170, 64, 64),dtype='float32')
    data_set_train_y = np.empty((335170, 1),dtype='float32')

    data_set_test_x = np.empty((111764, 64, 64),dtype='float32')
    data_set_test_y = np.empty((111764, 1),dtype='float32')
    

    global_count_train=0
    global_count_test=0

    for path in list_path:

        for lettre in list_all :

            path_tmp=None
            path_resize=None
            flip = False

            if path == "../resources/my_data_set/original/" or path == "../resources/my_data_set/" :
                path_tmp=path+lettre
                path_resize=path_tmp+end_floder
            else :
                flip = True
                path_tmp=path+lettre.upper()
                path_resize=path_tmp
            
            list_all_file_in_lettre = os.listdir(path_resize)

            nb_train = int((len(list_all_file_in_lettre)*75)/100)
            nb_test = len(list_all_file_in_lettre) - nb_train
            print(lettre+" train: "+str(nb_train)+" test "+str(nb_test)+" len :"+str(len(list_all_file_in_lettre))+" total : "+str(nb_test+nb_train))

            list_file_test = random.sample(list_all_file_in_lettre,nb_test)
            list_file_train = list(set(list_all_file_in_lettre) - set(list_file_test))
            
            print(len(list_file_test),len(list_file_train),len(list_all_file_in_lettre),len(list_file_test)+len(list_file_train))




            for file_train in list_file_train:
                # print(file_train)
                img = Image.open(os.path.join(path_resize, file_train))
                img = img.convert("L")
                img = img.resize((64, 64), Image.ANTIALIAS)
                

                data=np.asarray(img)

                data_set_train_x[global_count_train]=data
                data_set_train_y[global_count_train]=np.array([list_all.index(lettre)])

                if flip == True :
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    data=np.asarray(img)
                    data_set_train_x[global_count_train+1]=data
                    data_set_train_y[global_count_train+1]=np.array([list_all.index(lettre)])
                    global_count_train+=2
                else : 
                    global_count_train+=1

                print(data.shape)
                print(lettre+" train "+str(global_count_train)+"/total")


            for file_test in list_file_test:
                img = Image.open(os.path.join(path_resize, file_test))
                img = img.convert("L")
                img = img.resize((64, 64), Image.ANTIALIAS)

                # img.save("./test/"+file_test)
                
                data=np.asarray(img)

                data_set_test_x[global_count_test]=data
                data_set_test_y[global_count_test]=np.array([list_all.index(lettre)])

                if flip == True :
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    data=np.asarray(img)
                    data_set_test_x[global_count_test+1]=data
                    data_set_test_y[global_count_test+1]=np.array([list_all.index(lettre)])
                    global_count_test+=2
                else : 
                    global_count_test+=1

                            
                print(data.shape)
                print(lettre+" test "+str(global_count_test)+"/total")



        
           



    np.save(path_save+"/x_train_64_64_all_3", np.asarray(data_set_train_x/255, dtype= "float32"))
    np.save(path_save+"/y_train_64_64_all_3", np.asarray(data_set_train_y, dtype= "float32"))

    np.save(path_save+"/x_test_64_64_all_3", np.asarray(data_set_test_x/255, dtype= "float32"))
    np.save(path_save+"/y_test_64_64_all_3", np.asarray(data_set_test_y, dtype= "float32"))

    print(global_count_train,global_count_test)





if __name__ == "__main__":
    

    path = "../resources/my_data_set/"
    path_3 = "../resources/my_data_set/original/"
    path_2 = "../resources/train_set/"

    path_save = "../resources/np_array/"
    end_floder = "_normal_orig"
    end_floder_front = "_front"
    list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space","nothing"]
    list_all=[elt.lower() for elt in list_all]

    resize_and_save([path,path_3,path_2], path_save, list_all,end_floder)




