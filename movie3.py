import requests
from bs4 import BeautifulSoup
import csv

soup_objects = []

URL = 'https://movie.naver.com/movie/running/current.nhn'

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

id_section = soup.select(
'#content > .article > div:nth-child(1) > .lst_wrap > ul > li'
)

for id in id_section:
        
    a_tag = id.select_one('dl > dt > a')

    code = a_tag['href'].split('=')[1]


    headers = {
        'authority': 'movie.naver.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code={0}'.format(code),
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'NNB=ULSNSBNJRIBF6; NRTK=ag^#all_gr^#1_ma^#-2_si^#0_en^#0_sp^#0; BMR=; page_uid=UyoQAdprvOsssczvyIVssssssXK-261716; nx_ssl=2; csrf_token=58f5dcfd-f0fd-4423-8044-1ac741f4c622',
    }

    params = (
        ('code', f'{code}'),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)


    soup = BeautifulSoup(response.text,'html.parser')

    review_section = soup.select(
    'body > div > div > div.score_result > ul > li'
    )


    final_movie_data = []

    for idx, review in enumerate(review_section):
                    
        score_tag = review.select_one('.star_score > em')
        score = score_tag.get_text()

        review_tag = review.select_one('.score_reple > p > #_filtered_ment_{0}'.format(idx))
        review = review_tag.text.strip()
        
        data = [score, review]
    

        final_movie_data.append(data)

        
    for data in final_movie_data:
        print(data[0], data[1])
    






    