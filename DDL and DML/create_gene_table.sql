CREATE TABLE gene (
	gene_id int NOT NULL AUTO_INCREMENT,
	gene_symbol varchar(100) NOT NULL,
	gene_name varchar(500),
	PRIMARY KEY (gene_id)
);