import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import requests


def search_data(sentence, language="en", show_header=False):

    if language != "en" and language != "it":
        print("Please use en for english or it for italian.")
        dict_response = {}
        return dict_response

    if sentence != "":
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "nl": sentence,
            "lang": language,
            "show_header": show_header
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = "https://api-dev.askdata.com/opendata/spacy_method"

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            dict_response = r.json()

            if show_header:
                for dt in dict_response['df_list']:
                    df = pd.DataFrame().from_dict(dt)
                    print(df.head())
                    print("#-------------------#")

            return dict_response
        except Exception as e:
            logging.error(str(e))
    else:
        print("Input sentence is empty!")
        dict_response = {}
        return dict_response
