from datetime import datetime

import requests
from typing import List
import numpy as np

DEFAULT_SRC = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"


class DataReader:
    def __init__(self, source=DEFAULT_SRC):
        # type: (str) -> None
        """
        Initializes dataset from specified url.
        :param source: optional, source to gather data from.
        """
        self.fetched_data = requests.get('https://opendata.ecdc.europa.eu/covid19/casedistribution/json/').json()['records']

    def get_country_data(self, country):
        # type: (str) -> CountryData
        """
        Generates country data from the previously loaded data source.
        :param country: 2-letter code for the desired country to obtain data from.
        :return: a CountryData object containing the desired country information.
        """
        data_points = list()
        for data_point in self.fetched_data:
            if data_point['geoId'] == country:
                data_points.append(DataPoint(data_point))
        data_points.sort(key=DataPoint.get_date, reverse=False)
        return CountryData(country, data_points)


FORMAT_STR = '%d/%m/%Y'


class DataPoint:
    def __init__(self, info):
        # type: (dict) -> None
        self.date = datetime.strptime(info['dateRep'], FORMAT_STR)
        self.cases = int(info['cases'])
        self.deaths = int(info['deaths'])
        self.pop_size = info['popData2018']

    def get_date(self):
        return self.date

    def __str__(self):
        return self.date.date()


class CountryData:
    def __init__(self, country, data_points):
        # type: (str, List[DataPoint]) -> None
        self.name = country
        self.data_points = data_points
        self.pop_size = data_points[0].pop_size if len(data_points) > 0 else 0

    def get_deaths(self):
        deaths = np.zeros(len(self.data_points))
        for i, data_point in enumerate(self.data_points):
            deaths[i] = data_point.deaths
        return deaths

    def get_cases(self, acc=False):
        # type:(bool) -> np.ndarray
        """
        Returns cases for a country, in a ndarray fashion.
        :param acc: boolean when set to true, returns the accumulated cases.
        :return: numpy ndarray containing the reported cases.
        """
        cases = np.zeros(len(self.data_points), dtype=float)
        if not acc:
            for i, data_point in enumerate(self.data_points):
                cases[i] = float(data_point.cases)
        else:
            for i, data_point in enumerate(self.data_points):
                cases[i] = float(data_point.cases) + cases[i-1] if i > 0 else float(data_point.cases)
        return cases

    def calculate_first_day(self):
        for i, data_point in enumerate(self.data_points):
            if data_point.cases > 0:
                return i

    def get_growth_rate(self, array):
        first_day = self.calculate_first_day()
        aux_arr = array
        accumulated_rate = np.zeros(len(array))
        print("Array", aux_arr)
        for i, data_point in enumerate(aux_arr):
            if i < first_day:
                accumulated_rate[i] = 0.0
            elif i == first_day:
                accumulated_rate[i] = float(data_point)
            else:
                accumulated_rate[i] = data_point / accumulated_rate[i-1]
        return accumulated_rate

    def get_dates(self):
        return [i.date for i in self.data_points]


# Test
if __name__ == "__main__":
    data = DataReader("MX")
    mx = data.get_country_data("MX")
    for d in mx.data_points:
        print(d.deaths)
