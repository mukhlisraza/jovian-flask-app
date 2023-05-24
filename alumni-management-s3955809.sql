-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 23, 2023 at 08:00 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `alumni-management-s3955809`
--

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `id` int(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `user_id` int(20) NOT NULL,
  `document_type` varchar(255) NOT NULL,
  `document_url` varchar(255) NOT NULL,
  `unique_number` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`id`, `title`, `user_id`, `document_type`, `document_url`, `unique_number`, `created_at`, `updated_at`) VALUES
(1, 'Bachelor of Computer Science', 3, 'degree', '/static/files/1234567890.pdf', '1234567890', '2023-05-22 21:28:20', '2023-05-22 21:28:20'),
(2, 'Java Developer', 3, 'certificate', '/static/files/9876543210.pdf', '9876543210', '2023-05-22 21:30:17', '2023-05-22 21:30:17'),
(3, 'Python Developer', 3, 'certificate', '/static/files/0123456789.pdf', '0123456789', '2023-05-22 22:04:10', '2023-05-22 22:04:10'),
(4, 'Bachelor of Arts in English', 2, 'degree', '/static/files/7654321098.pdf', '7654321098', '2023-05-23 13:18:39', '2023-05-23 13:18:39'),
(5, 'Certified Public Accountant', 2, 'certificate', '/static/files/3210987654.pdf', '3210987654', '2023-05-23 13:21:02', '2023-05-23 13:21:02'),
(6, 'Certified Occupational Therapy Assistant', 1, 'certificate', '/static/files/4321098765.pdf', '4321098765', '2023-05-23 13:55:37', '2023-05-23 13:55:37');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(20) NOT NULL,
  `user_id` int(20) NOT NULL,
  `role` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `user_id`, `role`, `created_at`, `updated_at`) VALUES
(1, 1, 'alumni', '2023-05-22 13:31:36', '2023-05-22 13:31:36'),
(2, 2, 'alumni', '2023-05-22 13:35:08', '2023-05-22 13:35:08'),
(3, 3, 'alumni', '2023-05-22 21:36:49', '2023-05-22 21:36:49'),
(4, 5, 'alumni', '2023-05-23 14:02:24', '2023-05-23 14:02:24');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(20) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `created_at`, `updated_at`) VALUES
(1, 'hanif', '$2b$12$2fR9IKL2QFeIPGTXUDiAS.LKrAIqfj6vFf/THDd9IFyB2mxom4Uzm', '2023-05-22 12:07:43', '2023-05-22 12:07:43'),
(2, 'johndoe', '$2b$12$3LD8luF9.xDZhZf6AOG9l.naiLoNMK8UmknPiz3VtnJS6on9wMlWu', '2023-05-22 13:35:08', '2023-05-22 13:35:08'),
(3, 'danielvitorrie', '$2b$12$0yr6nuiIOCu/trPOAJ43k.4tjL0PA8H13OIfg46R7xPBYzhv6b3hC', '2023-05-22 21:36:49', '2023-05-22 21:36:49');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
