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
import re

PATTERN_ROMAN_FEET = r"Liked Roman / Egyptian feet better(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_GREEK_FEET = r"Liked Greek feet / Morton's toe better(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_NOT_FOOT_TATTOOS = r"I Don't like foot tattoos(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_MAYBE_FOOT_TATTOOS = r"I Sometimes like foot tattoos(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_FOOT_TATTOOS = r"I Like foot tattoos(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_NATURAL_TOES = r"I like natural toes better(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_PAINTED_TOES = r"I like painted toes better(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_SECRET_FEET_LOVER = r"No, I keep it to myself(.*?) width:(.*?)%'>(.*?)</div></td></tr>"
PATTERN_OPEN_FEET_LOVER = r"Yes, I am open about it(.*?) width:(.*?)%'>(.*?)</div></td></tr>"


def http(modelUrl):
    try:
        conn = client.HTTPSConnection('www.wikifeet.com')
        conn.request('GET', modelUrl)
        data = conn.getresponse().read().decode('UTF-8')
        conn.close()
        return data
    except:
        return None


class WikiFeetStats:
    """
    Gets WikiFeet stats.
    """

    def roman_feet(self):
        """
        Gets roman feet stats.

        :returns: Stats of the people who like roman feet.
        """
        url = http('/polls/1')
        if url is not None:
            matcher = re.search(PATTERN_ROMAN_FEET, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None

    def greek_feet(self):
        """
        Gets greek feet stats.

        :returns: Stats of the people who like greek feet.
        """
        url = http('/polls/1')
        if url is not None:
            matcher = re.search(PATTERN_GREEK_FEET, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None

    def not_foot_tattoos(self):
        """
        Gets foot tattoos stats.

        :returns: Stats of the people who don't like foot tattoos.
        """
        url = http('/polls/2')
        if url is not None:
            matcher = re.search(PATTERN_NOT_FOOT_TATTOOS, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None

    def maybe_foot_tattoos(self):
        """
        Gets foot tattoos stats.

        :returns: Stats of the people who sometimes like foot tattoos.
        """
        url = http('/polls/2')
        if url is not None:
            matcher = re.search(PATTERN_MAYBE_FOOT_TATTOOS, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return

    def foot_tattoos(self):
        """
        Gets foot tattoos stats.

        :returns: Stats of the people who like foot tattoos.
        """
        url = http('/polls/2')
        if url is not None:
            matcher = re.search(PATTERN_FOOT_TATTOOS, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None

    def natural_toes(self):
        """
        Gets natural toes stats.

        :returns: Stats of the people who like natural toes.
        """
        url = http('/polls/3')
        if url is not None:
            matcher = re.search(PATTERN_NATURAL_TOES, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None

    def painted_toes(self):
        """
        Gets painted toes stats.

        :returns: Stats of the people who like painted toes.
        """
        url = http('/polls/3')
        if url is not None:
            matcher = re.search(PATTERN_PAINTED_TOES, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None

    def secret_feet_lover(self):
        """
        Gets secret feet lover stats.

        :returns: Stats of the people who like feet and keep it secret.
        """
        url = http('/polls/4')
        if url is not None:
            matcher = re.search(PATTERN_SECRET_FEET_LOVER, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None

    def open_feet_lover(self):
        """
        Gets open feet lover stats

        :returns: Stats of the people who like feet and open about it.
        """
        url = http('/polls/4')
        if url is not None:
            matcher = re.search(PATTERN_OPEN_FEET_LOVER, url)
            if matcher:
                return matcher.group(3)
            else:
                return None
        else:
            return None
