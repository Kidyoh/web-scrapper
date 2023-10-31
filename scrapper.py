from flask import Flask, render_template, request, send_file
from bs4 import BeautifulSoup
import pandas as pd
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']

    # Perform web scraping using BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all HTML tags on the page
    all_tags = soup.find_all()

    return render_template('scrap_results.html', url=url, tags=all_tags)

from io import BytesIO

@app.route('/download/excel')
def download_excel():
    url = request.args.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_tags = soup.find_all()
    
    # Create a Pandas DataFrame from the scraped data
    data = [{'Tag': tag.name, 'Value': tag.text} for tag in all_tags]
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file (in memory using BytesIO)
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Set the position to the beginning of the buffer
    excel_data.seek(0)

    return send_file(excel_data, as_attachment=True, download_name="scraped_data.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.route('/download/csv')
def download_csv():
    url = request.args.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_tags = soup.find_all()
    
    # Create a Pandas DataFrame from the scraped data
    data = [{'Tag': tag.name, 'Value': tag.text} for tag in all_tags]
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file (in memory using BytesIO)
    csv_data = BytesIO()
    df.to_csv(csv_data, index=False)

    # Set the position to the beginning of the buffer
    csv_data.seek(0)

    return send_file(csv_data, as_attachment=True, download_name="scraped_data.csv", mimetype="text/csv")

if __name__ == '__main__':
    app.run(debug=True)
