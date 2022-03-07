-- Command to create the database
CREATE DATABASE `mydb_v2` IF NOT EXISTS;

-- Command to create the rows table
CREATE TABLE `rows`(
    editable BOOLEAN NOT NULL DEFAULT 0,
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    last_update VARCHAR(50),
    field VARCHAR(255),
    creator VARCHAR(255),
    preview VARCHAR(255),
    creator_avatar VARCHAR(500),
    dynamic_image BOOLEAN NOT NULL DEFAULT 0,
    creator_id INT NOT NULL,
    keywords VARCHAR(500),
    questions INT,
    uses INT,
    description VARCHAR (2000),

    PRIMARY KEY(id)
);

-- Command to create the columns table
CREATE TABLE `columns`(
    id VARCHAR(255),
    label VARCHAR(255),
    `default` BOOLEAN NOT NULL DEFAULT 0,
    minWidth INT,
    align VARCHAR(255),

    PRIMARY KEY(id)
);

-- Command to create the Users table
CREATE TABLE `users`(
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    description VARCHAR(5000),
    joined INT NOT NULL,
    avatar VARCHAR(500),
    chips VARCHAR(2000),
    favorites VARCHAR(500),
    recents VARCHAR(500),
    created VARCHAR(500),
    admin BOOLEAN NOT NULL DEFAULT 0,

    PRIMARY KEY(id)
);

CREATE TABLE `hash` (
    user VARCHAR(255) NOT NULL,
    hash VARCHAR(32) NOT NULL,

    PRIMARY KEY(user)
);

-- Command to create the Forms table
CREATE TABLE `forms`(
    formName VARCHAR(255) NOT NULL,
    creator VARCHAR(255) NOT NULL,
    content VARCHAR(21000) NOT NULL,
    formID INT NOT NULL AUTO_INCREMENT,

    PRIMARY KEY(FormID)
);

-- Command to create the Forms table
CREATE TABLE `templates`(
    template VARCHAR(21800),
    formID INT NOT NULL,

    PRIMARY KEY(FormID)
);


CREATE TABLE `images`(
    imageName VARCHAR(255) NOT NULL,
    begin VARCHAR(500),
    end VARCHAR(255),
    image VARCHAR(21000) NOT NULL,
    formID INT NOT NULL,

    PRIMARY KEY(FormID)
);