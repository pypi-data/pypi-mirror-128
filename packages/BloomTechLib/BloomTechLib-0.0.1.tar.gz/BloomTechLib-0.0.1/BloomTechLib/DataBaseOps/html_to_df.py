import pandas as pd
import requests


def html_to_df(url: str, table_index: int = 0) -> pd.DataFrame:
    """ Takes a URL and returns a DataFrame.

    @param url: web address with an HTML table
    @param table_index: index of the desired table, 0 by default
    @return: DataFrame
    """
    return pd.read_html(requests.get(url).content)[table_index]
