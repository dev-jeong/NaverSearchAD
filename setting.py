#API 정보 설정
BASE_URL = 'https://api.naver.com'
API_KEY = '01000000007ff99c3c70244df9f84ae69ec049ed8c6c1eac54731a9d8588bcb30db174d3dc'
SECRET_KEY = 'AQAAAAB/+Zw8cCRN+fhK5p7ASe2Ms4p3GjtWqdqpWphSzCT3ZA=='
CUSTOMER_ID = '576009'

# format = PC, MO
# adtype = 쇼핑검색, 파워링크, 통합검색
# page = searching을 진행할 페이지 갯수
format = "MO"
adtype = "파워링크"
page = 5

# campaign, adgroup 이름설정
campaign_name = "1. 검색광고_애니시트 - 주간"
adgroup_name = "!!!!!_대표키워드"

# search_word = naver에서 검색할 단어
# identify_word = 등수 식별을 위한 단어 (파워링크 = url, 쇼핑검색 = 쇼핑상품ID)
# modify_word = 금액 변경을 위해 사용되는 단어 (파워링크 = 키워드, 쇼핑검색 = 쇼핑상품ID)
search_word = "시트지"
identify_word = "http://hdi1533.modoo.at/"
modify_word = "시트지"

# 프로세스 동작 설정 (단위 : amount_unit(원), time(분), rank(등))
amount_unit = 10
time = 10
rank = 7
