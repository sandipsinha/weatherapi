from flask import Flask,json, jsonify
import datetime,calendar
from datetime import date
import requests
import rfc3339
import time
import dateutil.parser


app = Flask(__name__)
api_key = 'e034d76e40ee4b3b78cd'
urlapi='https://api.weathersource.com/v1'
event='history_by_postal_code.json'
period='day'
zip='postal_code_eq'
zip1='postal_codes/'
country='country_eq=US'
country1=',US'
fieldlist2='fields=timestamp,tempMax,tempAvg,tempMin'
fieldlist1='fields=timestamp,tempAvg'
event1='/forecast.json?'

@app.route('/<int:zipcode>/temperature-stats', methods=['GET'])
def grab_tempstats(zipcode):
    getdetails=readweather(zipcode)

    return jsonify(getdetails), 200

@app.route('/temperature-stats/<postalcodes>', methods=['GET'])
def grab_weather(postalcodes):
    bigdict={}
    bigret={}
    list1=[]
    ziparray=postalcodes.split(',')
    for items in ziparray:
         getdetails=readweather(items)
         getdetails['postal_code'] = items
         list1.append(getdetails)
         print 'big list is now', items, 'And', list1
    bigret['results'] = list1
    return jsonify(bigret), 200


def readweather(zipcode):
    zipstr=zip + '=' + str(zipcode)
    zipstr1=zip1+str(zipcode)

    url = urlapi+ '/' + api_key + '/' + event
    urla = urlapi+ '/' + api_key
    #now=datetime.datetime.now()
    now5=datetime.datetime.now() - datetime.timedelta(days=5)
    today=time.strftime("%Y-%m-%d")
    retresp={}
    innerlist=[]

    daterange='timestamp_between='+str(now5.strftime('%Y-%m-%d'))+','+str(today)
    datestr='timestamp_eq='+ str(today)
    url1=urla+'/'+zipstr1+country1+event1+datestr+'&'+fieldlist1

    url2=url+'?'+'period=day'+'&'+zipstr+'&'+country+'&'+daterange+'&'+fieldlist2

    response_dict = requests.get(url1).json() # for getting current temperature
    for items in response_dict:
         print 'items', items
         inneresp={}
         current_date_ind='n'
         for key,value in items.iteritems():
             print key, 'and', value
             if key== 'timestamp':
                 readate= dateutil.parser.parse(value)
                 verifydate=readate.strftime('%Y-%m-%d')
                 if verifydate == today:
                     current_date_ind='y'


             if key=='tempAvg':
                 curtmp=value
         if current_date_ind=='y':
             retresp['current'] = curtmp
    response_dict = requests.get(url2).json() # for getting historical temperature
    for items in response_dict:
         inneresp={}
         current_date_ind='n'
         for key,value in items.iteritems():
             if key== 'timestamp':
                 readate= dateutil.parser.parse(value)
                 verifydate=readate.strftime('%Y-%m-%d')
                 if verifydate == today:
                     current_date_ind='y'
                 else:
                     inneresp['date']= dt(readate)
             if key=='tempMax':
                inneresp['max'] = value
             if key=='tempMin':
                inneresp['min'] = value
             if key=='tempAvg':
                 curtmp=value
             if current_date_ind=='y':
                 retresp['current'] = curtmp
         else:
             innerlist.append(inneresp)

    retresp['historical']=innerlist
    return retresp

def dt(u): return rfc3339.rfc3339(u)

def convertk2f(n):
    c=0
    c = (n - 273.15)*9/5 + 32
    return c


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
