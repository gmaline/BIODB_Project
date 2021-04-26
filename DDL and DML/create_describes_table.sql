CREATE TABLE Described_By (
	go_id varchar(100) NOT NULL,
	project_id varchar(100) NOT NULL,
	PRIMARY KEY (go_id, project_id)
);