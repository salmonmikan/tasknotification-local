import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import inspect
import dotenv

dotenv.load_dotenv() #.envからの環境変数のロード

options = Options() #関数に入れる

#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--hide-scrollbars')
#options.add_argument('--single-process')
options.add_argument('--ignore-certificate-errors')


USER_NAME = os.environ['USER_NAME']
PASS_WORD = os.environ['PASS_WORD']
URL = 'https://portal.tku.ac.jp/'
ERRORURL = 'https://portal.tku.ac.jp/portal/action/pt/f01/Uspt010111'


def get_manaba_report():
    driver_path = (os.path.dirname(os.path.abspath(__file__)))
    driver_path = os.path.join(driver_path, 'chromedriver')
    local_driver_path = "D:\code/tasknotification-local/chromedriver.exe"
    driver = webdriver.Chrome(executable_path= local_driver_path, options=options)
    driver.implicitly_wait(10)
    driver.get(URL)
    sleep(3)
    #警告ページが出た場合はリダイレクトボタンを押す
    if driver.current_url == ERRORURL :
        redirect_botton = driver.find_element(By.XPATH, '//*[@id="body"]/div/form/a')
        redirect_botton.click()
  
    else:
        try:
            # ログインページにてメールアドレス/パスワードを入力・「サインイン」をクリックを入力
            username_field = driver.find_element(By.XPATH, '/html/body/div/form/table[1]/tbody/tr[1]/td[2]/input')
            username_field.send_keys(USER_NAME)
            password_field = driver.find_element(By.XPATH, '/html/body/div/form/table[1]/tbody/tr[2]/td[2]/input')
            password_field.send_keys(PASS_WORD)
            signin_botton = driver.find_element(By.XPATH, '/html/body/div/form/table[1]/tbody/tr[4]/td/div/input')
            signin_botton.click()
            manaba_botton = driver.find_element(By.XPATH, '//*[@id="leftside"]/div[2]/div/div/div[1]/a')
            manaba_botton.click()

        except TimeoutException as t:
            print(t)
            pass

    driver.switch_to.window(driver.window_handles[1])
    course_list = driver.find_elements(By.CLASS_NAME, 'courselist-c')
    print("履修中：%sコマ" %(len(course_list))) #%sは%に置き換わる

    unsubmitted_list_botton = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div/div[5]/div[1]/div[2]/div/a')
    unsubmitted_list_botton.click()
    unsubmitted_list = driver.find_elements(By.XPATH, '//*[contains(@class, "row")]')
    print("未提出課題：%s個" %(len(unsubmitted_list))) #%sは%に置き換わる

    report_info = []
    count = 0
    print("---manaba取得課題一覧---")
    try:
        for unsubmitted in unsubmitted_list:
            report_title = driver.find_element(By.XPATH, '//tr[' + str(count+2) +']/td[2]/div/a').text
            report_title = ''.join(report_title.split()) #全角スペースの削除
            corse_name = driver.find_element(By.XPATH, '//tr[' + str(count+2) + ']/td[3]/div/a').text
            deadline = driver.find_element(By.XPATH, '//tr[' + str(count+2) + ']/td[5]').text
            deadline = datetime.strptime(deadline, '%Y-%m-%d %H:%M') #文字列を日付へ
            deadline = datetime.strftime(deadline, "%Y-%m-%dT%H:%M:00") #日付を文字列へ
            report_info.append((report_title,corse_name,deadline)) #2つ(ここでは3つ)の情報を1つにまとめた要素としてリストに格納する。 ex)[(要素a1,要素a2),(要素b1,要素b2),...]
            count += 1
    except TimeoutException as t:
        print(t)
        pass

    print(report_info)
    driver.quit()
    return report_info


if __name__ == '__main__':
    get_manaba_report()