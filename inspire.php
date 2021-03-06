<!--  This is the inspirational advisory page which includes the recent advisories regarding the coronavirus provided by the government of India.
    -->

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

<!-- Here we are using internal style. This is used for decorating the table
    	which contains the inspirational advisories -->
    <style>
        	.styled-table {
    		border-collapse: collapse;
    		margin: 25px 0;
    		margin-left: auto;
  		margin-right: auto;
    		font-size: 0.9em;
    		font-family: sans-serif;
    		min-width: 400px;
    		box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
	}
	.styled-table thead tr {
    		background-color: #009879;
    		color: #ffffff;
    		text-align: left;
	}
	.styled-table th,
	.styled-table td {
    	padding: 12px 15px;
	}
	.styled-table tbody tr {
    		border-bottom: 1px solid #dddddd;
	}

	.styled-table tbody tr:nth-of-type(even) {
   	 	background-color: #f3f3f3;
	}

	.styled-table tbody tr:last-of-type {
    		border-bottom: 2px solid #009879;
	}
        .styled-table tbody tr.active-row {
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
        <li class="nav-item">
          <a class="nav-link" href="index.php">Home </a>
        </li>
        <li class="nav-item active">
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
        <img src="Images/inspirational.jpg"  class="image_center">
    </div>
    <br>
    <br>
    <!-- This table shows the inspirational advisories! -->
    <br>
     <h2 align="center">
    Inspirational Advisories
    </h2>
    <table class="styled-table">
    <tr>
    <th>Date</th>
    <th>Heading</th>
    <th>Link</th>
    </tr>
    <?php
 
 // mysqli_connect is used for connecting with the covid_19_database in the xampp mysql.
    $conn = mysqli_connect("localhost", "root", "", "covid_19_database");
    // Check connection
    if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);  
    }
    $sql = "SELECT Date, Heading, Link FROM Inspirational_advisories";
    
    $result = $conn->query($sql);
    
    if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
    echo "<tr><td>" . $row["Date"]. "</td><td>" . $row["Heading"] . "</td><td><a href = " . $row["Link"]. "> ". $row["Link"]. "</a></td> <td>";
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
