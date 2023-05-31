from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import psycopg2
import time

class Crawler:
    
    def read(self):
    
        start_date = "2023-04-01"
        date_format = "%Y-%m-%d"

        #크롬 드라이버로 웹 브라우저 실행
        path = "C:\chromedriver_win32\chromedriver.exe"
        driver = webdriver.Chrome()
        driver.get("https://www.i-sh.co.kr/main/lay2/program/S1T294C295/www/brd/m_241/list.do")
        time.sleep(4)

        #시작날짜 입력창을 찾아 start_date 입력
        element = driver.find_element(By.ID, 'srchFr')
        element.click()
        element.send_keys(start_date)
        time.sleep(2)

        #조회 버튼을 클릭
        btn_area = driver.find_element(By.CLASS_NAME,'btn-area')
        tag_a = btn_area.find_element(By.TAG_NAME,'a')
        driver.execute_script("arguments[0].click()", tag_a)

        #데이터 파싱 loop 시작
        flag = 1
        current_page = 1
        input_data = []
        while flag == 1:
            #paging 처리를 위한 변수 세팅
            paging_area = driver.find_element(By.CLASS_NAME,'pagingWrap')
            list_a = paging_area.find_elements(By.TAG_NAME,'a')
            
            #데이터 파싱
            list_table = driver.find_element(By.ID, 'listTb')
            list_tbody = list_table.find_element(By.TAG_NAME,'tbody')
            list_tr = list_tbody.find_elements(By.TAG_NAME,'tr')
            for tr in list_tr:
                print("================")
                list_td = tr.find_elements(By.TAG_NAME,'td')
                values = [
                    int(list_td[0].text),
                    str(list_td[1].text),
                    str(list_td[2].text),
                    datetime.strptime(list_td[3].text, date_format),
                    int(list_td[4].text)
                ]
                input_data.append(values)
                print(list_td[0].text)
                print(list_td[1].text)
                print(list_td[2].text)
                print(list_td[3].text)
                print(list_td[4].text)
                
            #마지막 페이지 여부 확인
            page_count_str = driver.find_element(By.CLASS_NAME,'mentcount').text
            print(page_count_str)
            str_tmp1 = page_count_str.split('[')
            str_tmp2 = str_tmp1[1].split('페')
            str_tmp3 = str_tmp2[0].split('/')
            if int(str_tmp3[0]) == int(str_tmp3[1]):
                break

            #다음페이지 이동
            for a in list_a:
                if a.text == "첫페이지":
                    print("skip")
                elif a.text == "이전페이지":
                    print("skip")
                elif a.text == "다음페이지":
                    print("=====next page=====")
                    driver.execute_script("arguments[0].click()", a)
                    current_page = current_page + 1
                    print(current_page)
                    break
                elif a.text == "마지막페이지":
                    break
                elif int(a.text) > current_page:
                    print("=====next page=====")
                    current_page = int(a.text)
                    driver.execute_script("arguments[0].click()", a)
                    print(current_page)
                    break
            time.sleep(2)
            
        self.write(input_data)

    def write(self, input_data):
        #DB 저장    
        db = psycopg2.connect(host='localhost', dbname='postgres',user='daewoong',password='',port=5432)
        cursor = db.cursor()

        query = "truncate table tb_sh_notice"
        cursor.execute(query)
        query = "INSERT INTO tb_sh_notice(seq,title,dep_nm,first_cret_dt,inq_cnt)values(%s,%s,%s,%s,%s)"
        cursor.executemany(query, input_data)
        db.commit()
            
        db.close()