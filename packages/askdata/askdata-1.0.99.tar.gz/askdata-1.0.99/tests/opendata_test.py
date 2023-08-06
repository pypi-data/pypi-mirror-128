from askdata import opendata


if __name__ == "__main__":
    nl = "emissions by countries by year"
    response = opendata.search_data(sentence=nl, show_header=True)
    df = opendata.extract_specific_result(response=response, request="top1_df")
    print(df)
