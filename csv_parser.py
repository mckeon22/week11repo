import os

# Path to the CSV file
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

# Reading the file and handling potential format issues
try:
    with open(file_path, 'r') as file:
        lines = file.readlines()
except Exception as e:
    raise IOError(f"Error reading the file: {e}")

# Variables to store team scores and individual results
team_scores = []
individual_results = []

# Booleans to detect sections
in_team_scores = False
in_individual_results = False

# For loop to capture data sections
for line in lines:
    line = line.strip()

    if line.startswith("Place,Team,Score"):
        in_team_scores = True
        in_individual_results = False
        continue
    elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
        in_team_scores = False
        in_individual_results = True
        continue
    elif not line:  # Ignores empty lines
        continue

    data = line.split(',')

    # Validate CSV structure for teams and individuals and limit to top 3 results
    if in_team_scores and len(team_scores) < 3:
        if len(data) >= 3 and all(data[:3]):
            team_scores.append(data[:3])
        else:
            print(f"Warning: Incorrect or incomplete team score data: {line}")
    elif in_individual_results and len(individual_results) < 3:
        if len(data) >= 8 and all(data[:8]):
            individual_results.append(data[:8])
        else:
            print(f"Warning: Incorrect or incomplete individual result data: {line}")

# Report any issues if less than 3 entries are found
if len(team_scores) < 3:
    print("Warning: Less than 3 valid team scores found.")
if len(individual_results) < 3:
    print("Warning: Less than 3 valid individual results found.")

# HTML content to be constructed directly
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" type="text/css" href="css/reset.css"> 
    <link rel="stylesheet" href="css/style.css">
    <title>Client Project - Results</title>
</head>
<body>
    <header>
        <h1>Athlete Performance Tracker</h1>
    </header>
    <nav>
        <span class="hamburger">&#9776;</span> <!-- The hamburger icon -->
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="#">Men</a></li>
            <li><a href="#">Women</a></li>
            <li class="dropdown">
                <a href="#">Grade Level</a>
                <ul class="dropdown-content">
                    <li><a href="#"> 9</a></li>
                    <li><a href="#">10</a></li>
                    <li><a href="#"> 11</a></li>
                    <li><a href="#"> 12</a></li>
                </ul>
            </li>
            <li><a href="results.html">Event Results</a></li>
        </ul>
    </nav>
    <main id="content">
        <section id="event-title">
            <h2>Womens 5000 Meters Junior Varsity</h2>
        </section>
        
        <div id="theme-switcher-container">
    <div id="theme-switcher-label">Appearance</div>
    <div id="theme-switcher">
        <button id="light-mode-btn">Light Mode</button>
        <button id="dark-mode-btn">Dark Mode</button>
        <button id="high-contrast-btn">High Contrast</button>
    </div>
</div>

        <section id="team-scores">
            <h3>Team Scores</h3>
            <table>
                <thead>
                    <tr>
                        <th>Place</th>
                        <th>Team</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
"""

# Adds top 3 team scores to the HTML content
for score in team_scores:
    if len(score) >= 3:
        html_content += f"""
                    <tr>
                        <td>{score[0]}</td>
                        <td>{score[1]}</td>
                        <td>{score[2]}</td>
                    </tr>
        """

# Closes the team scores table tag
html_content += """
                </tbody>
            </table>
        </section>
        <section id="individual-results">
            <h2>Top 3 Results</h2>
            <div id="results-container">
"""

# Creates the HTML content for top 3 individual athletes with icons
for idx, result in enumerate(individual_results):
    if len(result) >= 7:  # Ensuring all required data is present
        athlete_link = result[3]
        try:
            athlete_id = athlete_link.split('/')[-2]
            image_path = f"images/{athlete_id}.jpg"
        except IndexError:
            image_path = "images/default.jpg"

        # Set styles for 1st, 2nd, and 3rd place
        place_class = ""
        if idx == 0:
            place_class = "first-place"
            medal_icon = '<i class="fas fa-medal" style="color: gold;"></i>'
        elif idx == 1:
            place_class = "second-place"
            medal_icon = '<i class="fas fa-medal" style="color: silver;"></i>'
        else:
            place_class = "third-place"
            medal_icon = '<i class="fas fa-medal" style="color: #CD7F32;"></i>'

        # Add the athlete's information along with the image path and icons to HTML
        html_content += f"""
            <div class="athlete {place_class}">
                <h3>{medal_icon} {result[2]}</h3>
                <p><i class="fas fa-trophy icon"></i> Place: {result[0]}</p>
                <p><i class="fas fa-graduation-cap icon"></i> Grade: {result[1]}</p>
                <p><i class="fas fa-stopwatch icon"></i> Time: {result[4]}</p>
                <p><i class="fas fa-users icon"></i> Team: {result[5]}</p>
                <img src="{image_path}" alt="Profile Picture of {result[2]}" width="150">
            </div>
        """

# Closing the individual results section and main content
html_content += """
            </div>
        </section>
    </main>
    <footer id="main-footer">
        <p>&copy; 2024 Client Project - All rights reserved.</p>
    </footer>

    <!-- Theme switcher JavaScript -->
    <script>
    // Get the buttons and listen for click events
    document.getElementById('light-mode-btn').addEventListener('click', () => {
        document.body.classList.remove('dark-mode', 'high-contrast-mode');
    });

    document.getElementById('dark-mode-btn').addEventListener('click', () => {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('high-contrast-mode');
    });

    document.getElementById('high-contrast-btn').addEventListener('click', () => {
        document.body.classList.add('high-contrast-mode');
        document.body.classList.remove('dark-mode');
    });
    </script>
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = 'results.html'
try:
    with open(html_file_path, 'w') as file:
        file.write(html_content)
    print(f'HTML file generated: {html_file_path}')
except Exception as e:
    raise IOError(f"Error writing to the file: {e}")