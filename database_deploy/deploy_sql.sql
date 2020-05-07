CREATE DATABASE IF NOT EXISTS projet_annuel ;

USE projet_annuel -A;

CREATE TABLE IF NOT EXISTS  user(
    id_user INT NOT NULL AUTO_INCREMENT,
    nom VARCHAR(100)  NOT NULL,
    prenom VARCHAR(100)  NOT NULL,
    email VARCHAR(255)  NOT NULL,
    password VARCHAR(100) NOT NULL,
    date_naissance DATE  NOT NULL,
    handicap BOOL  NOT NULL,
    PRIMARY KEY (id_user,email)
    );

CREATE TABLE IF NOT EXISTS  thoadmin(
    id_user INT NOT NULL AUTO_INCREMENT,
    nom VARCHAR(100)  NOT NULL,
    prenom VARCHAR(100)  NOT NULL,
    email VARCHAR(255)  NOT NULL,
    password VARCHAR(100) NOT NULL,
    date_naissance DATE  NOT NULL,
    PRIMARY KEY (id_user,email)
    );


INSERT INTO user (nom,prenom,email,password,date_naissance,handicap)  VALUES ('TEST','TEST','TEST@gmail.com','TEST','2020-02-02',1);
