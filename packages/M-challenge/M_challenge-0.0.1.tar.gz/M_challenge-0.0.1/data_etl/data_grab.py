import json
from copy import deepcopy
import pandas as pd
import requests


class GetData:
    """
        This class is used to scrape world bank data in a json format. Data extracted is then transformed
        to a dataframe.

        class attributes:
            url (str): this specifies the API data is being extracted from.
            bank_data & bank_data: Empty lists to hold extracted data during processing.
        """

    def __init__(self):
        self.bank_data1 = []
        self.bank_data = []
        self.url = "http://api.worldbank.org/v2/country/?format=json&page="

    def extract_data(self):
        for i in range(1, 7):
            url = self.url + str(i)
            r = requests.get(url).json()
            self.bank_data.append(r)

    def clean_data(self):
        for item in self.bank_data:
            self.bank_data1.append(item[1])

    def write_to_json(self):
        with open('./world_bank.json', 'w') as f:
            json.dump(self.bank_data1, f, indent=4)

    def cross_join(self, left, right):
        """function to do a cartesian product"""
        new_rows = [] if right else left
        for left_row in left:
            for right_row in right:
                temp_row = deepcopy(left_row)
                for key, value in right_row.items():
                    temp_row[key] = value
                new_rows.append(deepcopy(temp_row))
        return new_rows

    def flatten_list(self, data):
        """function ensures JSON arrays are flattened. It uses a list of dictionaries comprising keys from one
        iteration before assigned to each of the list's values. """
        for elem in data:
            if isinstance(elem, list):
                yield from self.flatten_list(elem)
            else:
                yield elem

    def json_to_dataframe(self):
        def flatten_json(data, prev_heading=''):

            """Function will normalize deeply nested JSON."""

            if isinstance(data, dict):
                rows = [{}]
                for key, value in data.items():
                    rows = self.cross_join(rows, flatten_json(value, prev_heading + '.' + key))
            elif isinstance(data, list):
                rows = []
                for i in range(len(data)):
                    [rows.append(elem) for elem in self.flatten_list(flatten_json(data[i], prev_heading))]
            else:
                rows = [{prev_heading[1:]: data}]
            return rows

        self.extract_data()
        self.clean_data()
        self.write_to_json()
        world_bank_df = pd.DataFrame(flatten_json(self.bank_data1))

        return world_bank_df


if __name__ == '__main__':
    gd = GetData()
    gd.json_to_dataframe()
