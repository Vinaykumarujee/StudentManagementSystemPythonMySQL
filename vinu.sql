-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 02, 2020 at 07:06 AM
-- Server version: 10.1.13-MariaDB
-- PHP Version: 5.6.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vinu`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `AId` int(11) NOT NULL,
  `AU` varchar(50) NOT NULL,
  `AP` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`AId`, `AU`, `AP`) VALUES
(1, 'admin1', 'admin1'),
(2, 'admin2', 'admin2'),
(3, 'admin3', 'admin3');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `CourseName` varchar(50) NOT NULL,
  `CourseId` varchar(50) NOT NULL,
  `CourseFee` varchar(50) NOT NULL,
  `CourseDuration` varchar(50) NOT NULL,
  `CourseDept` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`CourseName`, `CourseId`, `CourseFee`, `CourseDuration`, `CourseDept`) VALUES
('BC', 'BC 908', '90000', '3 years', 'COM'),
('BCOM', 'BCOM 102', '66000', '3 years', 'COM'),
('BSC', 'BSC 102', '70000', '3 years', 'MATHS'),
('BSC AG', 'AGRI 102', '76000', '3 years', 'AGRI'),
('BTECH', 'Btech 102', '56000', '4 Years', 'CSE'),
('MCOM', 'MCOM 102', '75000', '2 years', 'COM'),
('MSC', 'MSC 102', '80000', '2 years', 'MATHS'),
('MTECH', 'Mtech 102', '50000', '2 Years', 'CSE'),
('PHD', 'PHD 102', '60000', '2 Years', 'CSE');

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `DeptName` varchar(50) NOT NULL,
  `DeptCode` varchar(50) NOT NULL,
  `DeptHOD` varchar(50) NOT NULL,
  `DeptEmp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`DeptName`, `DeptCode`, `DeptHOD`, `DeptEmp`) VALUES
('AGRI', 'AGRI102', 'AGRI HOD', 98),
('BC', 'BC 000', 'HOD BC', 98),
('BIO', 'BIO102', 'BIO HOD', 54),
('COM', 'COM102', 'COM HOD', 43),
('COPA', 'COPA 111', 'COPA 123', 76),
('CSE', 'CS102', 'ABC', 56),
('EE', 'EE102', 'EE HOD', 85),
('IT', 'IT102', 'XYZ', 87),
('MATHS', 'Math102', 'MATH HOD', 70),
('ME', 'ME102', 'ME HOD', 69);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `StudentId` varchar(50) NOT NULL,
  `RollNo` varchar(50) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `CourseName` varchar(50) NOT NULL,
  `Phone` varchar(50) NOT NULL,
  `Gmail` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`StudentId`, `RollNo`, `FirstName`, `LastName`, `CourseName`, `Phone`, `Gmail`) VALUES
('', '16115026', 'Kshitij', 'UK', 'BTECH', '9879879876', 'G@f.d'),
('', '16115067', 'Rupesh', 'Sahu', 'MTECH', '8827016669', 'Rup@gmial.com'),
('', '16115084', 'Thallu', 'Sahu', 'PHD', '9876543219', 'Thallu@g.c'),
('', '16115087', 'Vinay', 'Ujee', 'BTECH', '8827014449', 'Vinay@gmial.com'),
('', '16115095', 'Laddu', 'Markam', 'BSC', '8827019999', 'Laddu@gmial.com'),
('', '16115098', 'Naveen', 'Nag', 'BCOM', '8827011119', 'Naveen@gmial.com'),
('', '77777777', 'Vinu', 'Ujji', 'PHD', '9809809809', 'Vin@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `RollNo` varchar(50) NOT NULL,
  `UN` varchar(50) NOT NULL,
  `UP` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`RollNo`, `UN`, `UP`) VALUES
('16115087', 'user1', '1111'),
('16115084', 'EUILGM', 'OETFTG'),
('16115026', 'ZGCBOI', '9999'),
('77777777', 'BYCQTX', 'AOTOMX');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`AId`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`CourseName`),
  ADD KEY `CourseDept` (`CourseDept`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`DeptName`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`RollNo`),
  ADD KEY `CourseName` (`CourseName`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD KEY `RollNo` (`RollNo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `AId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`CourseDept`) REFERENCES `department` (`DeptName`) ON DELETE CASCADE;

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`CourseName`) REFERENCES `course` (`CourseName`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`RollNo`) REFERENCES `students` (`RollNo`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
