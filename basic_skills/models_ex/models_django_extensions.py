# 공식 문서 : https://django-extensions.readthedocs.io/en/latest/

# 가장 많이 사용되는 명령어들

# @ shell_plus

# Django shell with autoloading of the apps database models and subclasses of user-defined classes.
# tab 키를 이용한 자동 완성

# 실행
# python manage.py shell_plus --ipython


# @ create_command

# Creates a command extension directory structure within the specified application. 
# This makes it easy to get started with adding a command extension to your application.

# 해당 기능은 따로 살표볼 필요가 있음


# @ graph_models

# Creates a GraphViz dot file. You need to send this output to a file yourself. 
# Great for graphing your models. 
# Pass multiple application names to combine all the models into a single dot file.

# 진행 중이던 django 프로젝트에 참여하게 되었을 때, 
# 그 프로젝트를 가장 빨리 이해하는 방법은 models.py를 파악하는 것입니다. 
# 대부분의 로직들이 models에서 관리되기 때문입니다. 
# 코드를 단순히 읽는 것보다도 graph로 각 모델 간의 관계를 그림으로 표현해 줍니다.

# 전체 혹은 선택적으로 그릴 수 있음
# 참고 : https://blog.isaccchoi.com/programing/Django-ERD-%EB%A7%8C%EB%93%A4%EA%B8%B0/

# 실행
# $ ./manage.py graph_models -a > my_project.dot # 문제 없음

# graphviz를 이용해 더 좋은 이미지 생성

# 전체 모델에 대한 그래프 출력 $ python manage.py graph_models -a -g -o models.png
# 특정 앱에 대한 그래프 출력 $ python manage.py graph_models board -o models.png

# python manage.py graph_models your_app your_model -o /tmp/models.png
# or 
# python manage.py graph_models -a -g -o my_project_visualized.png

# 위 두 방식 다 에러가 남, 윈도우에서의 문제
# 해결책 pip install --global-option = build_ext --global-option = "-IC : \ Program Files (x86) \ Graphviz2.38 \ include"--global-option = "-LC : \ Program Files (x86) \ Graphviz2 .38 \ lib \ release \ lib "pygraphviz
# 하지만 해결 안됨, 똑같이 적어서는 안되고 내 시스템의 경로와 비교하여 수정해야함
# 리눅스에서 차후에 시도해 보기로함
# 참고 https://pythonq.com/so/python/1769802



# @ admin_generator app : app의 관리자 화면을 생성해 줍니다.

# @ clean_pyc : *.pyc 파일을 모두 지워 줍니다. settings.py에 BASE_DIR을 설정해야 합니다.
# 세부 명령어 참고 : https://c10106.tistory.com/4066

# @ notes : 파이썬 파일에 적어둔 # TODO: 주석들을 찾아 표시합니다.

# @ pipchecker : 사용 중인 패키지의 업데이트 현황을 알려줍니다.

# @ runserver_plus : 기본 웹 서버보다 향상된 웹 서버를 띄웁니다. 
# 서버 오류가 발생하면 웹 상에서 바로 디버깅할 수 있습니다. Werkzeug를 설치해야 합니다.

# @ shell_plus : INSTALLED_APP에 설치된 앱의 모델들이 import된 셸을 띄웁니다
# (ipython과 함께 사용하면 더 편합니다).