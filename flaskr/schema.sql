DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS customer_service_asisstant;
DROP TABLE IF EXISTS technician;
DROP TABLE IF EXISTS repairment;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS parts;
DROP TABLE IF EXISTS parts_repairment;
DROP TABLE IF EXISTS shipping;
DROP TABLE IF EXISTS complaint;


CREATE TABLE user(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR(50) UNIQUE NOT NULL,
email VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(50) NOT NULL,
first_name VARCHAR(50) NOT NULL,
middle_name VARCHAR(50),
last_name VARCHAR(50) NOT NULL,
phone INTEGER NOT NULL,
gender VARCHAR(6),
user_type VARCHAR(50) NOT NULL,
CHECK( gender IN ( "male", "female")),
CHECK( user_type IN ( "customer", "asisstant", "technician"))
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

CREATE TABLE repairment (
id INTEGER PRIMARY KEY AUTOINCREMENT,
technician_id INTEGER NOT NULL, 
product_id INTEGER NOT NULL,
customer_id INTEGER NOT NULL,
problem VARCHAR(150) NOT NULL,
demand VARCHAR(150) NOT NULL,
status VARCHAR(150),
decision VARCHAR(150),
satisfaction VARCHAR(150),
CHECK( demand IN ( "return", "repair", "renew")),
CHECK( status IN ( "ongoing", "shipped", "closed", "complained")),
CHECK( decision IN ( "yes", "no")),
FOREIGN KEY (technician_id) REFERENCES technician(id) on delete cascade on update cascade,
FOREIGN KEY (product_id)  REFERENCES  product(id) on delete cascade on update cascade,
FOREIGN KEY (customer_id)  REFERENCES  customer(id) on delete cascade on update cascade
);

CREATE TABLE product (
id INTEGER PRIMARY KEY AUTOINCREMENT,
model VARCHAR(50) NOT NULL,
color VARCHAR(14),
years_of_warranty INTEGER NOT NULL, 
time_of_buying DATE NOT NULL,
price FLOAT NOT NULL,
cat_id INTEGER NOT NULL,
FOREIGN KEY (cat_id) REFERENCES category(id) on delete cascade on update cascade
);

CREATE TABLE category (
id INTEGER PRIMARY KEY AUTOINCREMENT,
cat_name VARCHAR(50) NOT NULL
);

CREATE TABLE messages ( 
id INTEGER PRIMARY KEY AUTOINCREMENT,
date DATE NOT NULL,
text VARCHAR(1000) NOT NULL,
complaint_id INTEGER NOT NULL,
receiver_id INTEGER NOT NULL,
sender_id INTEGER NOT NULL,
FOREIGN KEY (receiver_id) REFERENCES  user(id) on delete cascade on update cascade,
FOREIGN KEY (sender_id) REFERENCES user(id) on delete cascade on update cascade,
FOREIGN KEY (complaint_id) REFERENCES complaint(id) on delete cascade on update cascade
);

CREATE TABLE parts (
id INTEGER,
product_id INTEGER NOT NULL,
name VARCHAR(50) NOT NULL,
PRIMARY KEY (id, product_id),
FOREIGN KEY (product_id) REFERENCES product(id) on delete cascade on update cascade
);

CREATE TABLE parts_repairment(
repairment_id INTEGER NOT NULL,
part_id INTEGER NOT NULL,
product_id INTEGER NOT NULL,
status VARCHAR(50) NOT NULL,
PRIMARY KEY (repairment_id, part_id),
FOREIGN KEY  (repairment_id)  REFERENCES  repairment(id) on delete cascade on update cascade,
FOREIGN KEY  (part_id)  REFERENCES  parts(id) on delete cascade on update cascade,
CHECK (status in ("changed", "notChanged", "fixed"))
);


CREATE TABLE shipping(
id INTEGER PRIMARY KEY AUTOINCREMENT,
delivery_date DATE NOT NULL,
receive_date DATE,
repairment_id INTEGER NOT NULL,
customer_id INTEGER NOT NULL,
technician_id INTEGER NOT NULL,
status VARCHAR(50) NOT NULL,
FOREIGN KEY (repairment_id) REFERENCES repairment(id) on delete cascade on update cascade,
FOREIGN KEY (customer_id) REFERENCES customer(id) on delete cascade on update cascade, 
FOREIGN KEY (technician_id) REFERENCES technician(id) on delete cascade on update cascade, 
CHECK (status IN( "shipped", "delivered", "onWay"))
);

CREATE TABLE complaint (
id INTEGER PRIMARY KEY AUTOINCREMENT,
problem VARCHAR(150) NOT NULL,
current_status  VARCHAR(50) NOT NULL,
final_status VARCHAR(50),
repairment_id INTEGER NOT NULL,
customer_service_asisstant_id INTEGER NOT NULL,
customer_id INTEGER NOT NULL,
FOREIGN KEY (repairment_id) REFERENCES repairment(id) on delete cascade on update cascade,
FOREIGN KEY (customer_service_asisstant_id) REFERENCES customer_service_assistant(id) on delete cascade on update cascade,
FOREIGN KEY (customer_id) REFERENCES customer(id) on delete cascade on update cascade,
CHECK (current_status IN ("ongoing", "finished", "onOthers", "waiting")),
CHECK (final_status IN ("positive", "negative"))
);





