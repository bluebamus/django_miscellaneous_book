# 쿼리의 Q 모델을 활용한 검색 기능 구현
## Q 객체를 사용한 복잡한 조회
### 부제: 검색 조건이 복잡하면 Q models 를 불러와서 정의하자.
* Post.objects.filter() 는 AND 연산자가 포함이 된다. 그렇기 때문에 OR 문을 실행해야 하는 경우에는 Q objects 를 사용
  * 즉, A 와 B 를 포함하는 모든 검색 조건에 대해서 검색하라. 라는 것이 Q 객체를 사용하는 이유
```python
from django.db.models import Q

Q(question__startswith='What')
```
* Q objects 는 & 와 |(파이프라인: or 연산자) 의 사용이 가능하다. 
  * 연산자가 두 개의 Q 객체에 사용되면 새로운 Q 객체가 생성
* 예를 들어, 아래의 예제는 2개의 question__startswith 쿼리의 OR 을 나타내는 단일 Q 객체를 생성한다.
```python
Q(question__startswith='Who' | Q(question__startswith='What')
```
```python
# 이것은 아래의 SQL WHERE 절과 동일하다.
WHERE question LIKE 'Who%' OR question LIKE 'What%'
```
* Q objects 를 & 와 |(파이프라인) 으로 결합하여 임의의 복잡성을 갖는 문장을 작성.
  * 연산자 및 괄호 그룹화를 사용하는데, Q objects 는 '~' 연산자를 사용하여 무효화할 수 있으므로 일반 쿼리와 부정(NOT) 쿼리를 결합한 조회를 허용
```python
Q(question__startswith='Who' | ~Q(pub_date__year=2005)
```
* 키워드 인수(filter(), exclude(), get()) 을 사용하는 각 조회 함수는 하나 이상의 Q objects 를 위치 지정되지 않은 인수로 전달할 수 있다.
* 조회 함수에 여러 개의 Q objects 인수를 제공하면 인수가 AND 가 된다.
```python
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
```
```python
# SQL 문으로 작성
SELECT * from polls WHERE question LIKE 'Who%'
   AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
```
* 조회 함수(Lookup functions) 는 Q objects 와 키워드 인수의 사용을 혼합할 수 있다.
* 조회 함수에 제공된 모든 인수(키워드 인수 또는 Q objects) 는 함께 AND 된다.
* 그러나 Q objects 가 제공되면 키워드 인수의 정의 앞에 와야 한다.
  * (1순위) 모든 조건에 해당하는 검색조건 (2순위) 연산자가 들어간 상세 조건

```python
# 올바른 예시
Poll.objects.get(
   question__startswith='Who',
   Q(pub_date=date(2005, 5, 2) | pub_date=date(2005, 5, 6)),
)
```
```python
# 잘못된 예시
# INVALID QUERY
Poll.objects.get(
    Q(pub_date=date(2005, 5, 2) | pub_date=date(2005, 5, 6)),
    question_startswith='Who',
)
```
# Q object 이용해 조건에 맞는 데이터 불러오기
* Q 객체를 사용해서 and, or, not 연산을 이용한 조건을 걸어서 데이터를 가져오는 방법
```python
from django.db.models import Q           		#[1]
from django.forms.models import model_to_dict	        #[2]

#1  or 
obj = User.objects.filter(Q(name_kr__startswith = '김') | Q(account_number__endswith = '7'))   #[3]
model_to_dict(obj[0])                			#[4]

#2 and
obj2 = User.objects.filter(Q(birth = '1505-03-13') & Q(gender = 1)) #[5]
model_to_dict(obj2[0])					#[6]

#3 not
obj3 = User.objects.filter(Q(birth__startswith = '1999') & ~Q(name_eng = 'kukudas')) #[7]
model_to_dict(obj3[0]) 					#[8]
```
1. 데이터에 조건을 걸기 위해 Q 모듈을 import 한다
2. 객체를 딕셔너리 형식으로 변환해 출력해주는 모듈을 import 한다
3. user 테이블에서 name_kr이 '김'으로 시작하거나 account_number가 7로 끝나는 데이터들을 obj라는 객체에 담았다.
4. obj에서 0번째에 있는 객체를 딕셔너리 형식으로 출력해줘서 결과를 보기 편하다.
```python
# 출력 예시
{'id': 1, 
'grade': 1, 
'account_number': '10147747', 
'account': 'aaa1234', 
'name_kr': '에이',
 중간 생략}
```
5. user테이블에서 생일이 1505년 3월 13일 이고 gender id가 1인 데이터를 소환하기 위한 조건을 걸었다.
6. 출력 예시
```python
# 출력 예시
{'id': 11, 
'grade': 1, 
'account_number': '10147757', 
'birth': datetime.date(1505, 3, 13), 
'gender': 1, 
 중간 생략 }
```
7. 출생년도가 1999년이면서 영어이름이 kukudas가 아니어야 한다는 조건을 걸었다. not은 ~ 라고 표시하면 된다.
8. 출력 예시
```python
# 출력 예시
{'id': 1, 
'grade': 1, 
'account_number': '10147747', 
'account': 'aaa1234',
'name_kr': '에이', 
'name_eng': 'a', 
'birth': datetime.date(1999, 1, 1)
 중간 생략 }
```
* 이와 비슷하게 exclude 라는 것도 사용할 수 있다.
```python
Point.objects.filter(user = 33).exclude(saved_point = 313)
```
* filter처럼 사용할 수 있는데, 위 코드는 포인트 테이블에서 user_id가 33인 데이터 중에서 saved_point가 313인 데이터는 제외한 나머지 데이터를 출력한다
# Django Q 객체
* &를 사용하면 where 조건 and 조건이고, |를 사용하면 where 조건 or 조건이다.
* where 조건 and 조건 => 조건 둘다를 만족하는 결과값만 보여준다. 즉 교집합 
  * where 조건 or 조건 => 조건들중 하나라도 조건에 맞으면 그 결과 값을 전부 다 보여준다. 즉 합집합
```python
#sql 쿼리문
select * from product where category=소 or sub_category=등심

# 장고 orm
Product.objects.filter(Q(category=소) | Q(sub_category=등심))
```

> reference : [쿼리의 Q 모델을 활용한 검색 기능 구현](https://dev-mht.tistory.com/62)
> reference : [Q object 이용해 조건에 맞는 데이터 불러오기](https://velog.io/@anrun/Q-object)
> reference : [Django Q 객체](https://velog.io/@jxxwon/Django-Q-%EA%B0%9D%EC%B2%B4)