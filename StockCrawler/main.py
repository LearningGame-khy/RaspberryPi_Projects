import pandas as pd

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


if __name__ == '__main__':
    get_stock_data_from_web("KIND")
