SELECT d.go_id, g.go_term, count(g.go_id) as "count" FROM Described_By d INNER JOIN Gene_Ontology g on g.go_id =d.go_id GROUP BY(g.go_term);
