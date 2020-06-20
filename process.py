from bs4 import BeautifulSoup
import requests
import threading
import time

import setting
import signaturehelper

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, setting.SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': setting.API_KEY, 'X-Customer': str(setting.CUSTOMER_ID).replace('\u200e',''), 'X-Signature': signature}

def get_rank() :
    rank = [1, 1]

    if(setting.adtype == '쇼핑검색') :
        if(setting.format == 'PC') :
            for i in range(1, setting.page+1) :
                url = 'https://search.shopping.naver.com/search/all.nhn?pagingIndex='+str(i)+'&query={}'.format(setting.search_word)
                req = requests.get(url)

                html = req.text
                soup = BeautifulSoup(html,'html.parser')
                url_list = soup.find(class_='search_list').find(class_='goods_list').find_all(class_='ad')

                for i in url_list :
                    if(setting.identify_word == i.get('data-nv-mid')) :
                        return rank;
                    else :
                        rank[1] += 1

                rank[0] += 1
                rank[1] = 1

        if(setting.format == 'MO') :
            for i in range(1, setting.page+1) :
                url = 'https://msearch.shopping.naver.com/search/all.nhn?pagingIndex='+str(i)+'&query={}'.format(setting.search_word)
                req = requests.get(url)

                html = req.text
                soup = BeautifulSoup(html,'html.parser')
                url_list = soup.find_all(class_='_1SzfBYA4Wc')

                for i in url_list :
                    if(i.find(class_='_1SwezRSbBH').find(class_='_2kELSD-U0C').find(class_='c_ad') != None) :
                        if(setting.identify_word == i.get('id').replace('_sr_lst_', '').replace('hot_','')) :
                            return rank;
                        else :
                            rank[1] += 1

                rank[0] += 1
                rank[1] = 1

    if(setting.adtype == '파워링크')  :
        if(setting.format == 'PC') :
            for i in range(1, setting.page+1) :
                url = 'https://ad.search.naver.com/search.naver?&pagingIndex='+str(i)+'&query={}'.format(setting.search_word)
                req = requests.get(url)

                html = req.text
                soup = BeautifulSoup(html,'html.parser')
                url_list = soup.find(class_='ad_section').find(class_='lst_type').find_all(class_='lst')
                for i in url_list :
                    if(setting.identify_word == i.find(class_='url_area').a.text) :
                        return rank;
                    else :
                        rank[1] += 1

                rank[0] += 1
                rank[1] = 1

        if(setting.format == 'MO') :
            for i in range(1, setting.page+1) :
                url = 'https://ad.search.naver.com/search.naver?&page='+str(i)+'&where=m_expd&query={}'.format(setting.search_word)
                req = requests.get(url)

                html = req.text
                soup = BeautifulSoup(html,'html.parser')
                url_list = soup.find_all(class_='list_item')
                for i in url_list :
                    if(setting.identify_word == i.find(class_='url_area').a.text) :
                        return rank;
                    else :
                        rank[1] += 1

                rank[0] += 1
                rank[1] = 1

    if(setting.adtype == "통합검색")  :
        if(setting.format == 'PC') :
            print('통합검색_PC')
        if(setting.format == '모바일') :
            print('통합검색_모바일')

    return [0, 0];

