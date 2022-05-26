# from bs4 import BeautifulSoup
# from selenium import webdriver
# from html_table_parser import parser_functions as parser
# import requests, json, pprint
# from datetime import datetime
# import os
# from dotenv import load_dotenv  

# # 위도, 경도 구하기
# def current_location():
#     here_req = requests.get("http://www.geoplugin.net/json.gp")

#     if (here_req.status_code != 200):
#         print("현재좌표를 불러올 수 없음")
#     else:
#         location = json.loads(here_req.text)
#         lat = str(location["geoplugin_latitude"])
#         lng = str(location["geoplugin_longitude"])

#     return lat, lng

# lat, lng = current_location()

# # 현재 날짜 시간 구하기
# current_time = datetime.now()
# date = f'{current_time.year}-{current_time.month}-{current_time.day}'
# hour = f'{current_time.hour}'
# minute = f'{current_time.minute}'
# second = f'{current_time.second}'


# # 현재 위치 주소 받기

# load_dotenv()
# KAKAO_API_KEY  = str(os.getenv('KAKAO_API_KEY'))

# # def get_address(lat, lng):
# #     url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x="+lng+"&y="+lat
    
# #     headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
# #     api_json = requests.get(url, headers=headers)
# #     full_address = json.loads(api_json.text)

# #     return full_address

# # full_address = get_address(lat, lng)

# # address = ''
# # for address in full_address:
# #     print(address)
# #     # ad1 = address['region_1depth_name']
# #     # ad2 = address['region_2depth_name']
# #     # ad3 = address['region_3depth_name']
# #     # ad4 = address['region_4depth_name']
# #     # address = f'{ad1}+{ad2}+{ad3}+{ad4}'
# #     break

# # 크롤링
# chrome_driver_path = 'movies/chromedriver.exe'
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)

# # 일출*일몰 시간 받기
# url_c = 'https://astro.kasi.re.kr/life/pageView/9'

# url = url_c + '?lat=' + lat + '&lng=' + lng + '&date=' + date + '&address=' + address

# driver.get(url)
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# sunrise = soup.find_all('span', {'class': 'sunrise'})
# sunset = soup.find_all('span', {'class': 'sunset'})

# rise = sunrise[0].string
# set = sunset[0].string

# # 태양 고도
# url_r = 'https://astro.kasi.re.kr/life/pageView/10'

# # address = '경상북도+구미시+검성로+27'
# url = url_r + '?useElevation=1'+'&lat=' + lat + '&lng=' + lng  +'&elevation=' +'1' + '&output_range=' + '2' + '&date=' + date +  '&hour=' + hour + '&minute=' + minute + '&second=' + second + '&address=' + address 

# driver.get(url)
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# data = soup.find('td')
# data2 = data.next_sibling
# altitude = int(data2.get_text()[0:2])


# time = hour + '시' + ' ' + minute + '분'
# if time < rise or time > set:
#     altitude = -altitude

# now_altitude = str(altitude)

