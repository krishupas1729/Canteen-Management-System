-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 07, 2026 at 12:55 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `canteen_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`, `description`) VALUES
(1, 'Snacks', 'Quick bites and snacks'),
(2, 'Beverages', 'Hot and cold drinks'),
(3, 'Meals', 'Full meals'),
(6, 'Desserts', 'Sweet dishes and desserts'),
(7, 'Fast Food', 'Quick fast food items');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `customer_type` varchar(20) NOT NULL DEFAULT 'Student',
  `registration_date` date NOT NULL DEFAULT curdate()
) ;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `customer_name`, `phone`, `customer_type`, `registration_date`) VALUES
(1, 'Aarav Sharma', '9811111111', 'Student', '2026-11-06'),
(2, 'Priya Verma', '9822222222', 'Faculty', '2026-11-06'),
(3, 'Rashid ', '9876543210', 'Student', '2026-11-06'),
(4, 'Mayank Jha', '7982573828', 'Student', '2026-11-07'),
(5, 'Rahul Sharma', NULL, 'Student', '2026-11-07'),
(6, 'Amit Kumar', NULL, 'Student', '2026-11-07'),
(7, 'Neha Singh', NULL, 'Student', '2026-11-07'),
(8, 'Rohan Mehta', NULL, 'Student', '2026-11-07'),
(9, 'Krishu', '7999663300', 'Student', '2026-11-07');

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `expense_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `expense_category` varchar(50) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `expense_date` date NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`expense_id`, `user_id`, `expense_category`, `amount`, `expense_date`, `description`, `created_at`) VALUES
(1, 1, 'Electricity', 1000.00, '2026-11-07', 'Monthly electricity test', '2026-11-07 11:02:58'),
(2, 1, 'Electricity', 3500.00, '2026-11-01', 'Monthly electricity bill', '2026-11-07 12:51:08'),
(3, 1, 'Rent', 12000.00, '2026-11-02', 'Monthly canteen rent', '2026-11-07 12:51:08'),
(4, 1, 'Transportation', 800.00, '2026-11-03', 'Goods transportation', '2026-11-07 12:51:08'),
(5, 1, 'Maintenance', 1500.00, '2026-11-04', 'Canteen equipment maintenance', '2026-11-07 12:51:08'),
(6, 1, 'Miscellaneous', 500.00, '2026-11-04', 'Other canteen expenses', '2026-11-07 12:51:09');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_available` int(11) NOT NULL DEFAULT 0,
  `reorder_level` int(11) NOT NULL DEFAULT 5,
  `last_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`inventory_id`, `product_id`, `quantity_available`, `reorder_level`, `last_updated`) VALUES
(1, 1, 30, 5, '2026-11-06 10:34:19'),
(2, 2, 55, 15, '2026-11-07 13:18:02'),
(3, 3, 25, 5, '2026-11-06 10:34:19'),
(4, 4, 20, 5, '2026-11-06 10:34:19'),
(5, 9, 43, 5, '2026-11-07 13:18:02'),
(6, 10, 28, 5, '2026-11-07 12:48:56'),
(7, 11, 57, 5, '2026-11-07 12:48:56'),
(9, 13, 15, 10, '2026-11-07 13:27:50');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `order_date` datetime NOT NULL DEFAULT current_timestamp(),
  `order_status` varchar(20) NOT NULL DEFAULT 'Pending'
) ;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `customer_id`, `user_id`, `order_date`, `order_status`) VALUES
(1, NULL, 1, '2026-11-07 11:40:35', 'Completed'),
(2, 5, 1, '2026-11-06 09:30:00', 'Completed'),
(3, 2, 1, '2026-11-06 10:00:00', 'Completed'),
(4, 6, 1, '2026-11-06 10:30:00', 'Preparing'),
(5, 7, 1, '2026-11-06 11:00:00', 'Pending'),
(6, NULL, 1, '2026-11-07 13:18:02', 'Completed'),
(7, NULL, 1, '2026-11-07 13:27:03', 'Completed'),
(8, NULL, 1, '2026-11-07 13:27:50', 'Completed');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL
) ;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `product_id`, `quantity`, `unit_price`) VALUES
(1, 1, 2, 2, 15.00),
(2, 2, 9, 2, 15.00),
(3, 2, 2, 1, 15.00),
(4, 3, 1, 1, 50.00),
(5, 3, 3, 1, 40.00),
(6, 4, 4, 2, 90.00),
(7, 5, 11, 3, 20.00),
(8, 6, 2, 5, 15.00),
(9, 6, 9, 5, 15.00),
(10, 7, 13, 2, 100.00),
(11, 8, 13, 3, 100.00);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `payment_date` datetime NOT NULL DEFAULT current_timestamp(),
  `payment_status` varchar(20) NOT NULL DEFAULT 'Paid',
  `transaction_reference` varchar(100) DEFAULT NULL
) ;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `order_id`, `amount`, `payment_method`, `payment_date`, `payment_status`, `transaction_reference`) VALUES
(1, 1, 30.00, 'Cash', '2026-11-07 11:40:35', 'Paid', NULL),
(2, 2, 45.00, 'Cash', '2026-11-06 09:30:00', 'Paid', NULL),
(3, 3, 90.00, 'UPI', '2026-11-06 10:00:00', 'Paid', NULL),
(4, 6, 150.00, 'Cash', '2026-11-07 13:18:02', 'Paid', NULL),
(5, 7, 200.00, 'Cash', '2026-11-07 13:27:03', 'Paid', NULL),
(6, 8, 300.00, 'Cash', '2026-11-07 13:27:50', 'Paid', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `selling_price` decimal(10,2) NOT NULL,
  `cost_price` decimal(10,2) NOT NULL,
  `is_available` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `category_id`, `product_name`, `description`, `selling_price`, `cost_price`, `is_available`, `created_at`) VALUES
(1, 1, 'Veg Sandwich', 'Fresh vegetable sandwich', 50.00, 30.00, 1, '2026-11-06 10:34:19'),
(2, 2, 'Tea', 'Regular milk tea', 15.00, 7.00, 1, '2026-11-06 10:34:19'),
(3, 2, 'Cold Coffee', 'Chilled coffee', 40.00, 22.00, 1, '2026-11-06 10:34:19'),
(4, 3, 'Veg Thali', 'Daily vegetarian meal', 90.00, 60.00, 1, '2026-11-06 10:34:19'),
(5, 1, 'Waffle Special', 'Special chocolate waffle', 120.00, 65.00, 0, '2026-11-06 15:42:28'),
(6, 3, 'Dosa', 'Masala dosa', 50.00, 27.00, 0, '2026-11-07 10:29:40'),
(7, 3, 'dosa', 'masala dosa', 50.00, 27.00, 0, '2026-11-07 10:41:40'),
(8, 3, 'Dosa', 'Masala Dosa', 50.00, 27.00, 0, '2026-11-07 12:29:55'),
(9, 1, 'Samosa', 'Crispy potato samosa', 15.00, 8.00, 1, '2026-11-07 12:46:41'),
(10, 1, 'Aloo Tikki', 'Crispy potato tikki', 20.00, 12.00, 1, '2026-11-07 12:46:41'),
(11, 6, 'Gulab Jamun', 'Traditional sweet dish', 20.00, 10.00, 1, '2026-11-07 12:46:41'),
(12, 3, 'Dosa', 'Masala Dosa', 50.00, 25.00, 1, '2026-11-07 13:13:42'),
(13, 6, 'waffle', 'milk chocolate waffle', 100.00, 65.00, 1, '2026-11-07 13:23:23');

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `purchase_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `purchase_date` datetime NOT NULL DEFAULT current_timestamp(),
  `invoice_number` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`purchase_id`, `supplier_id`, `user_id`, `purchase_date`, `invoice_number`) VALUES
