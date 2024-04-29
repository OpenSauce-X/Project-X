from flask import Flask, render_template, request, send_from_directory
import requests
import time
import sqlite3
import smtplib
import logging
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
from flask import redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
import datetime


app = Flask(__name__)

def append_http(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url  # Add 'http://' if schema is missing
    return url

def check_website(url):
    url = append_http(url)
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def perform_login_transaction(url):
    url = append_http(url)
    try:
        login_data = {'username': 'your_username', 'password': 'your_password'}
        response = requests.post(url, data=login_data)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def send_email_notification(subject, message, recipient_email):
    sender_email = 'your_email@example.com'
    password = 'your_password'

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP_SSL('smtp.example.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email notification sent successfully.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email notification: {e}")
    finally:
        server.quit()

def log_performance_data(url, status, load_time):
    url = append_http(url)
    try:
        timestamp = int(time.time())
        conn = sqlite3.connect('performance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO performance_data (timestamp, url, status, load_time) VALUES (?, ?, ?, ?)", (timestamp, url, status, load_time))
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

# Configure logging
logging.basicConfig(filename='monitoring.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def monitor_website(website_url, measure_speed, login_transaction):
    status = check_website(website_url)
    page_load_time = None
    transaction_status = None

    if measure_speed:
        start_time = time.time()
        response = requests.get(website_url)
        end_time = time.time()
        page_load_time = end_time - start_time
        logging.info(f"Pinged website {website_url} at {datetime.datetime.now()} with page load time: {page_load_time} seconds")

    if login_transaction:
        transaction_status = perform_login_transaction(website_url)
        logging.info(f"Performed login transaction on website {website_url} at {datetime.datetime.now()}, transaction status: {transaction_status}")

    log_performance_data(website_url, status, page_load_time)

    if not status:
        send_email_notification("Website Down Alert", f"The website {website_url} is down. Please take immediate action.", "recipient@example.com")
        logging.warning(f"Website {website_url} is down at {datetime.datetime.now()}")

# Initialize BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()

DEFAULT_INTERVAL = 30

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website_url = request.form['website_url']
        website_url = append_http(website_url)  # Ensure URL has schema before using it
        try:
            time_interval = int(request.form['time_interval'])
        except KeyError:
            # Handle the case where 'time_interval' is missing
            # Set a default time interval value or display an error message
            time_interval = DEFAULT_INTERVAL  # Set a default value
        measure_speed = 'measure_speed' in request.form
        login_transaction = 'login_transaction' in request.form
        status = check_website(website_url)
        
         # Schedule website monitoring task
        scheduler.add_job(monitor_website, 'interval', minutes=time_interval, args=[website_url, measure_speed, login_transaction])
        
        page_load_time = None
        transaction_status = None
        if measure_speed:
            start_time = time.time()
            response = requests.get(website_url)
            end_time = time.time()
            page_load_time = end_time - start_time
        if login_transaction:
            transaction_status = perform_login_transaction(website_url)
        log_performance_data(website_url, status, page_load_time)
        if not status:
            send_email_notification("Website Down Alert", f"The website {website_url} is down. Please take immediate action.", "recipient@example.com")
        return render_template('index.html', website_url=website_url, status=status, page_load_time=page_load_time, measure_speed=measure_speed, transaction_status=transaction_status)
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('performance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, status, load_time FROM performance_data")
    data = cursor.fetchall()
    conn.close()

    timestamps = [row[0] for row in data]
    statuses = [row[1] for row in data]
    load_times = [row[2] for row in data]

    # Plot uptime status over time
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, statuses, marker='o', linestyle='-')
    plt.title('Website Uptime Status Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Status (1=UP, 0=DOWN)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/uptime_status.png')

    # Plot page load time over time
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, load_times, marker='o', linestyle='-')
    plt.title('Page Load Time Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Page Load Time (seconds)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/page_load_time.png')

    return render_template('analytics.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
