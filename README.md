# Website Monitoring Tool

![Website Monitoring Tool](https://placeimg.com/640/480/tech)

A simple Flask web application for monitoring website uptime, page speed, and performing login transactions. It also includes a basic analytics dashboard for viewing historical performance data.

## Features
- Website uptime monitoring
- Page speed monitoring
- Transaction monitoring (e.g., login transactions)
- Alerting/notification system
- Historical performance data and analytics

## Goal
The goal of this project is to create a free and open-source alternative to paid website monitoring services like Pingdom. By providing essential monitoring features and analytics in a lightweight and customizable package, this tool aims to empower individuals and small businesses to monitor their website performance effectively without the need for expensive subscription services.

## Instructions

### Prerequisites
- Python 3.x
- SQLite (for storing performance data)

### Installation
1. Clone this repository to your local machine.
2. Navigate to the project directory.

### Set Up SQLite Database
1. Create a SQLite database file named `performance.db` in the project directory.
2. Run the following SQL commands to create the `performance_data` table:

    ```sql
    CREATE TABLE performance_data (
        id INTEGER PRIMARY KEY,
        timestamp INTEGER NOT NULL,
        url TEXT NOT NULL,
        status INTEGER NOT NULL,
        load_time REAL
    );
    ```

### Usage
1. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the Flask web application:

    ```bash
    python app.py
    ```

3. Access the application in your web browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

4. Enter a website URL, choose monitoring options, and click the "Check" button to monitor website performance.

## Credits
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [SQLite](https://www.sqlite.org/) - Embedded database engine

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
