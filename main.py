from flask import Flask, request
import requests
import json

from werkzeug.wrappers import response

app = Flask(__name__)

def filtringHolidays(year, month):
    response = requests.get(f'https://brasilapi.com.br/api/feriados/v1/{year}')
    holidays = json.loads(response.content)
    response = []
    for holiday in holidays:
        if( holiday['date'][5:7] == month):
            response.append(holiday)
            return json.dumps(response)
    return json.dumps(response)

def filterHolidays(year, month):
    if int(month[0]) == 1 or int(month[0]) == 0:
        if int(month[0]) == 1 and int(month[1]) >= 0 and int(month[1]) <= 2: 
            return filtringHolidays(year, month)

        elif int(month[0]) == 0 and int(month[1]) >= 1 and int(month[1]) <= 9:
            return filtringHolidays(year, month)

        else:
            response = { "status": 400, "error": 'month is not valid'}
            return json.dumps(response)
    else:
        response = { "status": 400, "error": 'month is not valid'}
        return json.dumps(response)

@app.route('/holidays/<year>/<month>')
def findHolidaysByYearAndMonth(year, month):
    return filterHolidays(year, month)
app.run(debug=True)
