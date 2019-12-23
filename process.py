from bs4 import BeautifulSoup
import requests

import setting

def get_rank() :
    rank = [1, 1]

    if(setting.adtype == '쇼핑검색')  :
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
