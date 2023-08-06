import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import requests
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def search_data(sentence, language="en", show_header=False, dataset_score_dict=None, boost_columns=False,
                boost_name_score=False, use_domains=True):

    if language != "en" and language != "it":
        print("Please use 'en' for english or 'it' for italian.")
        dict_response = {}
        return dict_response

    if sentence != "":
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "nl": sentence,
            "lang": language,
            "dataset_score_dict": dataset_score_dict,
            "show_header": show_header,
            "use_domains": use_domains,
            "boost_columns": boost_columns,
            "boost_name_score": boost_name_score
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = "https://api-dev.askdata.com/opendata/spacy"

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            dict_response = r.json()

            if show_header:
                # Print first, second, third place
                i = 1
                j = 0
                for el in dict_response['dataset_rank']["first_place"]["dataset_list"]:
                    score = dict_response['dataset_rank']["first_place"]["scoring"]
                    name = el['dataset']
                    df = pd.DataFrame().from_dict(dict_response['df_list'][j])
                    print("#------------------------------------------------------------------#")
                    print("Dataset " + name + " ranked as #" + str(i) + " with score: " + str(score) + ".")
                    print()
                    print(df.head())
                    print("#------------------------------------------------------------------#")
                    print()
                    j += 1
                # i += 1

            return dict_response
        except Exception as e:
            logging.error(str(e))
    else:
        print("Input sentence is empty!")
        dict_response = {}
        return dict_response
