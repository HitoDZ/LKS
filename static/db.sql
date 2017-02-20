Create table log_pass(user_id VARCHAR(6) PRIMARY KEY, login VARCHAR(60) NOT NULL, password VARCHAR(60) NOT NULL, role int not null);

Create table comands(comand_id VARCHAR(6) PRIMARY KEY, name Varchar(60) not null,  grad1 int , grad2 int, nomination varchar (30) NOT NULL);

CREATE TABLE judge(judge_id int Primary Key,
                   user_id VARCHAR(6) REFERENCES log_pass NOT NULL ,
                   comand_id VARCHAR(6) REFERENCES comands NOT NULL,
                   technique int, production int, teamwork int,artistry int,
                   musicality int,show int,creativity int);
-- ---------------------------------------------------------------------------------------------------------------------------------------------
Alter Table comands Add Column C_order int unique ;
Alter Table comands Add Column C_order2 int unique ;
Alter Table log_pass Add Column name int unique ;
