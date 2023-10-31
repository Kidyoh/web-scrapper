from flask import Flask, Response
from datetime import datetime

app = Flask(__name__)

current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%Y-%m-%d")




@app.route('/api/ethiojobs', methods=['GET'])
def get_data_ethiojobs():
    with open(f'scraped_data_ethiojobs_{formatted_date}.json', 'r') as json_file:
       data = json_file.read()
    return Response(data, content_type='application/json')


@app.route('/api/ezega', methods=['GET'])

def get_data_ezega():
    with open(f'scraped_data_ezega_{formatted_date}.json', 'r') as json_file:
       data = json_file.read()
    return Response(data, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
