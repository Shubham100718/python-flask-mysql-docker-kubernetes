-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 08, 2024 at 11:47 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ms_tribunals_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `applicant_legal_representative`
--

CREATE TABLE `applicant_legal_representative` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `applicant_legal_representative_name` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `applicant_name`
--

CREATE TABLE `applicant_name` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `applicant_name` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `case_details`
--

CREATE TABLE `case_details` (
  `id` int(11) NOT NULL,
  `court_type_id` int(11) DEFAULT NULL,
  `filing_no` varchar(255) DEFAULT NULL,
  `date_of_filing` varchar(50) DEFAULT NULL,
  `case_no` varchar(255) DEFAULT NULL,
  `registration_date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `modified_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `case_status` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `case_history`
--

CREATE TABLE `case_history` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `sr_no` varchar(11) DEFAULT NULL,
  `hearing_date` varchar(50) DEFAULT NULL,
  `court_no` varchar(11) DEFAULT NULL,
  `purpose` varchar(255) DEFAULT NULL,
  `action` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `case_history_details`
--

CREATE TABLE `case_history_details` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `case_history_id` int(11) DEFAULT NULL,
  `case_no` varchar(255) DEFAULT NULL,
  `diary_no` varchar(50) DEFAULT NULL,
  `listing_date` varchar(50) DEFAULT NULL,
  `court_no` varchar(11) DEFAULT NULL,
  `coram` text DEFAULT NULL,
  `proceeding_summary` text DEFAULT NULL,
  `stage_of_case` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `case_list`
--

CREATE TABLE `case_list` (
  `id` int(11) NOT NULL,
  `court_type_id` int(11) DEFAULT NULL,
  `search_by` int(11) DEFAULT NULL COMMENT '1-caseno,2-filingno,3-casetype,4-party,5-advocate',
  `location` varchar(50) DEFAULT NULL COMMENT 'delhi / chennai',
  `sr_no` varchar(11) DEFAULT NULL,
  `filing_no` varchar(250) DEFAULT NULL,
  `case_no` varchar(250) DEFAULT NULL,
  `case_title` longtext DEFAULT NULL,
  `registration_date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `action` varchar(11) DEFAULT NULL,
  `advocate_name` varchar(255) DEFAULT NULL,
  `party_name` varchar(255) DEFAULT NULL,
  `party_type` varchar(11) DEFAULT NULL,
  `case_type` varchar(11) DEFAULT NULL,
  `case_number` varchar(11) DEFAULT NULL,
  `case_year` varchar(11) DEFAULT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `case_status` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `case_status_category`
--

CREATE TABLE `case_status_category` (
  `id` int(11) NOT NULL,
  `case_status_name` varchar(50) DEFAULT NULL,
  `case_status_id` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `case_status_category`
--

INSERT INTO `case_status_category` (`id`, `case_status_name`, `case_status_id`) VALUES
(1, 'All', 'all'),
(2, 'Pending', 'P'),
(3, 'Dispose', 'D');

-- --------------------------------------------------------

--
-- Table structure for table `case_type_category`
--

CREATE TABLE `case_type_category` (
  `id` int(11) NOT NULL,
  `case_type_name` varchar(50) DEFAULT NULL,
  `case_type_id` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `case_type_category`
--

INSERT INTO `case_type_category` (`id`, `case_type_name`, `case_type_id`) VALUES
(1, 'Compensation Application', '36'),
(2, 'Interlocutory Application', '35'),
(3, 'Company Appeal(AT)', '32'),
(4, 'Company Appeal(AT)(Ins)', '33'),
(5, 'Competition Appeal(AT)', '34'),
(6, 'Contempt Case(AT)', '37'),
(7, 'Review Application', '38'),
(8, 'Restoration Application', '39'),
(9, 'Transfer Appeal', '40'),
(10, 'Transfer Original Petition (MRTP-AT)', '61');

-- --------------------------------------------------------

--
-- Table structure for table `connected_cases`
--

CREATE TABLE `connected_cases` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `sr_no` varchar(11) DEFAULT NULL,
  `filing_no` varchar(50) DEFAULT NULL,
  `case_no` varchar(255) DEFAULT NULL,
  `date_of_filing` varchar(50) DEFAULT NULL,
  `registration_date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `first_hearing_details`
--

CREATE TABLE `first_hearing_details` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `court_no` varchar(50) DEFAULT NULL,
  `hearing_date` varchar(50) DEFAULT NULL,
  `coram` text DEFAULT NULL,
  `stage_of_case` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ias_other_application`
--

CREATE TABLE `ias_other_application` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `sr_no` varchar(11) DEFAULT NULL,
  `filing_no` varchar(50) DEFAULT NULL,
  `case_no` varchar(255) DEFAULT NULL,
  `date_of_filing` varchar(50) DEFAULT NULL,
  `registration_date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `last_hearing_details`
--

CREATE TABLE `last_hearing_details` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `court_no` varchar(50) DEFAULT NULL,
  `hearing_date` varchar(50) DEFAULT NULL,
  `coram` text DEFAULT NULL,
  `stage_of_case` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `location_category`
--

CREATE TABLE `location_category` (
  `id` int(11) NOT NULL,
  `location_name` varchar(50) DEFAULT NULL,
  `location_id` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `location_category`
--

INSERT INTO `location_category` (`id`, `location_name`, `location_id`) VALUES
(1, 'New Delhi', 'delhi'),
(2, 'Chennai', 'chennai');

-- --------------------------------------------------------

--
-- Table structure for table `next_hearing_details`
--

CREATE TABLE `next_hearing_details` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `hearing_date` varchar(50) DEFAULT NULL,
  `court_no` varchar(50) DEFAULT NULL,
  `proceedings_summary` text DEFAULT NULL,
  `stage_of_case` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order_history`
--

CREATE TABLE `order_history` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `sr_no` varchar(11) DEFAULT NULL,
  `order_date` varchar(50) DEFAULT NULL,
  `order_type` varchar(255) DEFAULT NULL,
  `view` varchar(50) DEFAULT NULL,
  `orders_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `party_type_category`
--

CREATE TABLE `party_type_category` (
  `id` int(11) NOT NULL,
  `party_type_name` varchar(50) DEFAULT NULL,
  `party_type_id` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `party_type_category`
--

INSERT INTO `party_type_category` (`id`, `party_type_name`, `party_type_id`) VALUES
(1, 'Main Party', '1'),
(2, 'Addtional Party', '2');

-- --------------------------------------------------------

--
-- Table structure for table `respondant_name`
--

CREATE TABLE `respondant_name` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `respondant_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `respondent_legal_representative`
--

CREATE TABLE `respondent_legal_representative` (
  `id` int(11) NOT NULL,
  `court_case_id` int(11) DEFAULT NULL,
  `respondent_legal_representative_name` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applicant_legal_representative`
--
ALTER TABLE `applicant_legal_representative`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `applicant_name`
--
ALTER TABLE `applicant_name`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `case_details`
--
ALTER TABLE `case_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `case_history`
--
ALTER TABLE `case_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `case_history_details`
--
ALTER TABLE `case_history_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `case_list`
--
ALTER TABLE `case_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `case_status_category`
--
ALTER TABLE `case_status_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `case_type_category`
--
ALTER TABLE `case_type_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `connected_cases`
--
ALTER TABLE `connected_cases`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `first_hearing_details`
--
ALTER TABLE `first_hearing_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ias_other_application`
--
ALTER TABLE `ias_other_application`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `last_hearing_details`
--
ALTER TABLE `last_hearing_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `location_category`
--
ALTER TABLE `location_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `next_hearing_details`
--
ALTER TABLE `next_hearing_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_history`
--
ALTER TABLE `order_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `party_type_category`
--
ALTER TABLE `party_type_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `respondant_name`
--
ALTER TABLE `respondant_name`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `respondent_legal_representative`
--
ALTER TABLE `respondent_legal_representative`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applicant_legal_representative`
--
ALTER TABLE `applicant_legal_representative`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `applicant_name`
--
ALTER TABLE `applicant_name`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `case_details`
--
ALTER TABLE `case_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `case_history`
--
ALTER TABLE `case_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `case_history_details`
--
ALTER TABLE `case_history_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `case_list`
--
ALTER TABLE `case_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `connected_cases`
--
ALTER TABLE `connected_cases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `first_hearing_details`
--
ALTER TABLE `first_hearing_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ias_other_application`
--
ALTER TABLE `ias_other_application`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `last_hearing_details`
--
ALTER TABLE `last_hearing_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `next_hearing_details`
--
ALTER TABLE `next_hearing_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order_history`
--
ALTER TABLE `order_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `respondant_name`
--
ALTER TABLE `respondant_name`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `respondent_legal_representative`
--
ALTER TABLE `respondent_legal_representative`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
