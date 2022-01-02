-- Command to create the database
CREATE DATABASE `mydb` IF NOT EXISTS;

-- Command to create the Users table
CREATE TABLE `users`(
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Admin BOOLEAN NOT NULL DEFAULT 0,

    PRIMARY KEY(Username)
);

CREATE TABLE `hash` (
    user VARCHAR(255) NOT NULL,
    hash VARCHAR(32) NOT NULL,

    PRIMARY KEY(user)
);

-- Command to create the Forms table
CREATE TABLE `forms`(
    FormName VARCHAR(255) NOT NULL,
    Creator VARCHAR(255) NOT NULL,
    Content VARCHAR(21000) NOT NULL,
    FormID INT NOT NULL AUTO_INCREMENT,

    PRIMARY KEY(FormID)
);

-- Command to create the Forms table
CREATE TABLE `templates`(
    Template VARCHAR(21800),
    FormID INT NOT NULL,

    PRIMARY KEY(FormID)
);


CREATE TABLE `images`(
    ImageName VARCHAR(255) NOT NULL,
    Image VARCHAR(21500) NOT NULL,
    FormID INT NOT NULL,

    PRIMARY KEY(FormID)
);