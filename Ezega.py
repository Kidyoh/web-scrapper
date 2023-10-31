import os
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

def save_data_to_json(data, source):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    json_filename = f'scraped_data_{source}_{formatted_date}.json'

    try:
        with open(json_filename, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    for item in data:
        if item not in existing_data:
            existing_data.append(item)

    with open(json_filename, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def scrape_ezega():
    url = "https://www.ezega.com/jobs/AllPostedJobs"

    # Set the User-Agent to mimic a web browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the job postings
    job_postings = soup.find_all('li')

    # Initialize an empty list to store the scraped data
    data = []
    
    # Loop through each job posting and extract the relevant information
    for job_posting in job_postings:

        if job_posting.find_parent('ul', class_='menu clearfix') or job_posting.find_parent('div', class_='footer-container'):
           continue

        job_title_element = job_posting.find('a')
        if job_title_element is not None:
            job_title = job_title_element.text.strip()
        else:
            job_title = ''
        if job_title_element is not None:
          job_url = 'https://www.ezega.com' + job_title_element['href']
        else:
          job_url = ''
        company_name_elements = job_posting.find_all('div', class_='col-xs-12 col-sm-4')
        if len(company_name_elements) > 1:
            company_name = company_name_elements[1].text.strip()
        else:
            company_name = ''
        posted_date_element = job_posting.find('div', class_='col-xs-12 col-sm-2')
        if posted_date_element is not None:
            posted_date = posted_date_element.text.strip()
        else:
            posted_date = ''
        location_elements = job_posting.find_all('div', class_='col-xs-12 col-sm-2')
        if len(location_elements) > 1:
            location = location_elements[1].text.strip()
        else:
            location = ''

        # Add the extracted information to the list
        data.append({
            'Job Title': job_title,
            'Job URL': job_url,
            'Company Name': company_name,
            'Posted Date': posted_date,
            'Location': location
        })
    
    # Save the scraped data to the JSON file (updating the file if it exists)
    save_data_to_json(data, 'ezega')

    return data

if __name__ == '__main__':
    scrape_ezega()
