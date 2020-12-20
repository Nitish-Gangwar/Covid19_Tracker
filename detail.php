<!doctype html>
<html lang="en"> 
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

    <title>COVID-19 Tracker</title>
    <link rel="stylesheet" href="style.css">
    <script src="districts.js"></script>

    <style>
        	.styled-table1 {
    		border-collapse: collapse;
    		margin: 25px 0;
    		margin-left: auto;
  		margin-right: auto;
    		font-size: 0.9em;
    		font-family: sans-serif;
    		min-width: 600px;
    		box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
	}
	
	.styled-table1 thead tr {
    		background-color: #009879;
    		color: #ffffff;
    		text-align: center;
	}
	.styled-table1 th,
	.styled-table1 td {
    	padding: 12px 0px;
    	text-align: center;
	}
	.styled-table1 tbody tr {
    		border-bottom: 1px solid #dddddd;
	}

	.styled-table1 tbody tr:nth-of-type(even) {
   	 	background-color: #f3f3f3;
	}

	.styled-table1 tbody tr:last-of-type {
    		border-bottom: 2px solid #009879;
	}
        .styled-table1 tbody tr.active-row {
    		font-weight: bold;
    		color: #009879;
	}
	
	.styled-table2 {
    		border-collapse: collapse;
    		margin: 25px 0;
    		margin-left: auto;
  		margin-right: auto;
    		font-size: 0.9em;
    		font-family: sans-serif;
    		min-width: 400px;
    		box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
	}
	
	.styled-table2 thead tr {
    		background-color: #009879;
    		color: #ffffff;
    		text-align: center;
	}
	.styled-table2 th,
	.styled-table2 td {
    	padding: 12px 15px;
    	text-align: center;
	}
	.styled-table2 tbody tr {
    		border-bottom: 1px solid #dddddd;
	}

	.styled-table2 tbody tr:nth-of-type(even) {
   	 	background-color: #f3f3f3;
	}

	.styled-table2 tbody tr:last-of-type {
    		border-bottom: 2px solid #009879;
	}
        .styled-table2 tbody tr.active-row {
    		font-weight: bold;
    		color: #009879;
	}

    	</style>

  </head>

  <body>
    <nav class="navbar navbar-light navbar-expand-lg" style="background-color: #66b3ff;">
    <img class="logo" src="Images/logo.png"  width="80">

    <a class="navbar-brand" href="index.php">COVID-19 Tracker</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText">
        <span class="navbar-toggler-icon"></span>
      </button>

    <div class="collapse navbar-collapse" id="navbarText">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a class="nav-link" href="index.php">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="advisory.php">General Advisories</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="travel.php">Travel Alert</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="hospital.php">Hospital Alert</a>
        </li>

        <li class="nav-item">
          <a class="nav-link" href="paper.php">Recent Research</a>
        </li>
      </ul>
    
      </div>
    </nav>
    <br>
    <br>
    <div>
        <img src="Images/corona.jpg"  class="image_center">
    </div>
    <br>
    <br>
    <table class="styled-table1">
     	<thead>
    	<tr>
    	<th>State</th>
    	<th>Total Cases</th>
    	<th>Total Cured</th>
    	<th>Total Deaths</th>
    	</tr>
    	</thead>
    	<?php
        session_start();
        $string = $_SESSION['state'];
        $district = $_SESSION['district'];

    	$conn = mysqli_connect("localhost", "root", "", "covid_19_database");
    // Check connection
    	if ($conn->connect_error) {
    		die("Connection failed: " . $conn->connect_error);  
    	}
    	$sql = "SELECT SUM(Cases), SUM(Cured), SUM(Deaths) FROM $string";
    	$result = $conn->query($sql);
    
    	if ($result->num_rows > 0) {
    	// output data of each row
    	while($row = $result->fetch_assoc()) {
    	echo "<tr><td>$string</td><td>" . $row["SUM(Cases)"]. "</td><td>" . $row["SUM(Cured)"] . "</td><td>"
           . $row["SUM(Deaths)"]. "</td><td>";
    	}
    	echo "</table>";
    	} else { echo "0 results"; }
    	$conn->close();
    	?>
   	 </table>   
   	 
    <!--  ****    BOXES TO SHOW THE TOTAL COUNTS OF INDIA, (TOTAL INFECTED, RECOVERED, DEAD) -->
    <br>
      
    <table class="styled-table2">
    <tr>
    <th>Districts</th>
    <th>Cases</th>
    <th>Increased Cases</th>
    <th>Cured</th>
    <th>Cured and Sent</th>
    <th>Active</th>
    <th>Deaths</th>
    <th>Deaths Today</th>
    </tr>
    <?php
    $string = $_SESSION['state'];
    $conn = mysqli_connect("localhost", "root", "", "covid_19_database");
    // Check connection
    if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);  
    }
    if ($district)
    {
    $sql = "SELECT Name, Cases, Increased_cases,Cured, Cured_and_Sent, Active, Deaths, Deaths_Today FROM $string Where Name='$district'";
    }
    else{
    $sql = "SELECT Name, Cases, Increased_cases,Cured, Cured_and_Sent, Active, Deaths, Deaths_Today FROM $string";
    }
    $result = $conn->query($sql);
    
    if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
    echo "<tr><td>" . $row["Name"]. "</td><td>" . $row["Cases"] . "</td><td>"
. $row["Increased_cases"]. "</td><td>" . $row["Cured"] .  "</td><td>" . $row["Cured_and_Sent"] .  "</td><td>" . $row["Active"] . "</td><td>" . $row["Deaths"] .  "</td><td>" . $row["Deaths_Today"] . "</td></tr>";
    }
    echo "</table>";
    } else { echo "0 results"; }
    $conn->close();
    ?>
    </table>

    <br>
       <footer>
        	<span>Developed By: <br><br>TwistingTornadoes</span>
        </footer>

    </body>
</html>
