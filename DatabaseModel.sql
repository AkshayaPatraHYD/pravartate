-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 10, 2016 at 03:03 PM
-- Server version: 5.6.20
-- PHP Version: 5.5.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Pravartate`
--

-- --------------------------------------------------------

--
-- Table structure for table `AttendanceOLTP`
--

CREATE TABLE IF NOT EXISTS `AttendanceOLTP` (
  `time` datetime NOT NULL,
  `adminPhoneNumber` int(10) NOT NULL,
  `textMessage` varchar(100) NOT NULL,
  `schoolid` int(11) NOT NULL,
  `adminid` int(11) NOT NULL,
  `adminName` varchar(100) NOT NULL,
  `schoolTotal` int(11) NOT NULL,
  `schoolName` varchar(1000) NOT NULL,
  `mandal` varchar(1000) NOT NULL,
  `ItoVAttendance` int(11) NOT NULL,
  `VItoVIIIAttendance` int(11) NOT NULL,
  `IXtoXAttendance` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Kitchen`
--

CREATE TABLE IF NOT EXISTS `Kitchen` (
  `id` int(11) NOT NULL,
  `kitchenCode` varchar(1000) NOT NULL,
  `kitchenName` varchar(1000) NOT NULL,
  `area` varchar(1000) NOT NULL,
  `managerid` int(11) NOT NULL,
  `district` varchar(1000) NOT NULL,
  `city` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Login`
--

CREATE TABLE IF NOT EXISTS `Login` (
  `loginId` int(11) NOT NULL,
  `group` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(3000) NOT NULL,
  `createdOn` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Manager`
--

CREATE TABLE IF NOT EXISTS `Manager` (
  `managerid` int(11) NOT NULL,
  `managerName` varchar(1000) NOT NULL,
  `managerPhone` int(10) NOT NULL,
  `schoolid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `School`
--

CREATE TABLE IF NOT EXISTS `School` (
  `schoolid` int(11) NOT NULL,
  `district` varchar(50) NOT NULL,
  `schoolName` varchar(400) NOT NULL,
  `mandal` varchar(100) NOT NULL,
  `ItoVTotal` int(11) NOT NULL,
  `VItoVIIITotal` int(11) NOT NULL,
  `IXtoXTotal` int(11) NOT NULL,
  `allTotal` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `adminid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SchoolAdmins`
--

CREATE TABLE IF NOT EXISTS `SchoolAdmins` (
  `schoolid` int(11) NOT NULL,
  `adminid` int(11) NOT NULL,
  `adminName` varchar(100) NOT NULL,
  `adminPhoneNumber` int(10) NOT NULL,
  `adminDesignation` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
