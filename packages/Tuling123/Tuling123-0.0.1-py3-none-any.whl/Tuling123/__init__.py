import requests
import json


name = 'Tuling123'

class robot(object):
    def __init__(self, apiKey, userId, city, province, street):
        self.url = 'http://openapi.tuling123.com/openapi/api/v2'
        self._data = {"apiKey":apiKey, "userID":userId, "city":city, "province":province, "street":street}

    def ask(self, text):
        self.data_param = {
                "reqType":0,
                "perception": {
                    "inputText": {
                        "text": text
                                  },
                    "inputImage":{
                        "url": "imageUrl"
                                  },
                    "selfInfo":  {
                        "location":  {
                            "city": self._data['city'],
                            "province": self._data['province'],
                            "street": self._data['street']
                                      }
                                  }
                              },
                "userInfo":  {
                    "apiKey": self._data['apiKey'],
                    "userId": self._data['userID']
                             }
                  }
        response = requests.post(url=self.url,json=self.data_param)
        py_json = response.text
        py_dict = json.loads(py_json)
        results_list = py_dict['results']
        results_0_dict = results_list[0]
        values_dict = results_0_dict['values']
        return values_dict['text']


        
