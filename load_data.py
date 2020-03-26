from PIL import Image
import numpy as np
import os
import random


def means_size():
    list_1 =[]
    list_2 =[]
    list_img=[]
    list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space"]
    path = "/media/anis/2ff7f8a4-2e97-4755-b85e-d2e332fd86cf/home/anis/stockage/data_projet_annuel/significant-asl-sign-language-alphabet-dataset/train_set/"
    path_resize = "/media/anis/2ff7f8a4-2e97-4755-b85e-d2e332fd86cf/home/anis/stockage/data_projet_annuel/significant-asl-sign-language-alphabet-dataset/train_set/A_resize"
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


def resize_and_save():
    data_set_train_x = np.empty((64379, 155, 124,3),dtype='float16')
    data_set_train_y = np.empty((64379, 1),dtype='float16')

    data_set_test_x = np.empty((16111, 155, 124,3),dtype='float16')
    data_set_test_y = np.empty((16111, 1),dtype='float16')
    

    list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space"]
    path = "/home/anis/hdd/stockage/data_projet_annuel/data_asl/train_set/"
    
    global_count_train=0
    global_count_test=0

    for lettre in list_all :

        path_tmp=path+lettre
        path_resize=path_tmp+"_resize"
        
        list_all_file_in_lettre = os.listdir(path_resize)

        nb_train = int((len(list_all_file_in_lettre)*80)/100)
        nb_test = len(list_all_file_in_lettre) - nb_train
        print(lettre+" train: "+str(nb_train)+" test "+str(nb_test)+" len :"+str(len(list_all_file_in_lettre))+" total : "+str(nb_test+nb_train))

        list_file_test = random.sample(list_all_file_in_lettre,nb_test)
        list_file_train = list(set(list_all_file_in_lettre) - set(list_file_test))
        
        print(len(list_file_test),len(list_file_train),len(list_all_file_in_lettre),len(list_file_test)+len(list_file_train))




        for file_train in list_file_train:
            img = Image.open(os.path.join(path_resize, file_train))
            img = img.convert("RGB")
            data=np.asarray(img)

            data_set_train_x[global_count_train]=data/255
            data_set_train_y[global_count_train]=np.array([list_all.index(lettre)])

            global_count_train+=1
            
            print(data.shape)
            print(lettre+" train "+str(global_count_train)+"/64379")


        for file_test in list_file_test:
            img = Image.open(os.path.join(path_resize, file_test))
            img = img.convert("RGB")
            data=np.asarray(img)

            data_set_test_x[global_count_test]=data/255
            data_set_test_y[global_count_test]=np.array([list_all.index(lettre)])

            global_count_test+=1
            
            print(data.shape)
            print(lettre+" test "+str(global_count_test)+"/16111")


    np.save(path+"/x_train_2", data_set_train_x)
    np.save(path+"/y_train_2", data_set_train_y)

    np.save(path+"/x_test_2", data_set_test_x)
    np.save(path+"/y_test_2", data_set_test_y)

    

resize_and_save()






































    # img = img.resize((136, 120), Image.ANTIALIAS)

    # img.save(os.path.join(path_resize, file))
    


    # for file in os.listdir(path):
    #     img = Image.open(os.path.join(path, file))

    # img = img.resize((136, 120), Image.ANTIALIAS)

    # img.save(os.path.join(path_resize, file))
    
    
# image = Image.open('/media/anis/2ff7f8a4-2e97-4755-b85e-d2e332fd86cf/home/anis/stockage/data_projet_annuel/significant-asl-sign-language-alphabet-dataset/train_set/A/_test.jpg')
# # convert image to numpy array
# data = asarray(image)
# print(data)
# # summarize shape
# print(data.shape)

# # create Pillow image
# image2 = Image.fromarray(data)
# print(type(image2))

# # summarize image details
# print(image2.mode)
# print(image2.size)
