CREATE TABLE sex (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE frequency (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE payment_medium (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE sub_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE type_subtype (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_id INT NOT NULL,
    subtype_id INT NOT NULL,
    FOREIGN KEY (type_id) REFERENCES type(id),
    FOREIGN KEY (subtype_id) REFERENCES sub_type(id)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(15) NOT NULL,
    mname VARCHAR(15),
    lname VARCHAR(15),
    picture VARCHAR(100),
    dob DATE,
    email VARCHAR(50) NOT NULL UNIQUE,
    email_conformation INT NOT NULL DEFAULT 0,
    phone VARCHAR(15),
    password VARCHAR(60) NOT NULL,
    sex_id INT NOT NULL,
    active INT DEFAULT 1,
    FOREIGN KEY (sex_id) REFERENCES sex(id)
);

CREATE TABLE expences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(15) NOT NULL,
    date_time DATETIME NOT NULL,
    type_subtype_id INT NOT NULL,
    frequency_id INT NOT NULL,
    payment_id INT NOT NULL,
    debit FLOAT,
    credit FLOAT,
    user_id INT NOT NULL,
    comments VARCHAR(100),
    FOREIGN KEY (type_subtype_id) REFERENCES type_subtype(id),
    FOREIGN KEY (frequency_id) REFERENCES frequency(id),
    FOREIGN KEY (payment_id) REFERENCES payment_medium(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(15) NOT NULL,
    mname VARCHAR(15),
    lname VARCHAR(15),
    picture VARCHAR(100),
    dob DATE,
    email VARCHAR(60) NOT NULL UNIQUE,
    email_conformation INT NOT NULL DEFAULT 0,
    phone VARCHAR(15),
    password VARCHAR(60) NOT NULL,
    sex_id INT NOT NULL,
    active INT DEFAULT 1,
    FOREIGN KEY (sex_id) REFERENCES sex(id)
);
