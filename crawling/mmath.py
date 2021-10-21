from selenium import webdriver
from seleniumrequests import Chrome
import json
import pandas as pd

def createSessoin():
    """
    크롤링을 하기 위한 크롬 세션 생성
    :return:
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    chrome = Chrome('./driver/chromedriver', chrome_options=options)

    return chrome


def readMmathConfig(user):
    """
    config.json 설정값 읽기
    :param user: 로그인하려는 유저 종류
    :return:
        id : 로그인하려는 유저 id
        pw : 로그인하려는 유저 pw
    :example:
        ('idid', 'pwpw')
    """
    with open('config.json', 'r') as f:
        config = json.load(f)
    id = config['MMATH'][f'{user}']['ID']
    pw = config['MMATH'][f'{user}']['PW']
    return id, pw

def loginMmath(id, pw):
    """
    메타수학에 로그인
    :param id: 입력할 id
    :param pw: 입력할 pw
    :return:
        s :로그인완료된 크롬 세션
    """
    s = createSessoin()
    s.implicitly_wait(3)
    s.get("https://www.mmath.co.kr/n/center/login")
    login_x_path = '/html/body/div[1]/div/div[1]/form/a'
    s.find_element_by_name('f_web_id').send_keys(id)
    s.find_element_by_name('f_web_pw').send_keys(pw)
    s.find_element_by_xpath(login_x_path).click()

    return s

def quitSession(session):
    """
    세션 종료
    :param session: 종료하려는 세션
    :return:
    """
    session.quit()

def requestResponsToDataFrame(s, url):
    """
    url을 'GET'으로 요청하여 json형태를 응답받아 데이터프레임형식으로 반환
    :param s: 요청을 보내려는 세션
    :param url: 데이터 요청 url
    :return: DataFrame형식의 응답


    """
    r = s.request('GET', url)
    response_dic = json.loads(r.text)
    return pd.DataFrame(data=response_dic['rows'])

def loadStudentClassData(s):
    """
    메타수학의 학생 정보, 반 정보, 선생님 정보 불러오기
    :param s: 로그인된 세션
    :return: 데이터프레임 형식의 데이터
    example:
               f_user_id f_user_nm f_grade_cd  ... f_group_id f_group_nm f_teacher_id
        0      80867   0619김현수       GRM1  ...          0        미지정          NaN
        1      80860   0619박신아       GRM1  ...          0        미지정          NaN
        2      80859   0619박신영       GRM1  ...          0        미지정          NaN
        3      80804   0619박진원       GRE6  ...          0        미지정          NaN
        4      80864   0619박한나       GRM1  ...          0        미지정          NaN
        5      80868   0619서윤희       GRM1  ...          0        미지정          NaN
    """
    url = 'https://www.mmath.co.kr/common/site.ajax.cshtml?act=grpstdlist4tree&f_state_cd=MS10'
    return requestResponsToDataFrame(s, url)


def filteringTeacherId(df):
    return 0



if __name__ == '__main__':

    id, pw = readMmathConfig('MASTER')
    mmathSession = loginMmath(id, pw)
    baseData = loadStudentClassData(mmathSession)
    quitSession(mmathSession)

    

    print('t')

