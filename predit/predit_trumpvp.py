import json
import urllib2 as url
import time
keep_running = True
end_time = 1468620000

while keep_running:
  #create request object, with header to ask for json not xml, execute it
  req = url.Request('https://www.predictit.org/api/marketdata/ticker/rvp16')
  req.add_header('Accept', 'application/json')
  pred_content = url.urlopen(req).read()

  predictions = []
  pred_content_json = json.loads(pred_content)
  #print json.dumps(pred_content_json,indent = 4, sort_keys=True)
  for contract in pred_content_json['Contracts']:
    if float(contract['LastTradePrice']) > .01:
      predictions.append((contract['Name'],contract['LastTradePrice'])) 
  string = str(int(time.time()))
  for pred in predictions:
    string +=','+pred[0]+','+str(pred[1])
  #print string    

  with open('predit_trumpvp.txt','a+') as f:
    f.write(string+'\n')
  time.sleep(300)
  if int(time.time()) > end_time:
    keep_running = False

	