def get_adgroup_id() :
    uri = '/ncc/campaigns'
    method = 'GET'
    r = requests.get(setting.BASE_URL + uri, headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

    for i in r.json():
        if(i['name'] == setting.campaign_name) :
            campaign_id = i['nccCampaignId']

    uri = '/ncc/adgroups'
    method = 'GET'
    r = requests.get(setting.BASE_URL + uri, params={'nccCampaignId': campaign_id} ,headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

    for i in r.json():
        if(i['name'] == setting.adgroup_name) :
            adgroup_id = i['nccAdgroupId']

    return adgroup_id

def get_keyword_id() :
    uri = '/ncc/keywords'
    method = 'GET'
    r = requests.get(setting.BASE_URL + uri, params={'nccAdgroupId': get_adgroup_id()} ,headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

    for i in r.json():
        if(i['keyword'] == setting.modify_word) :
            keyword_id = i['nccKeywordId']
    return keyword_id

def get_ad_id() :
    uri = '/ncc/ads'
    method = 'GET'
    r = requests.get(setting.BASE_URL + uri, params={'nccAdgroupId': get_adgroup_id()} ,headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

    for i in r.json():
        if(i['referenceData']['id'] == setting.modify_word) :
            ad_id = i['nccAdId']
    return ad_id

def get_amount_by_keyword_id() :
    uri = '/ncc/keywords'
    method = 'GET'
    r = requests.get(setting.BASE_URL + uri, params={'nccAdgroupId': get_adgroup_id()} ,headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

    for i in r.json():
        if(i['keyword'] == setting.modify_word) :
            amount = i['bidAmt']
    return amount

def get_amount_by_ad_id() :
    uri = '/ncc/ads'
    method = 'GET'
    r = requests.get(setting.BASE_URL + uri, params={'nccAdgroupId': get_adgroup_id()} ,headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

    for i in r.json():
        if(i['referenceData']['id'] == setting.modify_word) :
            amount = i['adAttr']['bidAmt']
    return amount

def change_amount(cmd) :
    if(cmd == "up") :
        if(setting.adtype == '쇼핑검색') :
            print("초기금액: " + str(get_amount_by_ad_id()) + "원")

            uri = '/ncc/ads/' + get_ad_id()
            method = 'GET'
            r = requests.get(setting.BASE_URL + uri, headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            retrieved_adkeyword = r.json()

            uri = '/ncc/ads'
            method = 'PUT'
            retrieved_adkeyword['adAttr']['bidAmt'] = get_amount_by_ad_id() + setting.amount_unit
            r = requests.put(setting.BASE_URL + uri, params={'fields': 'adAttr'}, json=[retrieved_adkeyword], headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            print("변경된 금액: " + str(get_amount_by_ad_id()) + "원")

        elif(setting.adtype == '파워링크') :
            print("초기금액: " + str(get_amount_by_keyword_id()) + "원")

            uri = '/ncc/keywords/' + get_keyword_id()
            method = 'GET'
            r = requests.get(setting.BASE_URL + uri, headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            retrieved_adkeyword = r.json()

            uri = '/ncc/keywords'
            method = 'PUT'

            retrieved_adkeyword['bidAmt'] = get_amount_by_keyword_id() + setting.amount_unit
            retrieved_adkeyword['useGroupBidAmt'] = 0
            r = requests.put(setting.BASE_URL + uri, params={'fields': 'bidAmt'}, json=[retrieved_adkeyword], headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            print("변경된 금액: " + str(get_amount_by_keyword_id()) + "원")

    if(cmd == "down") :
        if(setting.adtype == '쇼핑검색') :
            print("초기금액: " + str(get_amount_by_ad_id()) + "원")

            uri = '/ncc/ads/' + get_ad_id()
            method = 'GET'
            r = requests.get(setting.BASE_URL + uri, headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            retrieved_adkeyword = r.json()

            uri = '/ncc/ads'
            method = 'PUT'
            retrieved_adkeyword['adAttr']['bidAmt'] = get_amount_by_ad_id() - setting.amount_unit
            r = requests.put(setting.BASE_URL + uri, params={'fields': 'adAttr'}, json=[retrieved_adkeyword], headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            print("변경된 금액: " + str(get_amount_by_ad_id()) + "원")

        elif(setting.adtype == '파워링크') :
            print("초기금액: " + str(get_amount_by_keyword_id()) + "원")

            uri = '/ncc/keywords/' + get_keyword_id()
            method = 'GET'
            r = requests.get(setting.BASE_URL + uri, headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            retrieved_adkeyword = r.json()

            uri = '/ncc/keywords'
            method = 'PUT'

            retrieved_adkeyword['bidAmt'] = get_amount_by_keyword_id() - setting.amount_unit
            retrieved_adkeyword['useGroupBidAmt'] = 0
            r = requests.put(setting.BASE_URL + uri, params={'fields': 'bidAmt'}, json=[retrieved_adkeyword], headers=get_header(method, uri, setting.API_KEY, setting.SECRET_KEY, setting.CUSTOMER_ID))

            print("변경된 금액: " + str(get_amount_by_keyword_id()) + "원")

def main () :
    if(get_rank()[0] == 0) :
        print("URL(소재)을 셋팅을 잘못하였거나 "+ str(setting.page) +"페이지 내에서 찾을 수 없습니다.")
    elif(get_rank()[0] > 1) :
        print("현재 셋팅한 URL(소재)은 " + str(get_rank()[0]) + '페이지에서 '+ str(get_rank()[1]) +"등 입니다.")
        print("1 페이지에서 벗어났기 때문에 금액을 증가시킵니다.")
        change_amount('up')
    elif(get_rank()[1] > setting.rank) :
        print("현재 셋팅한 URL(소재)은 " + str(get_rank()[0]) + '페이지에서 '+ str(get_rank()[1]) +"등 입니다.")
        print("셋팅한 " + str(setting.rank) +"등 보다 낮기 때문에 금액을 증가시킵니다.")
        change_amount('up')
    else :
        print("현재 셋팅한 URL(소재)은 " + str(get_rank()[0]) + '페이지에서 '+ str(get_rank()[1]) +"등 입니다.")
        print("셋팅한 " + str(setting.rank) +"등 보다 높거나 같기 때문에 금액을 감소시킵니다.")
        change_amount('down')

    timer = threading.Timer(setting.time * 60, main)
    timer.start()

if __name__ == "__main__":
    print("------------------------------------------------------------------")
    print("네이버 자동입찰 프로세스를 시작합니다")
    print("------------------------------------------------------------------")
    print("검색어: " + setting.search_word)
    print("식별어: " + setting.identify_word)
    print("희망등수: " + str(setting.rank) + "등")
    if(setting.adtype == '쇼핑검색') :
        print("초기금액: " + str(get_amount_by_ad_id()) + "원")
    elif(setting.adtype == '파워링크') :
        print("초기금액: " + str(get_amount_by_keyword_id()) + "원")
    print("증감금액: " + str(setting.amount_unit) + "원")
    print("증가간격: " + str(setting.time) + "분")
    print("광고포맷: " + setting.adtype + "-" + setting.format)
    print("------------------------------------------------------------------")

    main()
