from PIL import Image
import numpy as np
import os
import random
import cv2
import copy
import math

# 164061
def resize_and_save(list_path,path_save, list_all,end_floder):
    data_set_train_x = np.empty((244520, 64, 64,3),dtype='float32')
    data_set_train_y = np.empty((244520, 1),dtype='float32')

    data_set_test_x = np.empty((81538, 64, 64,3),dtype='float32')
    data_set_test_y = np.empty((81538, 1),dtype='float32')
    

    global_count_train=0
    global_count_test=0

    for path in list_path:

        for lettre in list_all :

            path_tmp=None
            path_resize=None
            flip = False

            if path == "../resources/my_data_set/original/" :
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

            path_save


            for file_train in list_file_train:
                # print(file_train)
                img = Image.open(os.path.join(path_resize, file_train))
                img = img.convert("RGB")
                img.save(path_save+"/train/"+lettre+"/"+file_train)
                

                if flip == True :
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    img.save(path_save+"/train/"+lettre+"/filp_"+file_train)
     
                

              
                print(lettre+" train "+str(global_count_train)+"/total")




            for file_test in list_file_test:
                img = Image.open(os.path.join(path_resize, file_test))
                img = img.convert("RGB")
                img.save(path_save+"/test/"+lettre+"/"+file_test)
                
                

               

                if flip == True :
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    img.save(path_save+"/test/"+lettre+"/filp_"+file_test)
                    
                    
                    
              

                            
                
                print(lettre+" test "+str(global_count_test)+"/total")



        
        
        









if __name__ == "__main__":
    

    path = "../resources/my_data_set/original/"
    path_2 = "../resources/train_set/"

    path_save = "../resources/data"
    end_floder = "_normal_orig"
    end_floder_front = "_front"
    list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space","nothing"]
    list_all=[elt.lower() for elt in list_all]

    resize_and_save([path_2,path], path_save, list_all,end_floder)
