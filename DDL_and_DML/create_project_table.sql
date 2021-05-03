CREATE TABLE project (
	project_id varchar(30) NOT NULL,
	authors varchar(300) NOT NULL,
	proj_date varchar(30),
	taxid varchar(10),
	tissue varchar(100),
	PRIMARY KEY (project_id)
);