--
-- Create model Address
--
CREATE TABLE `Address` (`add_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `address` varchar(255) NOT NULL, `zipcode` varchar(255) NOT NULL);
--
-- Create model Authenticate
--
CREATE TABLE `Authenticate` (`p_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `username` varchar(100) NOT NULL UNIQUE, `password` varchar(15) NOT NULL, `user_type` varchar(30) NOT NULL);
--
-- Create model Category
--
CREATE TABLE `Category` (`Category_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `Name` varchar(255) NOT NULL);
--
-- Create model Customer
--
CREATE TABLE `Customer` (`customer_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `f_name` varchar(255) NOT NULL, `l_name` varchar(255) NOT NULL, `email` varchar(255) NOT NULL, `p_id_id` integer NOT NULL);
--
-- Create model Delivery
--
CREATE TABLE `Delivery` (`delivery_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `timeDispatch` datetime(6) NULL, `timeArrival` datetime(6) NULL);
--
-- Create model deliveryPersonnel
--
CREATE TABLE `deliveryPersonnel` (`personnel_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NOT NULL, `phone` varchar(255) NOT NULL, `availability` varchar(255) NOT NULL, `p_id_id` integer NOT NULL);
--
-- Create model Manager
--
CREATE TABLE `Manager` (`manager_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `Name` varchar(255) NOT NULL, `email` varchar(255) NOT NULL, `p_id_id` integer NOT NULL);
--
-- Create model payInfo
--
CREATE TABLE `payInfo` (`infoId` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `payMode` varchar(100) NOT NULL, `payDescr` varchar(100) NOT NULL, `custId_id` integer NOT NULL);
--
-- Create model Product
--
CREATE TABLE `Product` (`product_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `item_name` varchar(255) NOT NULL, `price` integer NOT NULL, `description` varchar(255) NOT NULL);
--
-- Create model Restaurant
--
CREATE TABLE `Restaurant` (`restaurant_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `restaurant_name` varchar(255) NOT NULL, `addr_id_id` integer NOT NULL, `man_id_id` integer NOT NULL);
--
-- Create model Status
--
CREATE TABLE `Status` (`status_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `status_val` varchar(255) NOT NULL);
--
-- Create model Review
--
CREATE TABLE `Review` (`review_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `stars` integer NOT NULL, `del_rev` varchar(255) NOT NULL, `food_rev` varchar(255) NOT NULL, `customer_id_id` integer NOT NULL, `delivery_id_id` integer NOT NULL);
--
-- Create model restPhNos
--
CREATE TABLE `restPhNos` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `ph_no` varchar(255) NOT NULL, `restaurant_id_id` integer NOT NULL);
--
-- Create model Product_categ
--
CREATE TABLE `food_delivery_app_product_categ` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `cat_id_id` integer NOT NULL, `prod_id_id` integer NOT NULL);
--
-- Add field res_id to product
--
ALTER TABLE `Product` ADD COLUMN `res_id_id` integer NOT NULL , ADD CONSTRAINT `Product_res_id_id_c7434401_fk_Restaurant_restaurant_id` FOREIGN KEY (`res_id_id`) REFERENCES `Restaurant`(`restaurant_id`);
--
-- Create model personnelAddr
--
CREATE TABLE `personnelAddr` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `add_id_id` integer NOT NULL, `personnel_id_id` integer NOT NULL);
--
-- Create model Payment
--
CREATE TABLE `Payment` (`payId` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `payDate` datetime(6) NOT NULL, `infoId_id` integer NOT NULL);
--
-- Create model Orders
--
CREATE TABLE `Orders` (`order_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `total_price` integer NOT NULL, `ordered_on` datetime(6) NOT NULL, `customer_id_id` integer NOT NULL, `restaurant_id_id` integer NOT NULL);
--
-- Create model orderProducts
--
CREATE TABLE `orderProducts` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `quantity` integer NOT NULL, `item_id_id` integer NOT NULL, `order_id_id` integer NOT NULL);
--
-- Create model ManNos
--
CREATE TABLE `ManNos` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `ph_no` varchar(255) NOT NULL, `man_id_id` integer NOT NULL);
--
-- Add field orderId to delivery
--
ALTER TABLE `Delivery` ADD COLUMN `orderId_id` integer NOT NULL , ADD CONSTRAINT `Delivery_orderId_id_b0216b1c_fk_Orders_order_id` FOREIGN KEY (`orderId_id`) REFERENCES `Orders`(`order_id`);
--
-- Add field personnelId to delivery
--
ALTER TABLE `Delivery` ADD COLUMN `personnelId_id` integer NOT NULL , ADD CONSTRAINT `Delivery_personnelId_id_c5d17a4d_fk_deliveryP` FOREIGN KEY (`personnelId_id`) REFERENCES `deliveryPersonnel`(`personnel_id`);
--
-- Add field statusId to delivery
--
ALTER TABLE `Delivery` ADD COLUMN `statusId_id` integer NOT NULL , ADD CONSTRAINT `Delivery_statusId_id_b642461d_fk_Status_status_id` FOREIGN KEY (`statusId_id`) REFERENCES `Status`(`status_id`);
--
-- Create model CustNos
--
CREATE TABLE `CustNos` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `ph_no` varchar(255) NOT NULL, `customer_id_id` integer NOT NULL);
--
-- Create model CustAddress
--
CREATE TABLE `CustAddress` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `add_id_id` integer NOT NULL, `customer_id_id` integer NOT NULL);
ALTER TABLE `Customer` ADD CONSTRAINT `Customer_p_id_id_197eb410_fk_Authenticate_p_id` FOREIGN KEY (`p_id_id`) REFERENCES `Authenticate` (`p_id`);
ALTER TABLE `deliveryPersonnel` ADD CONSTRAINT `deliveryPersonnel_p_id_id_5f6d95bb_fk_Authenticate_p_id` FOREIGN KEY (`p_id_id`) REFERENCES `Authenticate` (`p_id`);
ALTER TABLE `Manager` ADD CONSTRAINT `Manager_p_id_id_031d5984_fk_Authenticate_p_id` FOREIGN KEY (`p_id_id`) REFERENCES `Authenticate` (`p_id`);
ALTER TABLE `payInfo` ADD CONSTRAINT `payInfo_custId_id_307622db_fk_Customer_customer_id` FOREIGN KEY (`custId_id`) REFERENCES `Customer` (`customer_id`);
ALTER TABLE `Restaurant` ADD CONSTRAINT `Restaurant_addr_id_id_c25ff85a_fk_Address_add_id` FOREIGN KEY (`addr_id_id`) REFERENCES `Address` (`add_id`);
ALTER TABLE `Restaurant` ADD CONSTRAINT `Restaurant_man_id_id_d979bcdd_fk_Manager_manager_id` FOREIGN KEY (`man_id_id`) REFERENCES `Manager` (`manager_id`);
ALTER TABLE `Review` ADD CONSTRAINT `Review_customer_id_id_c5286eb9_fk_Customer_customer_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Customer` (`customer_id`);
ALTER TABLE `Review` ADD CONSTRAINT `Review_delivery_id_id_fa8bf6b0_fk_Delivery_delivery_id` FOREIGN KEY (`delivery_id_id`) REFERENCES `Delivery` (`delivery_id`);
ALTER TABLE `restPhNos` ADD CONSTRAINT `restPhNos_restaurant_id_id_0784580b_fk_Restaurant_restaurant_id` FOREIGN KEY (`restaurant_id_id`) REFERENCES `Restaurant` (`restaurant_id`);
ALTER TABLE `food_delivery_app_product_categ` ADD CONSTRAINT `food_delivery_app_pr_cat_id_id_e346900b_fk_Category_` FOREIGN KEY (`cat_id_id`) REFERENCES `Category` (`Category_id`);
ALTER TABLE `food_delivery_app_product_categ` ADD CONSTRAINT `food_delivery_app_pr_prod_id_id_34df74ec_fk_Product_p` FOREIGN KEY (`prod_id_id`) REFERENCES `Product` (`product_id`);
ALTER TABLE `personnelAddr` ADD CONSTRAINT `personnelAddr_add_id_id_9562bc51_fk_Address_add_id` FOREIGN KEY (`add_id_id`) REFERENCES `Address` (`add_id`);
ALTER TABLE `personnelAddr` ADD CONSTRAINT `personnelAddr_personnel_id_id_8deda189_fk_deliveryP` FOREIGN KEY (`personnel_id_id`) REFERENCES `deliveryPersonnel` (`personnel_id`);
ALTER TABLE `Payment` ADD CONSTRAINT `Payment_infoId_id_092f86c0_fk_payInfo_infoId` FOREIGN KEY (`infoId_id`) REFERENCES `payInfo` (`infoId`);
ALTER TABLE `Orders` ADD CONSTRAINT `Orders_customer_id_id_8264ecb5_fk_Customer_customer_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Customer` (`customer_id`);
ALTER TABLE `Orders` ADD CONSTRAINT `Orders_restaurant_id_id_f487c164_fk_Restaurant_restaurant_id` FOREIGN KEY (`restaurant_id_id`) REFERENCES `Restaurant` (`restaurant_id`);
ALTER TABLE `orderProducts` ADD CONSTRAINT `orderProducts_item_id_id_93c57e4d_fk_Product_product_id` FOREIGN KEY (`item_id_id`) REFERENCES `Product` (`product_id`);
ALTER TABLE `orderProducts` ADD CONSTRAINT `orderProducts_order_id_id_18f33fb3_fk_Orders_order_id` FOREIGN KEY (`order_id_id`) REFERENCES `Orders` (`order_id`);
ALTER TABLE `ManNos` ADD CONSTRAINT `ManNos_man_id_id_00df6d8b_fk_Manager_manager_id` FOREIGN KEY (`man_id_id`) REFERENCES `Manager` (`manager_id`);
ALTER TABLE `CustNos` ADD CONSTRAINT `CustNos_customer_id_id_5b537516_fk_Customer_customer_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Customer` (`customer_id`);
ALTER TABLE `CustAddress` ADD CONSTRAINT `CustAddress_add_id_id_0772091b_fk_Address_add_id` FOREIGN KEY (`add_id_id`) REFERENCES `Address` (`add_id`);
ALTER TABLE `CustAddress` ADD CONSTRAINT `CustAddress_customer_id_id_48729482_fk_Customer_customer_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Customer` (`customer_id`);