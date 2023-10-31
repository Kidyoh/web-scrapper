import os
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

def save_data_to_json(data):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    json_filename = f'scraped_data_ethiojobs_{formatted_date}.json'

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

def delete_old_json_files():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    files = os.listdir()

    for file in files:
        if file.startswith('scraped_data_ethiojobs_') and file.endswith('.json'):
            date_in_filename = file.split('_')[3].split('.')[0]
            if date_in_filename != current_date:
                os.remove(file)

def get_number_of_jobs():
    url = "https://www.ethiojobs.net/search-results-jobs/?searchId=1698308799.1268&action=search&listings_per_page=100&view=list"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    h1_element = soup.find('h1', class_='no-margin')
    
    if h1_element:
        span_element = h1_element.find('span', class_='pull-left sp-right')
        if span_element:
            number_of_jobs = int(span_element.text.strip())
            return number_of_jobs
    
    return 500

def scrape_ethioJobs():
    delete_old_json_files()
    number_of_jobs = get_number_of_jobs()

    url = f"https://www.ethiojobs.net/search-results-jobs/?searchId=1698308799.1268&action=search&listings_per_page={number_of_jobs}&view=list"
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    job_postings = soup.find_all('tr', class_='evenrow') + soup.find_all('tr', class_='oddrow')

    data = []
    
    for job_posting in job_postings:
        job_title_element = job_posting.find('a', title='View Job')
        job_title = job_title_element.text.strip()
        job_url = job_title_element['href']
        company_name = job_posting.find('a', class_='company-name').text.strip()
        posted_date = job_posting.find('span', class_='captions-field').text.strip()
        scope_of_work = job_posting.find('div', class_='show-brief').text.strip()

        data.append({
            'Job Title': job_title,
            'Job URL': job_url,
            'Company Name': company_name,
            'Posted Date': posted_date,
            'Scope of Work': scope_of_work
        })

    save_data_to_json(data)

    return data

if __name__ == '__main__':
    scrape_ethioJobs()
