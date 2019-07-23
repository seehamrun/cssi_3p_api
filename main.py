# Copyright 2016 Google Inc.
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

import webapp2
from google.appengine.api import urlfetch
import json
import jinja2
import os
import api_key

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def getSunriseTimes(city):
    headers = {
        "X-RapidAPI-Host": "sun.p.rapidapi.com",
        "X-RapidAPI-Key": api_key.rapidapi_key
    }
    sunrise_api_url = 'https://sun.p.rapidapi.com/api/sun/?city=' + city
    sunrise_response = urlfetch.fetch(url = sunrise_api_url, headers=headers).content
    # the response is annoyingly a list of dictionaries with a single thing
    # we're going to consolidate them into one dictionary
    # [{u'dawn': u'2019-07-23T05:04:00-05:00'},
    #  {u'sunset': u'2019-07-23T20:18:10-05:00'},
    #  {u'noon': u'2019-07-23T12:57:14-05:00'},
    #  {u'sunrise': u'2019-07-23T05:36:19-05:00'},
    #  {u'dusk': u'2019-07-23T20:50:29-05:00'}]
    sunrise_json = json.loads(sunrise_response)
    all_times = {}
    for dict in sunrise_json:
        all_times.update(dict)
    return all_times


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/index.html')
        self.response.write(index_template.render({'times': getSunriseTimes("chicago"), 'city': "chicago"}))



app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
