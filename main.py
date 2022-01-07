# This is a sample Python script.
import queue

import requests, json
import pandas as pd
import openpyxl
from tqdm import tqdm
from threading import Thread
import time

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def get_from_xlsx(rf):
    items = []
    load_wb = openpyxl.load_workbook(rf, data_only=True)
    load_ws = load_wb.active
    for row_idx, row in enumerate(load_ws.rows):
        items.append({
          'utterance': str(row[0].value).strip(),
          'label': str(row[1].value).strip(),
        })
    return items

def get_from_xlsx2(rf):
    items = []
    load_wb = openpyxl.load_workbook(rf, data_only=True)
    load_ws = load_wb.active
    for row_idx, row in enumerate(load_ws.rows):
        items.append({
          'utterance': str(row[5].value).strip()
        })
    return items

def api_test(utterance):
    time.sleep(0.7)
    URL = 'http://121.126.223.232:80/api'
    #URL = 'http://121.126.223.232/api'
    data = {
      "userRequest":
      {
        "timezone":"Asia/Seoul",
        "utterance":utterance,
        "channel": "admin",
        "requestType": "text",
        "lang":"ko",
        "user":
        {
          "id":"test",
          "sessionId": ""
        }
      },
      "visit_count":1,
      "context":
      {
      }
    }

    res = requests.post(URL, json=data)
    res.encoding = 'utf-8'
    #print(res.text)
    json_data = json.loads(res.text)
    return json_data

def get_response(items):
    idx = 0
    results = []

    for item in items:
        print(idx, " item['utterance'] >>>>>>>>>>>>>>>>>>>", item['utterance'])
        intent = api_test(item['utterance'])

        result = {
                '사용자발화': intent['userRequest']['utterance'],
                '엔진결과_module': intent['intent']['module'],
                '엔진결과_intent_id': intent['intent']['intent_id'],
                '엔진결과_intent_title': intent['intent']['intent_title'],
                '엔진결과_confidence': intent['intent']['confidence']
            }

        results.append(result)
        idx += 1

    wf = 'chatLog_0816-1019_out_20211220.csv'
    pd.DataFrame(results).to_csv(wf, encoding='utf-8-sig')
    print("=> Write!!", wf)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    items = get_from_xlsx2('test_sample.xlsx')
    idx = 0
    utterance_list = []
    for item in items:
        for i in item['utterance'].split('&'):
            print(idx, "i >>>>>>>>>>>>>>>>", i)
            idx += 1
            result = {'utterance':i}
            utterance_list.append(result)

    get_response(utterance_list)

    #get_response(items)


