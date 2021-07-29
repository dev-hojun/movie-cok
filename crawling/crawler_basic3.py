import re
import os
from random import randrange

import requests
from bs4 import BeautifulSoup as bs
import openpyxl
from urllib.request import urlretrieve

# 장르 리스트
genreList = ["드라마", "판타지", "서부", "공포", "멜로/로맨스", "모험", "스릴러", "느와르", "컬트", "다큐멘터리", "코미디", "가족", "미스터리", "전쟁", "애니메이션", "범죄", "뮤지컬", "SF", "액션", "무협", "에로", "서스펜스", "서사", "블랙코미디", "실험", "공연실황"]

# 연령등급 리스트
ageList = ["전체 관람가", "12세 관람가", "15세 관람가", "청소년 관람불가"]

# 특수문자 제거 위한 함수
def cleanText(readData):
    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》 ]', '', readData)
    return text

# 네티즌평점, 전문가평점 조합하기 위한 함수
def cleanScore (list):
    cleanScore = ""
    for l in list :
        cleanScore += l.text
    return cleanScore

def crawling(start_code, finish_code):
    try:
        global is_ok
        is_ok = False
        wb = openpyxl.Workbook()
        sheet = wb.active
        point_code_list = []
        basic_code_list = []
		
		# point.py 에서 수집한 영화 코드 리스트 파일 가져오기
        with open('../crawling/data/final_code_list.txt', 'r') as text_file:
        # with open('../crawling/data/test_code_list.txt', 'r') as text_file:
            point_code_list = text_file.readline().split(",")

		# 항목 : 코드, 제목, 장르, 국가, 상영시간, 감독, 배우, 연령등급, 개봉일, 줄거리, 사진 주소, 네티즌평점, 전문가평점
        sheet.append(["id", "title", "genre", "nation", "playtime", "directors", "actors", "age", "date", "summary", "image", "score_npro", "score_pro"])

        # HTML 파싱
        # 저장 된 영화와 포스터의 행을 맞추기 위한 정수 j
        j = 0
        
        # point_code_list로 코드 범위 지정
        for code in point_code_list:
            is_ok = True
            raw = requests.get("https://movie.naver.com/movie/bi/mi/basic.nhn?code=" + code)
            
            html = bs(raw.text, 'html.parser')
			
            # 전체 컨테이너
            movie = html.select("div.article")

            # print(code, " : 코드")
			# 성인 인증 필요한 영화 제외
            if(len(movie) == 0):
                # print("00000000000000000")
                is_ok = False
				
            # 전체 컨테이너가 갖고 있는 영화관련 정보
            for a, m in enumerate(movie):
                # 제목
                title = m.select_one("h3.h_movie a")               
                
                # 장르
                genre = m.select("dl.info_spec dd p span:nth-of-type(1) a")
				
                # 국가 
                nation = m.select("dl.info_spec dd p span:nth-of-type(2) a")
                
				# 상영시간
                playtime = m.select_one("dl.info_spec dd p span:nth-of-type(3)")

                # 감독
                directors = m.select("dl.info_spec dd:nth-of-type(2) a")

                # 배우
                actors = m.select("dl.info_spec dd:nth-of-type(3) a")
                
			    # 연령등급
                age = m.select_one("dl.info_spec dd:nth-of-type(4) p a")
				
				# 개봉일
                date = m.select("dl.info_spec dd p span:nth-of-type(4):nth-child(n+3):nth-child(-n+4) a:nth-last-child(-n+2)")
				
                # 줄거리
                summary = m.select("div.story_area p.con_tx")
				
				# 사진주소
                image = m.select_one("div.mv_info_area div.poster a img")
				
                score_npro = m.select_one(".netizen_score .sc_view .star_score em")
                score_pro = m.select_one(".special_score .sc_view .star_score em") 
				
				# 유효성 검사
				# 장르 없거나 장르 리스트 외의 것일 경우 제외
                if len(genre) > 0:
                    if genre[0].text not in genreList:
                        is_ok = False
                        continue
                elif len(genre) == 0:
                    is_ok = False
                    continue
				
				# 국가에 TV영화 들어올 경우 제외
                for n in nation:
                    if (n.text == "TV영화"):
                        is_ok = False
                        break
				
                # 배우에 관람 기준이 적혀있거나 배우가 없을 경우 제외
                if len(actors) >= 1:
                    if actors[0].text in ageList:
                        is_ok = False
                        continue
                elif len(actors) == 0:
                    is_ok = False
                    continue

				# 연령등급 없거나 연령등급 리스트 외의 것일 경우 제외
                if(age == None):
                    is_ok = False
                    continue
                elif age.text not in ageList :
                    is_ok = False
                    continue

				# 상영시간 없을 경우 제외
                if(playtime == None):
                    is_ok = False
                    continue

				# 개봉일 없을 경우 제외
                if(len(date) == 0):
                    is_ok = False
                    continue
					
				# 줄거리 없을 경우 제외
                if(len(summary) == 0):
                    is_ok = False
                    continue
				
				# 사진 없을 경우 제외
                if(image == None):
                    is_ok = False
                    continue
				
				# 사진의 주소만 저장
                image = image.get("src")
				
				# 네티즌 평점 0.00, 없을 경우 제외 
                if(score_npro.text == "0.00" or score_npro.text == ""):
                    # print("111111111111")
                    is_ok = False
                    continue
					
				# 전문가 평점 0.00, 없을 경우 제외
                if(score_pro.text == "0.00" or score_pro.text == ""):
                    # print("222222222222")
                    is_ok = False
                    continue
					
				# 최종 확인
                if not(is_ok) :
                    continue
				
                # (6) ~~~~~ 이쁘게 출력 ~~~~~~~
                print("=" * 50)
                print(code)
                print("코드:", code)
				
                print("=" * 50)
                print("제목:", title.text)

                print("=" * 50)
                print("장르:")
                for g in genre:
                    print(g.text)

                print("=" * 50)
                print("나라:")
                for n in nation:
                    print(n.text)
				
                print("=" * 50)
                print("상영시간:")
                print(playtime.text)
				
                print("=" * 50)
                print("감독:")
                for d in directors:
                    print(d.text)

                print("=" * 50)
                print("주연 배우:")
                for a in actors:
                    if(a.text == "더보기"):
                        actors.remove(a)
                    else : 
                        print(a.text)
					
                print("=" * 50)
                print("관람 등급:")
                print(age.text)
				
                print("=" * 50)
                print("개봉일:")
                for d in date:
                    d = d.text
                    d = re.sub('[\s]', '', d)
                    print(d)
					
                print("=" * 50)
                for s in summary:
                    print(s.text)

                print("=" * 50)
                print("이미지:")
                print(image)
                
                
                #################
                # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                # 영화관련정보 엑셀(xlsx) 형식 저장
                # 데이터 만들기-1 : HTML로 가져온 영화장르/영화감독/영화배우 정보에서 TEXT정보만 뽑아서 리스트 형태로 만들기
                genre_list = [g.text for g in genre]
                # for g in genre_list:
                    # print(g)
                # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                # print(str(genre_list))
                nation_list = [n.text for n in nation]
                directors_list = [d.text for d in directors]
                actors_list = [a.text for a in actors]
                date_list = [d.text for d in date]
                summary_list = [s.text for s in summary]

                # 데이터 만들기-2 : 여러 개로 이루어진 리스트 형태를 하나의 문자열 형태로 만들기
                genre_str = ','.join(genre_list)
                nation_str = ','.join(nation_list)
                directors_str = ','.join(directors_list)
                actors_str = ','.join(actors_list)
                date_str = ''.join(date_list)
                summary_str = ','.join(summary_list)

                # age 숫자로 바꿔서 저장 "전체 관람가", "12세 관람가", "15세 관람가", "청소년 관람불가"
                if(age.text == '전체 관람가'):
                    age = 0
                elif(age.text == '12세 관람가'):
                    age = 12
                elif(age.text == '15세 관람가'):
                    age = 15
                elif(age.text == '청소년 관람불가'):
                    age = 19

                # 개봉일에서 모든 공백 제거
                date_str = re.sub('[\s]', '', date_str).replace('.', '-')
                # print("여기서")
                # 영화관련정보 엑셀 행 추가 : line by line 으로 추가하기(장르 리스트로 넣기 수정)
                sheet.append([code, title.text, genre_str, nation_str, int(playtime.text[0:-2]), directors_str, actors_str, age, date_str, summary_str, image, score_npro.text, score_pro.text])
                # print("에러낫겠지?")
            if is_ok == True:
                j = j + 1
				# basic_code_list에 code 저장
                basic_code_list.append(code)
				
            print(code, " : ", len(point_code_list), "개중에", point_code_list.index(code) + 1 , "번째 영화 체크 중", j, "개의 영화 정보저장 완료")
        # 엑셀 저장
    except:
        print("에러발생")
        wb.save("../crawling/data/basic4.xlsx")
    finally:
        print("완료")
		
		# 수집된 영화들 코드 리스트 파일 생성
        with open('../crawling/data/basic_code_list4.txt', 'w') as f:
            for code in basic_code_list:
                if code == basic_code_list[-1] :
                    f.write(code)
                else:
                    f.write(code + ",")
							
        wb.save("../crawling/data/basic4.xlsx")