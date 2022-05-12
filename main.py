import requests
from bs4 import BeautifulSoup as Bs
from urllib.parse import unquote


class CountriesData:
    def __init__(self):
        self._country_list = self.get_countries_list()

    @staticmethod
    def get_countries_list():
        url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%' \
              'B0%D1%80%D1%81%D1%82%D0%B2'

        country_list = []
        temp_name_list = []

        url = unquote(url, encoding='utf-8')
        response = requests.get(url)
        html = Bs(response.content, 'html.parser')
        for block_html in html.select('tbody'):

            country_dict = {}
            for country_data in block_html.select('img, a'):
                attrs = country_data.attrs

                if attrs.get('href'):
                    if attrs.get('class'):
                        country_dict['full_name'] = attrs.get('title')
                        country_dict['sym_count'] = len(attrs.get('title'))
                    else:
                        temp_name_list.append(country_data.text)
                        country_dict['name'] = country_data.text
                        country_list.append(country_dict)
                        country_dict = {}
                else:
                    country_dict['image'] = attrs.get('src')[2:]

        for country_dict in country_list:
            country_dict['same_letter_count'] = len(
                [name for name in temp_name_list if name[0] == country_dict['name'][0]])

        return country_list

    def get_country_data(self, name: str):

        result = [dct for dct in self._country_list if dct.get('name').lower() == name.lower()]
        if not result:
            return {
                'name': '<not found>',
                'full_name': '<not found>',
                'sym_count': 0,
                'image': '',
                'same_letter_count': 0
            }
        else:
            return result[0]


countries_data = CountriesData()
country_data = countries_data.get_country_data(input('Country:'))
for key, val in country_data.items():
    print(f'{key.ljust(18)}:{val}')
print(country_data)