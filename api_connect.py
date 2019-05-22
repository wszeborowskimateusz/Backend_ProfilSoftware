import requests
import urllib.request


class APIConnect:
    def __init__(self):
        self.API_URL = 'https://api.dane.gov.pl/resources/17363'

    def get_matura_file(self):
        response = requests.get(self.API_URL)

        if response.status_code != 200:
            return 0

        response_json = response.json()

        try:
            url = response_json['data']['attributes']['file_url']
        except KeyError:
            print('There was an error with json response')
            return 0

        try:
            response = urllib.request.urlopen(url)
        except ValueError:
            print('There was an error with file url in json response')
            return 0

        data = response.read()
        text = data.decode('ansi')

        return text

