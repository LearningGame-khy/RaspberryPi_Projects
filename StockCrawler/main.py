import pandas as pd
from urllib.request import urlopen
from requests import get
from bs4 import BeautifulSoup
import os


def get_stock_data_from_web(site_name, require_args=None):
    _SITE_URL = {
        'KIND': 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download',
    }

    _COL_NAME_DICT = {
        '회사명': 'company',
        '종목코드': 'code',
        '업종': 'sector',
        '주요제품': 'major_product',
        '상장일': 'listing_date',
        '결산월': 'closing_anaccount',
        '대표자명': 'owner',
        '홈페이지': 'website',
        '지역': 'zone',
    }

    # 한국거래소 상장법인목록은 EXCEL 파일로 제공됨.
    # [회사명, 종목코드, 업종, 주요제품, 상장일, 결산월, 대표자명, 홈페이지, 지역]
    stock_data = pd.read_html(_SITE_URL[site_name], header=0)[0]

    if require_args:
        stock_required = pd.DataFrame()
        for col_name in require_args:
            stock_required[col_name] = stock_data[col_name].values
    else:
        stock_required = stock_data

    stock_required = stock_required.rename(columns=_COL_NAME_DICT)

    # 주식코드가 6자리 고정이나, int 형식으로 되어있어서 str 6자로 만들어줘야함
    stock_required.code = stock_required.code.map('{:06d}'.format)
    return stock_required


_URL_DICT = {
    'naver': 'https://finance.naver.com/sise/sise_market_sum.naver',
}

def is_valid_site(site_name):
    return True if site_name.lower() in _URL_DICT else False

def get_url(site_name):
    return _URL_DICT[site_name.lower()]

def get_market_cap_from_NAVER(url):
    req = get(url)
    html = BeautifulSoup(req.content.decode('euc-kr', 'replace'), 'html.parser')
    trs = html.select_one('tbody').findAll('tr')

    _INTEREST_COLS = {
        'no': 0,
        'company': 1,
        'current': 2,
        'market_cap': 6,
        'PER': 10,
        'ROE': 11
    }
    stock_dataframe = pd.DataFrame(columns=_INTEREST_COLS.keys())
    for tr in trs:
        td = tr.select('td')
        data = []
        for col in _INTEREST_COLS.keys():
            if not td[_INTEREST_COLS[col]].text:
                break
            data.append(td[_INTEREST_COLS[col]].text)

        if len(data) > 0:
            stock_dataframe = stock_dataframe.append(pd.Series(data, index=stock_dataframe.columns), ignore_index=True)
    stock_dataframe.set_index('no', inplace=True)
    return stock_dataframe


if __name__ == '__main__':
    # stock_required = get_stock_data_from_web("KIND")
    # stock_required = get_stock_data_from_web('KIND', ['회사명', '종목코드'])

    site_name = 'Naver'
    if is_valid_site(site_name):
        url = get_url(site_name)
        market_cap = get_market_cap_from_NAVER(url)
        print(market_cap.head(10))
