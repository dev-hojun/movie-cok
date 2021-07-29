import re
import os
from random import randrange

import requests
from bs4 import BeautifulSoup as bs
import openpyxl
from urllib.request import urlretrieve

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
        is_ok = True
        wb = openpyxl.Workbook()
        sheet = wb.active
        final_code_list = []
        basic_code_list = []
		
		# basic_code_list 에서 수집한 영화 코드 리스트 파일 가져오기
        with open('../crawling/data/basic_code_list.txt', 'r') as text_file:
            basic_code_list = text_file.readline().split(",")
		
		# 항목 : 코드, 네티즌평점, 전문가평점, 남자평점, 여자평점, 10대평점, 20대평점, 30대평점, 40대평점, 50대평점, 연출, 연기, 스토리, 영상미, 배경음악
        sheet.append(["movie", "score_npro", "score_pro", "score_m", "score_w", "score_10", "score_20", "score_30", "score_40", "score_50", "production", "acting", "story", "visual", "ost"])

        # HTML 파싱
        # 저장 된 영화 개수
        j = 0
        
		# baic_code_list로 코드범위 지정
        for code in basic_code_list:
            is_ok = True
            raw = requests.get("https://movie.naver.com/movie/bi/mi/point.nhn?code=" + code)
            html = bs(raw.text, 'html.parser')
			
            # 전체 컨테이너
            movie = html.select("div.article")
            
            # print("준비@@@@@@@@@@@@@@@@@@@@@")
			
			# 성인 인증 필요한 영화 제외
            if(len(movie) == 0):
                # print("00000000000000000")
                is_ok = False
				
            # 전체 컨테이너가 갖고 있는 영화관련 정보
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
				
                # print("시작!!!!!!!!!!!!!!!!!!!!!!!!")
				# 유효성 검사
				# 네티즌 평점 0.00, 없을 경우 제외 
                if(score_npro == "0.00" or score_npro == ""):
                    # print("111111111111")
                    is_ok = False
                    continue
					
				# 네티즌 평점 0.00, 없을 경우 제외
                if(score_pro == "0.00" or score_pro == ""):
                    # print("222222222222")
                    is_ok = False
                    continue
				
				# 기타 태그들 없을 경우, 0.0일 경우 제외
                for tag in tagList :
                    if(type(tag) == None or tag.text == "" or tag.text == "0.0") :
                        # print("33333333333333")
                        is_ok = False
                        break
				
                # print("여기???????????????????")
				# 감상 포인트 모두 0이면 제외
                if(int(production.text[0:-1])+int(acting.text[0:-1])+int(story.text[0:-1])+int(visual.text[0:-1])+int(ost.text[0:-1]) == 0):
                    # print("444444444444444")
                    is_ok = False
                    continue
				
				# 최종 확인
                if not(is_ok) :
                    continue
                
                # 수집된 데이터 출력
                print("=" * 50)
                print("코드:", code)
				
                print("=" * 50)
                print("네티즌 평점:")
                # print(type(score_npro))
                print(score_npro)
				
                print("=" * 50)
                print("전문가 평점:")
                # print(type(score_pro))
                print(score_pro)
				
                print("=" * 50)
                print("남자 평점:")
                # print(type(score_m))
                print(score_m.text)
				
                print("=" * 50)
                print("여자 평점:")
                # print(type(score_w))
                print(score_w.text)
				
                print("=" * 50)
                print("10대 평점:")
                # print(type(score_10))
                print(score_10.text)
				
                print("=" * 50)
                print("20대 평점:")
                # print(type(score_20))
                print(score_20.text)
				
                print("=" * 50)
                print("30대 평점:")
                # print(type(score_30))
                print(score_30.text)
				
                print("=" * 50)
                # print(type(score_40))
                print(score_40.text)
				
                print("=" * 50)
                print("50대 평점:")
                # print(type(score_50))
                print(score_50.text)
				
                print("=" * 50)
                print("연출:")
                # print(type(production))
                print(production.text[0:-1])
				
                print("=" * 50)
                print("연기:")
                # print(type(acting))
                print(acting.text[0:-1])
				
                print("=" * 50)
                print("스토리:")
                # print(type(story))
                print(story.text[0:-1])
				
                print("=" * 50)
                print("영상미:")
                # print(type(visual))
                print(visual.text[0:-1])
				
                print("=" * 50)
                print("ost:")
                # print(type(ost))
                print(ost.text[0:-1])
				
                # 영화관련정보 엑셀 행 추가 : line by line 으로 추가하기
                sheet.append([code, score_npro, score_pro, score_m.text, score_w.text, score_10.text, score_20.text, score_30.text, score_40.text, score_50.text, production.text[0:-1], acting.text[0:-1], story.text[0:-1], visual.text[0:-1], ost.text[0:-1]])

            if is_ok == True:
                j = j + 1
				# final_code_list에 code 저장
                final_code_list.append(code)
			
            print(code, " : ", len(basic_code_list), "개중에", basic_code_list.index(code) + 1 , "번째 영화 체크 중", j, "개의 영화 정보저장 완료")
        # 엑셀 저장
    except:
        print("에러발생")
        wb.save("../crawling/data/final2.xlsx")
    finally:
        print("완료")
		
		# 수집된 영화들 코드 리스트 파일 생성
        with open('../crawling/data/final_code_list.txt', 'w') as f:
            for code in final_code_list:
                if code == final_code_list[-1] :
                    f.write(code)
                else:
                    f.write(code + ",")
					
        wb.save("../crawling/data/final2.xlsx")