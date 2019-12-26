DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS customer_service_asisstant;
DROP TABLE IF EXISTS technician;

CREATE TABLE user(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR(50) UNIQUE NOT NULL,
email VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(50) NOT NULL,
first_name VARCHAR(50) NOT NULL,
middle_name VARCHAR(50),
last_name VARCHAR(50) NOT NULL,
phone INTEGER NOT NULL,
gender VARCHAR(6)
);

CREATE TABLE customer(
id INTEGER PRIMARY KEY,
national_id VARCHAR(15) NOT NULL,
city VARCHAR(20),
street VARCHAR(50),
apt_no VARCHAR(50),
district VARCHAR(50),
zip_code INTEGER,
birth_date DATE,
FOREIGN KEY (id) REFERENCES user(id)
);

CREATE TABLE employee (
id INTEGER PRIMARY KEY,
requirement_year INTEGER NOT NULL,
department VARCHAR(50) NOT NULL,
years_of_experience INTEGER,
FOREIGN KEY (id) REFERENCES user(id) on delete cascade on update cascade
);

CREATE TABLE customer_service_asisstant (
id INTEGER PRIMARY KEY,
FOREIGN KEY (id) REFERENCES employee(id) on delete cascade on update cascade
);

CREATE TABLE technician(
id INTEGER PRIMARY KEY,
profession VARCHAR(50),
FOREIGN KEY (id) REFERENCES employee(id) on delete cascade on update cascade
);




