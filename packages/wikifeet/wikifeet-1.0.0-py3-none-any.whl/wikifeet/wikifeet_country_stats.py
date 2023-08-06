# Copyright 2021 XXIV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import http.client as client
import json as json_object
import re

PATTERN_ROMAN_FEET = r"\[\"Country\", \"Favor longer second toe\"\],(.*?\s*\s])"
PATTERN_FOOT_TATTOOS = r"\[\"Country\", \"Favor foot tattoos\"\],(.*?\s*\s])"
PATTERN_PAINTED_TOES = r"\[\"Country\", \"Favor painted toes\"\],(.*?\s*\s])"
PATTERN_SECRET_FEET_LOVER = r"\[\"Country\", \"Keep it secret\"\],(.*?\s*\s])"


def http(modelUrl):
    try:
        conn = client.HTTPSConnection('www.wikifeet.com')
        conn.request('GET', modelUrl)
        data = conn.getresponse().read().decode('UTF-8')
        conn.close()
        return data
    except:
        return None


def json(info, key):
    try:
        data = json_object.loads(country(info))
        if data is not None:
            if data[key] is not None:
                return data[key]
            else:
                return None
        else:
            return None
    except:
        return None


def country(info):
    try:
        array = json_object.loads(info)['country']
        data = {}
        for i in array:
            name = i[0]
            value = i[1]['f']
            data[name.upper()] = value
        return json_object.dumps(data)
    except:
        return None


def roman_feet_info():
    url = http('/polls/1')
    if url is not None:
        matcher = re.search(PATTERN_ROMAN_FEET, url)
        if matcher:
            return f"{{\"country\":[{matcher.group(1)}}}"
        else:
            return None
    else:
        return None


def foot_tattoos_info():
    url = http('/polls/2')
    if url is not None:
        matcher = re.search(PATTERN_FOOT_TATTOOS, url)
        if matcher:
            return f"{{\"country\":[{matcher.group(1)}}}"
        else:
            return None
    else:
        return None


def painted_toes_info():
    url = http('/polls/3')
    if url is not None:
        matcher = re.search(PATTERN_PAINTED_TOES, url)
        if matcher:
            return f"{{\"country\":[{matcher.group(1)}}}"
        else:
            return None
    else:
        return None


def secret_feet_lover_info():
    url = http('/polls/4')
    if url is not None:
        matcher = re.search(PATTERN_SECRET_FEET_LOVER, url)
        if matcher:
            return f"{{\"country\":[{matcher.group(1)}}}"
        else:
            return None
    else:
        return None


class WikiFeetCountryStats:
    """
    Gets WikiFeet stats by country.
    """

    def __init__(self, country_name: str):
        """
        Initialize WikiFeetCountryStats.

        :param country_name: The name of the country.
        """
        self.__country_name = country_name

    def roman_feet(self):
        """
        Gets roman feet stats.

        :returns: Stats of the people who like roman feet.
        """
        data = json(roman_feet_info(), self.__country_name.upper())
        if data is not None:
            return data
        else:
            return None

    def foot_tattoos(self):
        """
        Gets foot tattoos stats.

        :returns: Stats of the people who like foot tattoos.
        """
        data = json(foot_tattoos_info(), self.__country_name.upper())
        if data is not None:
            return data
        else:
            return None

    def painted_toes(self):
        """
        Gets painted toes stats.

        :returns: Stats of the people who like painted toes.
        """
        data = json(painted_toes_info(), self.__country_name.upper())
        if data is not None:
            return data
        else:
            return None

    def secret_feet_lover(self):
        """
        Gets secret feet lover stats.

        :returns: Stats of the people who like feet and keep it secret.
        """
        data = json(secret_feet_lover_info(), self.__country_name.upper())
        if data is not None:
            return data
        else:
            return None
