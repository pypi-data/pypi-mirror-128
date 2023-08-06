import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import requests


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
                for k in dict_response['dataset_rank'].keys():
                    for dt in dict_response['dataset_rank'][k]["dataset_list"]:
                        score = dict_response['dataset_rank'][k]["scoring"]
                        df = pd.DataFrame().from_dict(dt)
                        print("Dataset ranked as #" + str(i) + ". Score: " + str(score))
                        print(df.head())
                        print("#-------------------#")
                        print()
                    i += 1
                    break

            return dict_response
        except Exception as e:
            logging.error(str(e))
    else:
        print("Input sentence is empty!")
        dict_response = {}
        return dict_response
