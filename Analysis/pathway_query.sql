SELECT f.pathway_name, k.pathway_name, COUNT(f.pathway_name) as "count" FROM Functions_In f INNER JOIN KEGG_Pathway k ON k.pathway_id = f.pathway_name GROUP BY(f.pathway_name) ORDER BY count DESC;
