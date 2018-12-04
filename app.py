from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    # commented out by Naresh
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print ("starting processRequest...")
   # if req.get("result").get("action") != "yahooWeatherForecast":
        #return {}
    #baseurl = "https://query.yahooapis.com/v1/public/yql?"
    #yql_query = makeYqlQuery(req)
   # if yql_query is None:
       # return {}
    yql_url = "https://api.thingspeak.com/channels/107478/feeds.json?results=1"
    result = urlopen(yql_url).read()
    #data = json.loads(result)
    #for some the line above gives an error and hence decoding to utf-8 might help
    data = json.loads(result.decode('utf-8'))
    res = makeWebhookResult(data)
    zap_url="https://hooks.zapier.com/hooks/catch/3174192/fdhs6r?dataq="+res
    result1 = urlopen(zap_url).read()
    zapactivate=json.loads(result1)
    print ("zap activated zooooop!!")
    print (zapactivate)
    return res


"""def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None
    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"/"""


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    feeds = data.get('feeds')[0]
    if feeds is None:
        return {}
    #for r in feeds:
        #return r["field1"]
    field1 = feeds.get('field1')
    if field1 is None:
        return {}

    

    
      

    # print(json.dumps(item, indent=4))

    speech = "Today the water level of main tank is " + feeds.get('field1')
    print("Response:")
    print(speech)
    return field1


@app.route('/test', methods=['GET'])
def test():
    app = ClarifaiApp(api_key='d1c9df3c907e48e1a317856eea26c099')
    model = app.public_models.general_model
    model.model_version = 'aa7f35c01e0642fda5cf400f543e7c40'
    response = model.predict([ClImage(url="https://drive.google.com/uc?id=1r4gH7zDmQ24cuB-26PgLuyb7ncU_2WMY&export=download")])
    print(response)
    response=json.loads(response)
    return response


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')







# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
"""# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Updated in July 2018 to reflect Dialogflow v2 changes for request/response
# Author - Naresh Ganatra
# http://youtube.com/c/NareshGanatra


#from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

#from urllib.parse import urlparse, urlencode
#from urllib.request import urlopen, Request
#from urllib.error import HTTPError

#import json
import os

from flask import Flask
#from flask import request
#from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/w',methods=['GET'])
def index():
    return "hello how are u test message"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
       
    app.run(debug=True, port=port, host='0.0.0.0')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    # commented out by Naresh
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print ("here I am....")
    print ("starting processRequest...",req.get("queryResult").get("action"))
    if req.get("queryResult").get("action") != "yahooWeatherForecast":
        print ("Please check your action name in DialogFlow...")
        return {}
    print("111111111111")
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    print("1.5 1.5 1.5")
    yql_query = makeYqlQuery(req)
    print ("2222222222")
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    print("3333333333")
    print (yql_url)
    result = urlopen(yql_url).read()
    data = json.loads(result)
    #for some the line above gives an error and hence decoding to utf-8 might help
    #data = json.loads(result.decode('utf-8'))
    print("44444444444")
    print (data)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None
    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)
    #Naresh
    return {

    "fulfillmentText": speech,
     "source": "Yahoo Weather"
    }


@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    string = "You are awesome !!"
    Message ="this is the message"

    my_result =  {

    "fulfillmentText": string,
     "source": string
    }

    res = json.dumps(my_result, indent=4)

    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':


    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
#***********************************************************************"""