(1, 1, 1, '2026-11-06 09:00:00', 'INV-001'),
(2, 4, 1, '2026-11-06 10:00:00', 'INV-002'),
(3, 5, 1, '2026-11-06 11:00:00', 'INV-003');

-- --------------------------------------------------------

--
-- Table structure for table `purchase_items`
--

CREATE TABLE `purchase_items` (
  `purchase_item_id` int(11) NOT NULL,
  `purchase_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_cost` decimal(10,2) NOT NULL
) ;

--
-- Dumping data for table `purchase_items`
--

INSERT INTO `purchase_items` (`purchase_item_id`, `purchase_id`, `product_id`, `quantity`, `unit_cost`) VALUES
(1, 1, 9, 50, 8.00),
(2, 1, 10, 30, 12.00),
(3, 2, 2, 100, 4.00),
(4, 2, 3, 40, 22.00),
(5, 3, 4, 20, 55.00),
(6, 3, 11, 60, 10.00),
(7, 3, 1, 25, 20.00);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `supplier_id` int(11) NOT NULL,
  `supplier_name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `supplier_name`, `phone`, `email`, `address`) VALUES
(1, 'Fresh Foods Supplier', '9876543210', 'fresh@example.com', 'Delhi'),
(2, 'Campus Beverage Supply', '9876501234', 'drinks@example.com', 'New Delhi'),
(3, 'Raghav Milk supplier', '7788990000', 'raghav@example.com', 'New delhi'),
(4, 'Daily Dairy Products', '9876501235', 'dairy@example.com', 'Delhi'),
(5, 'City Beverage Distributors', '9876501236', 'beverages@example.com', 'New Delhi');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `is_active` tinyint(1) NOT NULL DEFAULT 1
) ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `full_name`, `username`, `password_hash`, `role`, `created_at`, `is_active`) VALUES
(1, 'Canteen Administrator', 'admin', 'admin123', 'Admin', '2026-11-06 10:34:19', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `category_name` (`category_name`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`expense_id`),
  ADD KEY `fk_expenses_user` (`user_id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`inventory_id`),
  ADD UNIQUE KEY `product_id` (`product_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `fk_orders_customer` (`customer_id`),
  ADD KEY `fk_orders_user` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD UNIQUE KEY `uq_order_product` (`order_id`,`product_id`),
  ADD KEY `fk_order_items_product` (`product_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD UNIQUE KEY `order_id` (`order_id`),
  ADD UNIQUE KEY `transaction_reference` (`transaction_reference`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `fk_products_category` (`category_id`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`purchase_id`),
  ADD UNIQUE KEY `invoice_number` (`invoice_number`),
  ADD KEY `fk_purchases_supplier` (`supplier_id`),
  ADD KEY `fk_purchases_user` (`user_id`);

--
-- Indexes for table `purchase_items`
--
ALTER TABLE `purchase_items`
  ADD PRIMARY KEY (`purchase_item_id`),
  ADD UNIQUE KEY `uq_purchase_product` (`purchase_id`,`product_id`),
  ADD KEY `fk_purchase_items_product` (`product_id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `expense_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
  MODIFY `purchase_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `purchase_items`
--
ALTER TABLE `purchase_items`
  MODIFY `purchase_item_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `fk_expenses_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `fk_inventory_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `fk_orders_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_orders_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_order_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON UPDATE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `fk_payments_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON UPDATE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON UPDATE CASCADE;

--
-- Constraints for table `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `fk_purchases_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_purchases_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `purchase_items`
--
ALTER TABLE `purchase_items`
  ADD CONSTRAINT `fk_purchase_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_purchase_items_purchase` FOREIGN KEY (`purchase_id`) REFERENCES `purchases` (`purchase_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
