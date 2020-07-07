import mysql.connector
from mysql.connector import Error
import configparser
import logging
from logging.handlers import RotatingFileHandler
import time

def init() :

    config = configparser.ConfigParser()
    config.read('../config/config.ini')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-[%(message)s]')
    file_handler = RotatingFileHandler(config['GLOBAL_LOG_MONITORING']['log'] , 'a', 1000000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return config,logger



def create_connection(host_name, user_name, user_password,config,logger):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        logger.info("conection to mysql server ... OK")
    except Error as e:
        logger.error("conection to mysql server ... KO ")
        logger.error(f"The error '{e}' occurred")

    return connection




def init_connection(config,logger):
    
    connection = create_connection(config['SQL_LOGIN']['machine'], config['SQL_LOGIN']['user'], config['SQL_LOGIN']['password'],config,logger)
    cursor = connection.cursor()
    try:
        query="use "+config['DATABABES']['projet_annuel']
        cursor.execute(query)
        logger.info("init_connection ... OK")
    except Error as e:
        logger.error("init_connection ... KO ")
        logger.error(f"The error '{e}' occurred")
        connection = None

    return connection


def add_user(nom,prenom,email,password,date_naissance,handicap):
    config,logger = init()
    connection = init_connection(config,logger)
    cursor = connection.cursor()
    result = True

    try:
        query="use "+config['DATABABES']['projet_annuel']
        cursor.execute(query)

        query="INSERT INTO "+ config['TABLES']['user'] +" (nom,prenom,email,password,date_naissance,handicap) VALUES ('" + nom + "','" + prenom + "','" + email + "','" + password + "','" + date_naissance + "'," + handicap+");"
        cursor.execute(query)
        logger.info("add_user ... OK")

        
    except Error as e:
        logger.error("add_user ... KO ")
        logger.error(f"The error '{e}' occurred")
        result = False

    connection.commit()

    return result



def add_admin(nom,prenom,email,password,date_naissance):
    config,logger = init()
    connection = init_connection(config,logger)
    cursor = connection.cursor()
    result = True

    try:
        # query="use "+config['DATABABES']['projet_annuel']
        # cursor.execute(query)

        query="INSERT INTO "+ config['DATABABES']['projet_annuel'] +"."+config['TABLES']['admin'] +" (nom,prenom,email,password,date_naissance) VALUES ('" + nom + "','" + prenom + "','" + email + "','" + password + "','" + date_naissance + "' );"
        cursor.execute(query)
        logger.info("add_admin ... OK")
        
    except Error as e:
        logger.error("add_admin ... KO ")
        logger.error(f"The error '{e}' occurred")
        result = False

    connection.commit()
    
    return result

def get_user(email):
    config,logger = init()
    connection = init_connection(config,logger)
    cursor = connection.cursor()
    result = True

    try:
        query="use "+config['DATABABES']['projet_annuel']
        cursor.execute(query)

        query="SELECT email,password,nom,prenom from  "+ config['TABLES']['user'] +" WHERE email='" + email + "' ;"
        cursor.execute(query)
        result = cursor
        try : 
            for (email,password,nom,prenom) in cursor :
                result=(email,password,nom,prenom)
        except :
            result = False
        logger.info("get_user ... OK")

        
    except Error as e:

        logger.error("get_user ... KO ")
        logger.error(f"The error '{e}' occurred")
        result = False


    return result



def add_entry(email,input):
    config,logger = init()
    connection = init_connection(config,logger)
    cursor = connection.cursor()
    result = True
    in_out = None

    try:
        if input == False : 
            in_out = "0"
        else :
            in_out = "1"

        query="INSERT INTO "+ config['DATABABES']['projet_annuel'] +"."+config['TABLES']['history'] +" (email,type_in_out,time) VALUES ('" + email + "','" + in_out + "','" + str(int(time.time())) + "' );"
        cursor.execute(query)
        logger.info("add_entry ... OK")
        
    except Error as e:
        logger.error("add_entry ... KO ")
        logger.error(f"The error '{e}' occurred")
        result = False

    connection.commit()
    
    return result

def update_password (email,old_password, new_password):

    config,logger = init()
    connection = init_connection(config,logger)
    cursor = connection.cursor()
    result = True

    try:
        query="use "+config['DATABABES']['projet_annuel']
        cursor.execute(query)

        query="UPDATE table  "+ config['TABLES']['user'] + "SET password ='"+ new_password +"' WHERE email='" + email + "' AND password='"+ old_password  +"' ;"
        cursor.execute(query)

        logger.info("get_uupdate_passwordser ... OK")

        
    except Error as e:

        logger.error("update_password ... KO ")
        logger.error(f"The error '{e}' occurred")
        result = False


    return result


if __name__ == "__main__" :
    
    add_user("nom","prenom","email","password","2020-02-01","1")
    add_admin("nom","prenom","email","password","2020-02-01")
    add_entry("email",False)


# INSERT INTO user (nom,prenom,email,password,date_naissance,handicap) VALUES ('fdsq','fdsq','fdsq','fdsq','gfsd',1);