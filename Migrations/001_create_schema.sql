-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `kharchakhatadb` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema kharchakhatadb
-- -----------------------------------------------------
USE `kharchakhatadb` ;

-- -----------------------------------------------------
-- Table `kharchakhatadb`.`sex`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`sex` (
  `sex_id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`sex_id`),
  UNIQUE INDEX `sex_id_UNIQUE` (`sex_id` ASC) );


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NOT NULL,
  `mname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `dob` DATE NULL,
  `email` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(13) NULL,
  `password` VARCHAR(45) NOT NULL,
  `sex` INT NULL,
  `active` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`user_id`),
  INDEX `fk_users_sex1_idx` (`sex` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) ,
  CONSTRAINT `fk_users_sex1`
    FOREIGN KEY (`sex`)
    REFERENCES `kharchakhatadb`.`sex` (`sex_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`frequency`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`frequency` (
  `frequency_id` INT NOT NULL AUTO_INCREMENT,
  `frequency` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`frequency_id`),
  UNIQUE INDEX `frequency_id_UNIQUE` (`frequency_id` ASC) ,
  UNIQUE INDEX `frequency_UNIQUE` (`frequency` ASC) );


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`payment_medium`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`payment_medium` (
  `medium_id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`medium_id`),
  UNIQUE INDEX `medium_id_UNIQUE` (`medium_id` ASC) ,
  UNIQUE INDEX `type_UNIQUE` (`type` ASC) );


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`type` (
  `type_id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`type_id`),
  UNIQUE INDEX `type_id_UNIQUE` (`type_id` ASC) ,
  UNIQUE INDEX `type_UNIQUE` (`type` ASC) );


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`sub_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`sub_type` (
  `sub_type_id` INT NOT NULL AUTO_INCREMENT,
  `subtype` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`sub_type_id`),
  UNIQUE INDEX `sub_type_id_UNIQUE` (`sub_type_id` ASC) ,
  UNIQUE INDEX `subtype_UNIQUE` (`subtype` ASC) );


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`type_subtype`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`type_subtype` (
  `type_subtype_id` INT NOT NULL AUTO_INCREMENT,
  `type_id` INT NOT NULL,
  `sub_type_id` INT NOT NULL,
  PRIMARY KEY (`type_subtype_id`),
  UNIQUE INDEX `type_subtype_id_UNIQUE` (`type_subtype_id` ASC) ,
  INDEX `fk_type_subtype_type1_idx` (`type_id` ASC) ,
  INDEX `fk_type_subtype_sub_type1_idx` (`sub_type_id` ASC) ,
  CONSTRAINT `fk_type_subtype_type1`
    FOREIGN KEY (`type_id`)
    REFERENCES `kharchakhatadb`.`type` (`type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_type_subtype_sub_type1`
    FOREIGN KEY (`sub_type_id`)
    REFERENCES `kharchakhatadb`.`sub_type` (`sub_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`expences`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`expences` (
  `expence_id` INT NOT NULL AUTO_INCREMENT,
  `expence_name` VARCHAR(45) NOT NULL,
  `date` DATE NOT NULL,
  `time` TIME NULL,
  `credit` FLOAT NULL,
  `debit` FLOAT NULL,
  `user_id` INT NOT NULL,
  `frequency_id` INT NOT NULL,
  `payment_medium_id` INT NOT NULL,
  `type_subtype_id` INT NOT NULL,
  PRIMARY KEY (`expence_id`),
  INDEX `fk_expences_users_idx` (`user_id` ASC) ,
  INDEX `fk_expences_frequency1_idx` (`frequency_id` ASC) ,
  INDEX `fk_expences_payment_medium1_idx` (`payment_medium_id` ASC) ,
  INDEX `fk_expences_type_subtype1_idx` (`type_subtype_id` ASC) ,
  UNIQUE INDEX `expence_id_UNIQUE` (`expence_id` ASC) ,
  CONSTRAINT `fk_expences_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `kharchakhatadb`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `fk_expences_frequency`
    FOREIGN KEY (`frequency_id`)
    REFERENCES `kharchakhatadb`.`frequency` (`frequency_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_expences_payment_medium`
    FOREIGN KEY (`payment_medium_id`)
    REFERENCES `kharchakhatadb`.`payment_medium` (`medium_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_expences_type_subtype1`
    FOREIGN KEY (`type_subtype_id`)
    REFERENCES `kharchakhatadb`.`type_subtype` (`type_subtype_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `kharchakhatadb`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kharchakhatadb`.`admin` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NOT NULL,
  `mname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `dob` DATE NULL,
  `email` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(13) NULL,
  `password` VARCHAR(45) NOT NULL,
  `sex` INT NULL,
  `active` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`user_id`),
  INDEX `fk_users_sex1_idx` (`sex` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) ,
  CONSTRAINT `fk_users_sex10`
    FOREIGN KEY (`sex`)
    REFERENCES `kharchakhatadb`.`sex` (`sex_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
