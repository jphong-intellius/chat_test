import requests, json
import pandas as pd
import openpyxl
from tqdm import tqdm
import queue
from threading import Thread
import datetime

from soynlp.normalizer import only_text


def get_from_xlsx(rf):
    items = []
    load_wb = openpyxl.load_workbook(rf, data_only=True)
    print("=> Read", rf)
    load_ws = load_wb.active
    for row_idx, row in enumerate(load_ws.rows):
        items.append({
            # 'idx': str(row[0].value).strip(),
            'utterance': str(row[1].value).strip(),
            'label_module': str(row[2].value).strip(),
            'label_intent_id': str(row[3].value).strip(),
            'label_intent_title': str(row[4].value).strip(),
        })
    return items


def get_from_csv(rf):
    items = []
    df = pd.read_csv(rf, delimiter=',', header=None)
    print("=> Read", rf)
    list_of_rows = [list(row) for row in df.values]
    for row_idx, row in enumerate(list_of_rows):
        if row_idx == 0:
            continue
        items.append({
            # 'idx': str(row_idx).strip(),
            'utterance': str(row[0]).strip(),
            #'label_intent_title': str(row[2]).strip(),
        })
    return items



def api_test_intellius(item):
    try:
        URL = 'http://121.126.223.232:80/api'
        data = {
            "userRequest": {
                "channel": "admin",
                "timezone": "Asia/Seoul",
                "utterance": item['utterance'],
                'requestType': 'text',
                "lang": "kr",
                "user": {"id": "test", "sessionId":""}
            },
            "context": {},
            "visit_count": 0
        }
        res = requests.post(URL, json=data)
        res.encoding = 'utf-8'
        # print(res.text)
        json_data = json.loads(res.text)
        return json_data["intent"]
    except:
        intent = {
            'module': '',
            'intent_id': '',
            'intent_title': '',
            'confidence': ''
        }
        return intent



def api_test_doub(item):
    try:
        URL = 'http://121.126.223.232:82/ruleApi/chat/rule/mapping'
        data = {
            "utterance": item['utterance']
        }
        res = requests.post(URL, json=data)
        res.encoding = 'utf-8'
        json_data = json.loads(res.text)

        if res.status_code == 200:
            pick = json_data['result']['pick'].split('|')
            intent = {
                'module': 'rule',
                'intent_id': pick[0],
                'intent_title': pick[1],
                'confidence': 1.0
            }
        else:
            intent = {
                'module': '',
                'intent_id': '',
                'intent_title': '',
                'confidence': ''
            }
        return intent
    except:
        intent = {
            'module': '',
            'intent_id': '',
            'intent_title': '',
            'confidence': ''
        }
        return intent


def api_test(item):
    intent_intellius = api_test_intellius(item)
    # intent_doub = api_test_doub(item)
    #
    # is_same = '??????'
    # if intent_intellius['intent_id'] == intent_doub['intent_id']:
    #     is_same = '??????'

    result = {
        # 'idx': item['idx'],
        '???????????????': item['utterance'],
        # '??????_module': item['label_module'] if item['label_module'] is not None else '',
        # '??????_intent_id': item['label_intent_id'] if item['label_intent_id'] is not None else '',
        #'????????????_intent_title': item['label_intent_title'] if item['label_intent_title'] is not None else '',
        '????????????_module': intent_intellius['module'],
        '????????????_intent_id': intent_intellius['intent_id'],
        '????????????_intent_title': intent_intellius['intent_title'],
        # '????????????_confidence': intent_intellius['confidence'],
        # '?????????_module': intent_doub['module'],
        # '?????????_intent_id': intent_doub['intent_id'],
        # '?????????_intent_title': intent_doub['intent_title'],
        # '?????????_confidence': intent_doub['confidence'],
        # '??????': is_same
    }
    return result


if __name__ == '__main__':
    items = get_from_csv('text_csv.csv')
    results = []
    for item in tqdm(items, desc='utterance list'):
        print(item)
        result = api_test(item)
        results.append(result)

    # que = queue.Queue()
    # threads_list = []
    # idx = 1
    # for item in tqdm(items, desc='utterance list'):
    #     t = Thread(target=lambda q, arg1: q.put(api_test(arg1)), args=(que, item))
    #     t.start()
    #     threads_list.append(t)
    #     if idx % 10 == 0:
    #         for t in threads_list:
    #             t.join()
    #             result = que.get()
    #             results.append(result)
    #         threads_list = []
    #     idx += 1
    #
    # for t in threads_list:
    #     t.join()
    #     result = que.get()
    #     results.append(result)


    now = datetime.datetime.now()
    date_string = now.strftime('%Y%m%d%H%M%S')
    wf = 'out{}.csv'.format(date_string)
    pd.DataFrame(results).to_csv(wf, encoding='utf-8-sig')
    print("=> Write!!", wf)





# if __name__ == '__main__':
#     items = get_from_xlsx('test.xlsx')
#     results = []
#     for item in tqdm(items, desc='utterance list'):
#         intent = api_test(item['utterance'])
#         result = {
#             '???????????????': item['utterance'],
#             '????????????': item['label'],
#             '????????????_module': intent['module'],
#             '????????????_intent_id': intent['intent_id'],
#             '????????????_intent_title': intent['intent_title'],
#             '????????????_confidence': intent['confidence']
#         }
#         results.append(result)
#     wf = 'out.csv'
#     pd.DataFrame(results).to_csv(wf, encoding='utf-8-sig')
#     print("=> Write!!", wf)

