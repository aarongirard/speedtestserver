import urllib2 as url
import json
import sys
import time

"""
python predit.py ticker_symbol recurring end_datetime

ticket_symbol: the string id of the predict_it contract to follow
recurring: should the script continue running? 0 for just one get request
and any value higher will be the duraction (in seconds) to repeat the requests
end_date: date in epoch to end the script if recurring

ex.
python predit.py USPREZ16 60 1468592437

this will run the script collecting contract data on usprez16 contracts every
minute and ending after 7/15/2016, 10:20:37 AM GMT-4:00 DST


OUTPUT: data is automatically written to a file named ticket_symbol.csv
so the output file for the above example would be USPREZ16.csv

Currently, the output is contract name, contract LastTradePrice for contracts
with a LastTradePrice .01 or else there is a ton of useless contracts at .01

output format = datetime(epoch),name,LastTradePrice,name,LastTradePrice,...
	- the names are sorted before outputting, but may not be static if a 
	contracts value rises to .02 or higher or if a new contract is created 
	with a value of .02 or higher. So these would be added to csv

"""
#create request 
def create_request_prediction_content(ticker_symbol, format = 'applicatoin/json'):
  req = url.Request('https://www.predictit.org/api/marketdata/ticker/' + ticker_symbol)
  req.add_header('Accept', format)
  return req

#send http get request  
def get_prediction_content(req):
  try:
    resp = url.urlopen(req)
  except urllib2.URLError as e:
    print str(e.reason)
    return 0
  content = resp.read()
  if content == 'null':
    print 'It looks like the ticket symbol you input is not valid'
    exit()
  return content

#parse returned json and parse out specific data into dictionary
def parsed_prediction_contract(got_prediction):
  #print parsed_prediction.keys()
  #print json.dumps(parsed_prediction, indent=4, sort_keys=True)
  parsed_prediction = json.loads(got_prediction)
  pred = {}
  for contract in parsed_prediction['Contracts']:
    if float(contract['LastTradePrice']) > .01 :
      pred[contract['Name']] = contract['LastTradePrice']
  return pred

#send request, get content, parse it as json, write to file
def get_parse_write(req):
  #send get http api request
  content = get_prediction_content(req)

  #if error, return 
  if content == 0:
    return
  #parse returned json object, reutrn dictionary with lastcloseprice
  prediction_content_to_save = parsed_prediction_contract(content)
  
  #initialize csv with date/time as epoch
  pred_csv = str(int(time.time()))
  
  #loop through dictionary to build csv string of data
  for k,v in sorted(prediction_content_to_save.items()):
    pred_csv+= ','  + k + ',' + str(v)
  
  #write string to file, creates it if not existing
  with open(TICKER_SYMBOL+'.csv', 'a+') as f:
    f.write(pred_csv + '\n')

  return pred_csv #maybe for later use idk


START_DATETIME = int(time.time())
#command line args required
if len(sys.argv) == 2 and sys.argv[1].lower() == 'help':
  print 'You have contacted the help center'
  print 'python predit.py ticker_symbol recurring end_date'
  exit()

if len(sys.argv) != 4:
  print 'There are ', str(len(sys.argv) -1), ' command line args'
  print 'Need 3 CLA!. For help use python predit.py help'
  exit()

TICKER_SYMBOL = sys.argv[1]
RECURRING = int(sys.argv[2])
END_DATETIME = int(sys.argv[3])

#create request to send
#Do once, it doesn't need to change 
req = create_request_prediction_content(TICKER_SYMBOL) #'USPREZ16'

#if recurring == 0, run once and exit
if RECURRING == 0:
  print get_parse_write(req)
  exit()

#while end time hasn't been reached
print 'Start Time: ',START_DATETIME,' End Time: ', END_DATETIME
while int(time.time()) < END_DATETIME: 
  get_parse_write(req)
  time.sleep(RECURRING) 

print 'The script has reached the ented End Datetime'
exit()
