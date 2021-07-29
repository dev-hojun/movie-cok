import re
import os
from random import randrange

import requests
from bs4 import BeautifulSoup as bs
import openpyxl
from urllib.request import urlretrieve

'''
(참고) 영화관련정보 엑셀(xlsx)형식 저장 컬럼 목록
    1) 영화제목
    2) 영화평점
    3) 영화장르
    4) 영화감독
    5) 영화배우
    6) 영화줄거리
    7) 영화포스터
    8) 영화코드번호
'''
'''
 코드 작성자
 박용태
 https://www.coalastudy.com/feed/1516

 코드 수정 사용
 2021-04-21
 박경태
 https://ktae23.tistory.com/
  
 수정 내용
 1. 영화 포스터 저장 시 파일명에 특수문자 제거를 위한 정규표현식 사용
 2. 평점이 없는 영화, 청소년 관람 불가, 배우 정보 없는 영화 건너뛰기
 3. 영화 줄거리 가져오기
 4. 영화 개봉일, 상영시간 가져오기
 5. 연습용 데이터를 위해 가격 정보 랜덤으로 만들어서 저장하기
 6. 이미지 파일을 imgs 디렉토리에 저장하기
 7. 예외처리를 통한 중간에 종료 될 경우에도 파일이 저장하기
'''

# 특수문자 제거 위한 함수
def cleanText(readData):
    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》 ]', '', readData)
    return text

def cleanScore (list):
    cleanScore = ""
    for l in list :
        cleanScore += l.text
    return cleanScore

def checkTag(tagList):
    for tag in tagList :
        if(tag == "") :
            is_ok = False
            break
        elif(tag == None) :
            is_ok = False
            break
        elif(tag.text == "0.0") :
            is_ok = False
            break

def crawling(start_code, finish_code):
    try:
        global is_ok
        is_ok = True
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["movie", "title", "score_npro", "score_pro", "score_m", "score_w", "score_10", "score_20", "score_30", "score_40", "score_50", "production", "acting", "story", "visual", "ost"])

        # (0) HTML 파싱
        # 저장 된 영화와 포스터의 행을 맞추기 위한 정수 j
        j = 0
        # 청소년 관람 불가, 평점 없는 영화 제외
        # 네이버영화의 영화 코드 범위 지정
        for i in range(start_code, finish_code):
            code = str(i)
            raw = requests.get("https://movie.naver.com/movie/bi/mi/point.nhn?code=" + code)
            html = bs(raw.text, 'html.parser')
			
            # (1) 전체 컨테이너
            movie = html.select("div.article")

            print(code, " : 코드")

            # (2) 전체 컨테이너가 갖고 있는 영화관련 정보
            for a, m in enumerate(movie):
                title = m.select_one("h3.h_movie a")
                score_npro_list = m.select(".score_left .star_score a em")
                score_npro = cleanScore(score_npro_list)
                score_pro_list = m.select(".obj_section .score_special .title_area .star_score em") 
                score_pro = cleanScore(score_pro_list)
                score_m = m.select_one("div.grp_male strong:nth-of-type(1)")
                score_w = m.select_one("div.grp_female strong:nth-of-type(1)")
                score_10 = m.select_one("div.grp_age div.grp_box:nth-of-type(1) strong:nth-of-type(2)")
                score_20 = m.select_one("div.grp_age div.grp_box:nth-of-type(2) strong:nth-of-type(2)")
                score_30 = m.select_one("div.grp_age div.grp_box:nth-of-type(3) strong:nth-of-type(2)")
                score_40 = m.select_one("div.grp_age div.grp_box:nth-of-type(4) strong:nth-of-type(2)")
                score_50 = m.select_one("div.grp_age div.grp_box:nth-of-type(5) strong:nth-of-type(2)")
                production = m.select_one("ul.grp_point li:nth-of-type(1) span")
                acting = m.select_one("ul.grp_point li:nth-of-type(2) span")
                story = m.select_one("ul.grp_point li:nth-of-type(3) span")
                visual = m.select_one("ul.grp_point li:nth-of-type(4) span")
                ost = m.select_one("ul.grp_point li:nth-of-type(5) span")
                
                tagList = [title, score_m, score_w, score_10, score_20, score_30, score_40, score_50, production, acting, story, visual, ost]
				
                if(score_npro == "0.0" or score_npro == ""):
                    is_ok = False
                if(score_pro == "0.0" or score_pro == ""):
                    is_ok = False
					
                # checkTag(tagList)
                for tag in tagList :
                    if(tag == "") :
                        is_ok = False
                        break
                    elif(tag == None) :
                        is_ok = False
                        break
                    elif(tag.text == "0.0") :
                        is_ok = False
                        break
						
                if not(is_ok) :
                    continue
                
                # (6) ~~~~~ 이쁘게 출력 ~~~~~~~
                print("=" * 50)
                print("코드:", code)
				
                print("=" * 50)
                print("제목:", title.text)

                print("=" * 50)
                print("네티즌 평점:")
                print(score_npro)

                print("=" * 50)
                print("전문가 평점:")
                print(score_pro)
				
                print("=" * 50)
                print("남자 평점:")
                print(score_m.text)
				
                print("=" * 50)
                print("여자 평점:")
                print(score_w.text)
				
                print("=" * 50)
                print("10대 평점:")
                print(score_10.text)
				
                print("=" * 50)
                print("20대 평점:")
                print(score_20.text)
				
                print("=" * 50)
                print("30대 평점:")
                print(score_30.text)
				
                print("=" * 50)
                print("40대 평점:")
                print(score_40.text)
				
                print("=" * 50)
                print("50대 평점:")
                print(score_50.text)
				
                print("=" * 50)
                print("연출:")
                print(production.text)
				
                print("=" * 50)
                print("연기:")
                print(acting.text)
				
                print("=" * 50)
                print("스토리:")
                print(story.text)
				
                print("=" * 50)
                print("영상미:")
                print(visual.text)
				
                print("=" * 50)
                print("ost:")
                print(ost.text)
				
                # (7-3) 영화관련정보 엑셀 행 추가 : line by line 으로 추가하기
                sheet.append([code, title.text, score_npro, score_pro, score_m.text, score_w.text, score_10.text, score_20.text, score_30.text, score_40.text, score_50.text, production.text, acting.text, story.text, visual.text, ost.text])

                is_ok = True
            if is_ok == True:
                j = j + 1
            print(finish_code - start_code, "개중에", finish_code - i - 1, "개 남음")
            print(i + 1 - start_code, "번째 영화 체크 중", j, "개의 영화 정보저장 완료")
        # (9) 엑셀 저장
    except:
        print("에러발생")
        wb.save("navermovie_point2.xlsx")
    finally:
        print("완료")
        wb.save("navermovie_point2.xlsx")