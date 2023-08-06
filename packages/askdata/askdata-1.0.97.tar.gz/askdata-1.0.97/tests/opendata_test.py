from askdata import opendata


if __name__ == "__main__":
    nl = "emissions by countries by year"
    res = opendata.search_data(sentence=nl, show_header=True)
