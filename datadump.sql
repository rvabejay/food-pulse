CREATE DATABASE IF NOT EXISTS foodsystem;

USE foodsystem;

CREATE USER IF NOT EXISTS 'rhys'@'localhost' IDENTIFIED BY '127rhys';
GRANT ALL PRIVILEGES ON foodsystem.* TO 'rhys'@'localhost' WITH GRANT OPTION;
GRANT CREATE USER ON *. * TO 'rhys'@'localhost';
FLUSH PRIVILEGES;


CREATE TABLE IF NOT EXISTS user
(
    username       VARCHAR(20) PRIMARY KEY NOT NULL,
    email_address  VARCHAR(50)             NOT NULL,
    first_name     VARCHAR(30)             NOT NULL,
    middle_initial VARCHAR(1),
    last_name      VARCHAR(30)             NOT NULL,
    password       VARCHAR(20)             NOT NULL,
    CONSTRAINT user_email_address UNIQUE (email_address)
);

CREATE TABLE IF NOT EXISTS admin
(
    username   VARCHAR(20),
    admin_code INT(5) AUTO_INCREMENT,
    CONSTRAINT admin_admin_code_uk UNIQUE (admin_code),
    CONSTRAINT admin_username_fk FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE IF NOT EXISTS food_establishment
(
    business_id    INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    business_name  VARCHAR(30)        NOT NULL,
    address        VARCHAR(50)        NOT NULL,
    website        VARCHAR(50),
    contact_number VARCHAR(11)
);

CREATE TABLE IF NOT EXISTS food_item
(
    food_id     INT(5) PRIMARY KEY                                                                          NOT NULL AUTO_INCREMENT,
    food_name   VARCHAR(50)                                                                                 NOT NULL,
    food_type   ENUM ('Meat', 'Vegetables', 'Appetizer', 'Pasta', 'Dessert', 'Beverage', 'Bread', 'Others') NOT NULL,
    price       DECIMAL(5, 2)                                                                               NOT NULL,
    description VARCHAR(200),
    business_id INT(5),
    CONSTRAINT food_item_business_id_fk FOREIGN KEY (business_id) REFERENCES food_establishment (business_id)
);

CREATE TABLE IF NOT EXISTS food_review
(
    review_id      INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    review_text    VARCHAR(200)       NOT NULL,
    rating         INT(1),
    date_of_review DATE               NOT NULL DEFAULT CURDATE(),
    username       VARCHAR(20),
    business_id    INT(5),
    food_id        INT(5),
    CONSTRAINT food_review_username_fk FOREIGN KEY (username) REFERENCES user (username),
    CONSTRAINT food_review_business_id_fk FOREIGN KEY (business_id) REFERENCES food_establishment (business_id),
    CONSTRAINT food_review_food_id_fk FOREIGN KEY (food_id) REFERENCES food_item (food_id)
);

INSERT INTO user (username, email_address, first_name, middle_initial, last_name, password)
VALUES ('prince', 'prince@email.com', 'Prince', 'S', 'Velasco', 'pass');

INSERT INTO user (username, email_address, first_name, middle_initial, last_name, password)
VALUES ('rhys', 'rhys@email.com', 'Rhys', 'A', 'Lomondot', '127rhys');

INSERT INTO user (username, email_address, first_name, middle_initial, last_name, password)
VALUES ('kevin', 'kevin@email.com', 'kevin', 'S', 'Cedillo', '1216');

INSERT INTO user (username, email_address, first_name, middle_initial, last_name, password)
VALUES ('josh', 'josh@email.com', 'josh', 'S', 'Atayde', '127f');

INSERT INTO user (username, email_address, first_name, middle_initial, last_name, password)
VALUES ('Seya', 'Seya@email.com', 'Seya', 'S', 'Concepcion', '129f');

INSERT INTO admin (username)
VALUES ('rhys');

INSERT INTO food_establishment (business_name, address, website, contact_number)
VALUES ('Burger Queen', 'Calamba, Laguna', 'burgerqueen.com.ph', '09123456789');

INSERT INTO food_establishment (business_name, address, website, contact_number)
VALUES ('Seoul Kitchen', 'Los Banos, Laguna', 'Skitechen.com.ph', '09557301065');

INSERT INTO food_establishment (business_name, address, website, contact_number)
VALUES ('Eatsumo', 'Los Banos, Laguna', 'Eatsumo.com.ph', '09557301765');

INSERT INTO food_establishment (business_name, address, website, contact_number)
VALUES ('Pizza Hut', 'Calamba, Laguna', 'pizzahut.com.ph', '09123456789');

INSERT INTO food_establishment (business_name, address, website, contact_number)
VALUES ('Mcdo', 'Calamba, Laguna', 'mcdo.com.ph', '09123458789');

INSERT INTO food_establishment (business_name, address, website, contact_number)
VALUES ('Spice Jar', 'Los Banos, Laguna', 'spice.com.ph', '09127456789');

INSERT INTO food_establishment (business_name, address, website, contact_number)
VALUES ('Dalcielo', 'Los Banos, Laguna', 'dalcielo.com.ph', '09127450789');

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Burger', 'Meat', 100.00, 'Juicy burger', 1);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Pizza', 'Bread', 200.00, 'Cheesy pizza', 2);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Spaghetti', 'Pasta', 150.00, 'Sweet spaghetti', 3);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Burger', 'Meat', 100.00, 'Juicy burger', 4);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Salad', 'Vegetables', 215.00, 'Fresh', 5);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Ice Cream', 'Dessert', 150.00, 'sweet', 6);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Kimbap', "Appetizer", 150, 'Fish cake, Pickled Radish, Egg, Ham, Carrots and Cucumber wrapped in a seaweed rice roll. (12 pieces)', 5);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Tuna Kimbap', "Appetizer", 170, 'Fish cake, Pickled Radish, Egg, Ham, Carrots, Cucumber, Tuna and Mayonnaise wrapped in a seaweed rice roll. (12 Pieces)', 1);

INSERT INTO food_item (food_name, food_type, price, description, business_id)
VALUES ('Ramyun', "Appetizer", 140, 'Packed Ramyun with egg.', 1);


INSERT INTO food_review (review_text, rating, username, business_id, food_id)
VALUES ('The best burger in town!', 5,  'rhys', 1, 1);

INSERT INTO food_review (review_text, rating, username, business_id, food_id)
VALUES ('The best pizza in town!', 5,  'rhys', 2, 2);

INSERT INTO food_review (review_text, rating,  username, business_id, food_id)
VALUES ('I thought it will be good, but its just okay', 5, 'rhys', 3, 3);

INSERT INTO food_review (review_text, rating,  username, business_id)
VALUES ('Its way more spicy than I expected, but its good!', 5,  'rhys', 2);

