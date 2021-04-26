CREATE TABLE expression (
	eid int NOT NULL AUTO_INCREMENT,
	gene_symbol varchar(100) NOT NULL,
	project_id varchar(100),
	sample_id varchar(100),
	direction varchar(100),
	PRIMARY KEY (eid)
);