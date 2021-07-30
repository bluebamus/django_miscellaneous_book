import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# reference : https://wikidocs.net/11061

# @ 폼으로 POST 요청 전송

'''
@ 바로 브라우저가 닫히면서 정확히 그 내용을 확인하기도 어렵다. 
  이런 경우 디버깅을 위해 아래와 같은 방법이 있다.

- print 문을 이용해 현재 페이지의 텍스트를 출력한다.
- 에러가 발생한 이유를 좀 더 자세히 알 수 있도록 에러 메시지를 출력한다.
- 사이트를 직접 수동으로 방문한다.
- time.sleep에 충분한 시간을 두어 에러 이유를 확인할 수 있도록 한다.
'''

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 영애씨는 온라인 일정관리 앱을 알게 되어 홈페이지에 방문한다.
        self.browser.get('http://localhost:8000/testcaseskills/homepost/')

        # 홈페이지에 방문해 보니 제목이 "일정관리"인 것을 보고 홈페이지에 올바르게 방문한 것을 확인한다.
        # assert '일정관리' in self.browser.title, "Browser title was " + self.browser.title
        self.assertIn('일정관리', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('일정목록', header_text)

        # 일정을 입력할 수 있는 페이지로 바로 이동한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '할일을 입력하세요')

        # 영애씨는 생일날 미역국을 끓이기 위해 텍스트박스에 "시장에서 미역 사기"를 입력한다.
        inputbox.send_keys('시장에서 미역 사기')

        # 영애씨가 엔터를 입력하면 페이지를 새로고침해서 모든 일정 목록을 보여준다.
        # "1: 시장에서 미역 사기"가 첫 번째 할일로 일정 목록에서 보여진다.
        inputbox.send_keys(Keys.ENTER)
        # ! 대기 시간값을 늘림
        time.sleep(10) # {% csrf_token %}가 없어서 발생하는것 확인 후 수정
        #time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        
        self.assertTrue(any(row.text == '1: 시장에서 미역 사기' for row in rows))
        #단순히 에러 메시지만 출력하면 나중에 디버깅하기 어려우므로 
        # 아래와 같이 테이블의 내용을 함께 출력하도록 수정할 수 있다.

        self.assertTrue(
            any(row.text == '1: 시장에서 미역 사기' for row in rows),
            "New to-do item did not appear in table. Contents were:\n{}".format(table.text),
        )
        
        # 영애씨는 추가로 할일 텍스트박스에 입력할 수 있고
        # "미역을 물에 불리기"라고 입력한다.
        self.fail('테스트 종료')

        # 다시 페이지를 새로고침해서 입력한 일정 두 가지 모두 목록에 표시한다.

        # 영애씨는 일정 목록이 사이트에 올바로 저장되었는지 궁금해서
        # 고유 URL 생성을 확인한다.

        # 영애씨는 URL을 방문하고 일정 목록이 올바르게 있음을 확인한다.

        # 영애씨는 이제 만족하고 잠을 자러간다.


if __name__ == '__main__':
    unittest.main(warnings='ignore')