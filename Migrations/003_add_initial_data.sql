INSERT INTO `sex` (`id`, `type`) VALUES (NULL, 'Male'), 
(NULL, 'Female'), 
(NULL, 'Others'), 
(NULL, 'Prefer not to say!');

INSERT INTO `type` (name) values ('Food'), ('Household Expences'),
 ('Personal'), ('Bills'), ('Travel'), ('Education'), ('Income');



INSERT INTO `sub_type` (name) values ('Breakfasts'), ('Lunch'),
 ('Dinner'), ('Supper'), ('Tiffin'), ('Extra Tiffin'), ('Snacks'), ('Others'), ('Grocery'), 
('Medicine'), ('Clothing'), ('Domestic Products'), ('Mobile Recharge'), ('Electricity'),
 ('Water'), ('WiFi'), ('Office'), ('Market'), ('Trip Weekly'), ('Trip Monthly'), ('School'),
 ('Books'), ('Miscellaneous'), ('Salary'), ('Investments'), ('Startup'), ('Business');

INSERT INTO `type_subtype` 
( type_id, subtype_id ) value ('1', '1'),('1', '2'),('1', '3'),('1', '4'),
('1', '5'),('1', '6'),('1', '7'),('1', '8'),('2', '9'),('2', '10'),('2', '11'),
('2', '12'),('2', '8'),('3', '8'),('4', '13'),('4', '14'),('4', '15'),('4', '16'),
('4', '8'),('5', '17'),('5', '18'),('5', '19'),('5', '20'),('5', '8'),('6', '21'),
('6', '22'),('6', '23'),('6', '8'),('7', '24'),('7', '25'),('7', '26'),('7', '27'),('7', '8');

INSERT INTO `frequency`
( name ) value ('Once'), ('Daily'), ('Weekly'), ('Bi-Weekly'), ('Monthly'), ('By-Monthly'),
 ('Quarter-Yearly'),  ('Semi-Yearly'), ('Yearly'), ('Randomly');

INSERT INTO `payment_medium`
( name ) value ('Cash'), ('UPI'), ('Paytm'), ('Bank Transfer'), ('Card'), ('Cheque'),
 ('Other E-Wallet');
