<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATTENDANCE-PROGRAMM</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            font-size: 2.5em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            font-size: 1.8em;
            margin-top: 20px;
        }
        p {
            margin: 10px 0;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            padding: 8px 0;
            position: relative;
        }
        li::before {
            content: "✔";
            color: #27ae60;
            margin-right: 10px;
        }
        code {
            background-color: #ecf0f1;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
        }
        pre {
            background-color: #2c3e50;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .section {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .highlight {
            background-color: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>ATTENDANCE-PROGRAMM</h1>
    <div class="section">
        <h2>Overview</h2>
        <p>
            ATTENDANCE-PROGRAMM is a powerful tool for managing and analyzing student attendance data. Designed for educational institutions, it tracks attendance and provides advanced statistical insights through probability distributions and visualizations.
        </p>
    </div>

    <div class="section">
        <h2>Features</h2>
        <ul>
            <li><strong>Attendance Tracking:</strong> Record and manage daily student attendance with ease.</li>
            <li><strong>Probability Distribution Analysis:</strong> Calculate the likelihood of students attending or missing classes.</li>
            <li><strong>Distribution Polygons:</strong> Visualize attendance patterns using frequency polygons.</li>
            <li><strong>Student Similarity Analysis:</strong> Compute similarity probabilities between students based on attendance behavior.</li>
            <li><strong>Statistical Reports:</strong> Generate detailed summaries of attendance trends.</li>
        </ul>
    </div>

    <div class="highlight">
        <h2>New Functionalities</h2>
        <p>Recent updates have introduced advanced statistical tools to enhance attendance analysis:</p>
        <ul>
            <li><strong>Attendance Probability Distribution:</strong> Analyze the probability of student attendance, revealing consistency patterns.</li>
            <li><strong>Distribution Polygons:</strong> Create visual representations of attendance frequency and distribution.</li>
            <li><strong>Student Similarity Probabilities:</strong> Identify students with similar attendance behaviors for targeted insights.</li>
        </ul>
    </div>

    <div class="section">
        <h2>Installation</h2>
        <p>Follow these steps to set up the project:</p>
        <ol>
            <li>Clone the repository:
                <pre><code>git clone https://github.com/bekfurr/ATTENDANCE-PROGRAMM.git</code></pre>
            </li>
            <li>Navigate to the project directory:
                <pre><code>cd ATTENDANCE-PROGRAMM</code></pre>
            </li>
            <li>Install dependencies:
                <pre><code>pip install -r requirements.txt</code></pre>
            </li>
        </ol>
    </div>

    <div class="section">
        <h2>Usage</h2>
        <p>Run the program and explore its features:</p>
        <ol>
            <li>Start the program:
                <pre><code>python main.py</code></pre>
            </li>
            <li>Input attendance data or load from a file (e.g., CSV).</li>
            <li>Access statistical tools via the menu to generate distributions, polygons, or similarity reports.</li>
            <li>View results in the console or as exported visualizations.</li>
        </ol>
        <p>Example code for probability distribution:</p>
        <pre><code>from attendance_stats import calculate_probability_distribution
data = load_attendance_data("attendance.csv")
dist = calculate_probability_distribution(data)
plot_distribution_polygon(dist)</code></pre>
    </div>

    <div class="section">
        <h2>Contributing</h2>
        <p>Contributions are welcome! To contribute:</p>
        <ol>
            <li>Fork the repository.</li>
            <li>Create a new branch (<code>git checkout -b feature-branch</code>).</li>
            <li>Commit your changes (<code>git commit -m 'Add new feature'</code>).</li>
            <li>Push to the branch (<code>git push origin feature-branch</code>).</li>
            <li>Open a pull request.</li>
        </ol>
    </div>

    <div class="section">
        <h2>License</h2>
        <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>
    </div>

    <div class="section">
        <h2>Contact</h2>
        <p>For questions or feedback, reach out to <a href="https://github.com/bekfurr">bekfurr</a>.</p>
    </div>
</body>
</html>
