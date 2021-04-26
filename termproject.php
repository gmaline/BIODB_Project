<!DOCTYPE html>
<html>
<title>COVID-19 Gene Expression DB</title>
<body>
<style>
table, th, td {
  border: 1px solid black;
  text-align: center;
}
table {
  width: 90%;
}
.header {
  padding: 30px;
  text-align: center;
  background: #023047;
  color: white;
  font-size: 30px;
}
body {
  text-align: center;
}
</style>


<div class="header">
  <h1>COVID-19 Gene Expression Database</h1>
</div>
</br>
<div class="body">
<form method="post" action="<?php echo $_SERVER['PHP_SELF'];?>">
  <label for="search_keys"> Select a Search Term: </label>
  <select name="search_keys" id="search_keys">
    <option value="gene_symbol">Gene Symbol</option>
    <option value="pathway_name">KEGG Pathway</option>
    <option value="go_term">GO Term</option>
  </select>
  <select name="search_type" id="search_type">
    <option value="summary">Summary</option>
    <option value="occurences">All Occurences</option>
  </select>
  <input type="text" name="key">
  <input type="submit">
</form>
</div>
</br>

<?php
$key = "empty";
/*Process info from a webuser*/ 
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // collect value of input field
    $key = $_POST['key']; 
    $key_type = $_POST['search_keys'];
    $search_type = $_POST['search_type'];
    echo "<br>";
    if (empty($key)) {
        $all = True;
    } else {
        echo "Showing results for $key.<br>";
    }   
}

$server="localhost";
$username="gmaline";
$password="";
$database="gmaline";

/*Connect to my database
* and throw errors if its unable to connect.
* Greets the web user if it is able to connect.*/
$connect = mysqli_connect($server,$username,"",$database);

if($connect->connect_error){
	echo "Connection error:" .$connect->connect_error;
}

/*Perform the queries based on search type and key type*/
$table_header = "";
if ($search_type == "summary") { 
	print("Summary:");
	if ($key_type == "gene_symbol") {
		$table_header = "<th>Gene Symbol</th><th>Differential " .
			"Expression</th><th>Count</th>";
		if ($key != '') {
			$query = "SELECT gene_symbol, direction, " .
				"COUNT(gene_symbol) as \"count\" FROM " .
				"expression WHERE ". $key_type ." = \"". $key . 
				"\";";
		}
		else {
			$query = "SELECT gene_symbol, direction, " .
				"COUNT(gene_symbol) as \"count\" FROM " .
				"expression GROUP BY(gene_symbol) ORDER BY " .
				"count DESC;";
		}
	}
	if ($key_type == "pathway_name") {
		$table_header = "<th>Pahtway ID</th><th>Pathway Name</th><th>Count</th>";
		// specific search not working.
		if ($key != '') {
			$query = "SELECT pathway_name, COUNT(pathway_name) as \"count\" FROM Funtions_In WHERE ". $key_type ." = \"". $key . "\";";
		}
		else {
			$query = "SELECT f.pathway_name, k.pathway_name, " .
				"COUNT(f.pathway_name) as \"count\" FROM " .
				"Functions_In f INNER JOIN KEGG_Pathway k ON " . 
				"k.pathway_id = f.pathway_name " . 
				"GROUP BY(f.pathway_name) ORDER BY count DESC;";
		}
	}
	if ($key_type == "go_term") {
		$table_header = "<th>GO ID</th><th>GO Term</th><th>Count</th>";
		if ($key != '') {
			$query = "SELECT d.go_id, g.go_term, COUNT(d.go_id) as " .
				"\"count\" FROM Described_By d INNER JOIN " .
				"Gene_Ontology g ON g.go_id = d.go_id WHERE g.". $key_type 
				." = \"". $key . "\" GROUP BY(g.go_term);";
		}
		else {
			$query = "SELECT d.go_id, g.go_term, count(d.go_id) as " .
				"\"count\" FROM Described_By d INNER JOIN " .
				"Gene_Ontology g ON g.go_id = d.go_id GROUP BY(g.go_term);";
		}
	}
}
else if ($search_type = "occurences") {
	print("All occurences:");
	if ($key_type == "gene_symbol") {
		$table_header = "<th>Gene Symbol</th><th>Direction</th><th>Project</th>";
		if ($key != '') {
			$query = "SELECT gene_symbol, direction, project_id " .
				"FROM expression WHERE ". $key_type ." = \"". 
				$key . "\";";
		}
		else {
			$query = "SELECT gene_symbol, direction, project_id " .
				"FROM expression;";
		}
	}
	//specific search not working.
	if ($key_type == "pathway_name") {
		$table_header = "<th>Pathway ID</th><th>Pathway Name</th><th>Gene Symbol</th>";
		if ($key != '') {
			$query = "SELECT k.pathway_id, f.pathway_name, f.gene_symbol FROM Functions_In f INNER JOIN KEGG_Pathway ON f.pathway_name = k.pathway_id WHERE k.". $key_type ." = \"". $key . "\";";
		}
		else {
			$query = "SELECT k.pathway_id, k.pathway_name, " .
				"f.gene_symbol FROM Functions_In f INNER JOIN" .
				" KEGG_Pathway k ON f.pathway_name =" .
				" k.pathway_id;";
		}
	}
	if ($key_type == "go_term") {
		$table_header = "<th>GO ID</th><th>GO TERM</th><th>Project ID</th>";
		if ($key != '') {
			$query = "SELECT d.go_id, g.go_term, d.project_id FROM " .
				"Gene_Ontology g INNER JOIN Described_By d ON " .
				"d.go_id = g.go_id WHERE g.". $key_type . 
				" = \"" . $key . "\";";
		}
		else {
			$query = "SELECT d.go_id, g.go_term, d.project_id " .
				"FROM Described_By d INNER JOIN Gene_Ontology g" .
				" ON g.go_id = d.go_id;";
		}
	}
}

$result = mysqli_query($connect, $query) 
	or trigger_error("Query Failed! SQL: $query - Error: "
	. mysqli_error($connect), E_USER_ERROR);


/*If there are results from the query, print the
 * result relation.
 * If there are no results, print an error message.
 */
if ($result = mysqli_query($connect, $query)) {
	print("<table>");
	print("<tr>");
	print($table_header);
	print("</tr>");
	while ($row = mysqli_fetch_row($result)) {
	print("<tr>");	
	printf("<td>%s</td>", $row[0]); 
	printf("<td>%s</td>", $row[1]); 
	printf("<td>%s</td>", $row[2]);
	print("</tr>");
	}
	print("</table>");
    mysqli_free_result($result);
}else{
	echo "No results";
}

/*Always close your connection. 
 * Its a courtesy to your fellow users.
 */
mysqli_close($connect);
?> 
</body> 
</html>
