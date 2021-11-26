

def get_loan_data(c):
    import requests
    import pandas as pd
    import os.path                      
    import numpy as np

    jn_key = 'f8a1ee19fb60a1fe7d89fbefd5a1ee729d4a67be99b748cdef74e3b1381f9e6e'
    file = f'C:\\Users\\soymi\\Desktop\\lib_git\\2021-2Capstonedesign\\api_data\\{c}.csv' 
    
    if os.path.isfile(file):
        pass
    else:
        isbn = []
        libcode = []
        reg_date = []

        url = f'http://data4library.kr/api/itemSrch?&libCode={c}&authKey={jn_key}&pageNo=1&pageSize=10&format=json&startDt=2021-01-01&endDt=2021-10-01'
        try:
            res = requests.get(url).json()
            pc = res['response']['numFound'] // 10
            re = res['response']['numFound'] % 10
        except:
            return(c)
        
        if pc == 1:
            try:
                url = f'http://data4library.kr/api/itemSrch?libCode={c}&authKey={jn_key}&pageNo=1&pageSize=10&format=json&startDt=2021-01-01&endDt=2021-10-01'
                res = requests.get(url).json()
                for j in res['response']['docs']:
                    libcode.append(c)
                    isbn.append(j['doc']['isbn13'])
                    reg_date.append(j['doc']['reg_date'])
            except:
                pass
        elif re == 0:
            for pgn in range(1,pc+1):
                try:
                    url = f'http://data4library.kr/api/itemSrch?libCode={c}&authKey={jn_key}&pageNo={pgn}&pageSize=10&format=json&startDt=2021-01-01&endDt=2021-10-01'
                    res = requests.get(url).json()
                    for j in res['response']['docs']:
                        libcode.append(c)
                        isbn.append(j['doc']['isbn13'])
                        reg_date.append(j['doc']['reg_date'])
                except:
                    pass

        else:
            for pgn in range(1,pc+2):
                try:
                    url = f'http://data4library.kr/api/itemSrch?libCode={c}&authKey={jn_key}&pageNo={pgn}&pageSize=10&format=json&startDt=2021-01-01&endDt=2021-10-01'
                    res = requests.get(url).json()
                    for j in res['response']['docs']:
                        libcode.append(c)
                        isbn.append(j['doc']['isbn13'])
                        reg_date.append(j['doc']['reg_date'])
                except:
                    pass

        result = pd.DataFrame({'libcode' : libcode, 'isbn' : isbn, 'reg_date' : reg_date})
        result.to_csv(f'./api_data/{c}.csv', index = False)

def get_info_from_isbn(isbn):
    
    import requests
    import pandas as pd
    import json
    import numpy as np
    
    oa_key = '578ca4ba507631e4a9b621f4029400eac427aaf6071b45611e599387b637b6dc'
    jn_key = 'f8a1ee19fb60a1fe7d89fbefd5a1ee729d4a67be99b748cdef74e3b1381f9e6e'


    try:
        url = f'http://seoji.nl.go.kr/landingPage/SearchApi.do?cert_key={oa_key}&isbn={isbn}&result_style=json&page_size=1&page_no=1'
        res = requests.get(url).json()
        url2 = f'http://data4library.kr/api/usageAnalysisList?authKey={jn_key}&format=json&isbn13={isbn}'
        res2 = requests.get(url2).json()
    except:
        return([isbn, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
    
    
    ############
    
    
    try:
        title = res['docs'][0]['TITLE']
    except:
        title = np.nan
    
    try:
        if res['docs'][0]['TITLE_URL'] == '':
            title_image_url = res2['response']['book']['bookImageURL']
        else:
            title_image_url = res['docs'][0]['TITLE_URL']
    except:
        title_image_url = np.nan
    
    try:
        pages = res['docs'][0]['PAGE']
        if pages == '':
            pages = np.nan
    except:
        pages = np.nan
    
    try:
        major_subject = res['docs'][0]['SUBJECT']
        if major_subject == '':
            major_subject = np.nan
    except:
        major_subject = np.nan
        
    try:
        author = res['docs'][0]['AUTHOR']
        if author == '':
            author = np.nan
    except:
        author = np.nan
    
    try:
        target_1 = res2['response']['loanGrps'][0]['loanGrp']['age']
        target_2 = res2['response']['loanGrps'][0]['loanGrp']['gender']
    except:
        target_1 = np.nan
        target_2 = np.nan
    
    try:
        description = res2['response']['book']['description']
    except:
        description = np.nan
    
    return([isbn, title, title_image_url, pages, major_subject, author, description, target_1, target_2])


def get_image(z):
    import os
    import numpy as np
    import urllib
    if os.path.isfile(f'./image/{z[1]}.jpg'):
        return z[1]

    try:
        urllib.request.urlretrieve(z[0], f'./image/{z[1]}.jpg')
        return z[1]
    except:
        return np.nan