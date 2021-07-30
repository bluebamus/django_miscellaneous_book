from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# reference : https://wikidocs.net/11060

# 웹 드라이버매니저 이용
# 버전 변경에 상관없이 현재 OS에 설치된 크롬브라우저를 사용합니다.

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('http://localhost:8000')

assert 'Django' in browser.title

# 위와 같이 assert 문을 작성하기보다 에러 메시지를 친절하게 확인할 수 있도록 아래와 같이 코드를 수정할 수 있다.

# assert 'Django' in browser.title, "Browser title was " + browser.title

# command : python test_selenium_basic_ex.py