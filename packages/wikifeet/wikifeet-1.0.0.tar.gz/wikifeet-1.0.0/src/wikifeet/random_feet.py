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
import random
import re

PATTERN_MODEL_INFO = r"Random wikiFeet gallery(.*?)<a href='/(.*?)'><div>"
PATTERN_RATING_INFO = r"width:100%'>(.*?)<br><span style='color:#abc'>(.*?)</span>"
PATTERN_ID = r"messanger\['gdata'\] \= (\[.*?\]);"
PATTERN_SHOE_SIZE = r"id=ssize_label>(.*?)<a"
PATTERN_BIRTH_PLACE = r"id=nation_label>(.*?)<a"
PATTERN_BIRTH_DATE = r"id=bdate_label>(.*?)<a"
PATTERN_RATING = r"white-space:nowrap' >&nbsp;\((.*?) feet\)</div>"
PATTERN_RATING_STATS = r"Feet rating stats \((.*?) (.*?)<br>"
PATTERN_RATING_GORGEOUS = r"Rating(.*?)&nbsp;\((.*?) feet\)</div>"
PATTERN_IMDB = r"www.imdb.com/(.*?)'(.*?)Go to IMDb page"


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
        data = json_object.loads(info)
        if data is not None:
            if data[key] is not None:
                return data[key]
            else:
                return None
        else:
            return None
    except:
        return None


def model_info():
    try:
        url = http("/")
        if url is not None:
            matcher = re.search(PATTERN_MODEL_INFO, url)
            if matcher:
                model_name = re.sub(r'_| ', ' ', matcher.group(2))
                model_username = re.sub(r'_| ', '-', matcher.group(2))
                model_url = f'https://www.wikifeet.com/{matcher.group(2)}'
                return f'{{"name": "{model_name}", "username": "{model_username}", "url": "{model_url}"}}'
            else:
                return None
        else:
            return None
    except:
        return None


class RandomFeet:
    """
    Gets random model.
    """

    def __init__(self):
        """
        Initialize RandomFeet.
        """
        self.__model_info = model_info()

    def __rating_info(self):
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                collection = re.findall(PATTERN_RATING_INFO, url)
                data = {}
                for matcher in collection:
                    data[matcher[1]] = matcher[0]
                json_data = json_object.dumps(data)
                return json_data
            else:
                return None
        else:
            return None

    def __id(self):
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                matcher = re.search(PATTERN_ID, url)
                if matcher:
                    collection = json_object.loads(matcher.group(1))
                    data_list = []
                    for i in collection:
                        data_list.append(i['pid'])
                    return random.choice(data_list)
                else:
                    return None
            else:
                return None
        else:
            return None

    def model_name(self):
        """
        Gets the name of the model.

        :returns: The name of the model.
        """
        data = json(self.__model_info, "name")
        if data is not None:
            return data
        else:
            return None

    def model_page(self):
        """
        Gets the page of the model.

        :returns: The page of the model.
        """
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                return data_url
            else:
                return None
        else:
            return None

    def thumbnail(self):
        """
        Gets thumbnail of the model.

        :returns: Random thumbnail of the model.
        """
        if self.__id() is not None:
            return f'https://thumbs.wikifeet.com/{self.__id()}.jpg'
        else:
            return None

    def image(self):
        """
        Gets image of the model.

        :returns: Random image of the model.
        """
        data = json(self.__model_info, "username")
        if self.__id() is not None and data is not None:
            return f'https://pics.wikifeet.com/{data}-feet-{self.__id()}.jpg'
        else:
            return None

    def shoe_size(self):
        """
        Gets shoe size of the model.

        :returns: The shoe size of the model.
        """
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                matcher = re.search(PATTERN_SHOE_SIZE, url)
                if matcher:
                    return matcher.group(1)
                else:
                    return None
            else:
                return None
        else:
            return None

    def birth_place(self):
        """
        Gets the birthplace of the model.

        :returns: The birthplace of the model.
        """
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                matcher = re.search(PATTERN_BIRTH_PLACE, url)
                if matcher:
                    return matcher.group(1)
                else:
                    return None
            else:
                return None
        else:
            return None

    def birth_date(self):
        """
        Gets the birthdate of the model.

        :returns: The birthdate of the model.
        """
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                matcher = re.search(PATTERN_BIRTH_DATE, url)
                if matcher:
                    return matcher.group(1)
                else:
                    return None
            else:
                return None
        else:
            return None

    def rating(self):
        """
        Gets the rating of the model.

        :returns: The rating of the model.
        """
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                matcher = re.search(PATTERN_RATING, url)
                matcher_gorgeous = re.search(PATTERN_RATING_GORGEOUS, url)
                if matcher:
                    return matcher.group(1)
                elif matcher_gorgeous:
                    return matcher_gorgeous.group(2)
                else:
                    return None
            else:
                return None
        else:
            return None

    def beautiful_rating(self):
        """
        Gets the beautiful rating of the model.

        :returns: The beautiful rating of the model.
        """
        data = json(self.__rating_info(), "beautiful")
        if data is not None:
            return data
        else:
            return None

    def nice_rating(self):
        """
        Gets the nice rating of the model.

        :returns: The nice rating of the model.
        """
        data = json(self.__rating_info(), "nice")
        if data is not None:
            return data
        else:
            return None

    def ok_rating(self):
        """
        Gets the ok rating of the model.

        :returns: The ok rating of the model.
        """
        data = json(self.__rating_info(), "ok")
        if data is not None:
            return data
        else:
            return None

    def bad_rating(self):
        """
        Gets the bad rating of the model.

        :returns: The bad rating of the model.
        """
        data = json(self.__rating_info(), "bad")
        if data is not None:
            return data
        else:
            return None

    def ugly_rating(self):
        """
        Gets the ugly rating of the model.

        :returns: The ugly rating of the model.
        """
        data = json(self.__rating_info(), "ugly")
        if data is not None:
            return data
        else:
            return None

    def rating_stats(self):
        """
        Gets the rating stats of the model.

        :returns: The rating stats of the model.
        """
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                matcher = re.search(PATTERN_RATING_STATS, url)
                if matcher:
                    return matcher.group(1)
                else:
                    return None
            else:
                return None
        else:
            return None

    def imdb_page(self):
        """
        Gets the imdb page of the model.

        :returns: The imdb page of the model.
        """
        data_url = json(self.__model_info, "url")
        data_name = json(self.__model_info, "name")
        if data_url is not None and data_name is not None:
            url = http(re.sub('https://www.wikifeet.com', '', data_url))
            if url is not None:
                matcher = re.search(PATTERN_IMDB, url)
                if matcher:
                    return f'https://www.imdb.com/{matcher.group(1)}'
                else:
                    return None
            else:
                return None
        else:
            return None
