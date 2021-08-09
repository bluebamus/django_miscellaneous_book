# 테스트 방법

> commander : python manage.py shell_plus --print-sql --ipython

# 쿼리셋의 활용

## Iteration 

* 쿼리셋은 전체 데이터를 순회가능한 형태로 가진다.

```python
for e in Blog.objects.all():
    print(e.name)
```

## len()
* 쿼리셋의 결과 데이터에 대한 길이값을 반환한다. 단순히 길이값만 필요하다면 장고에서 제공해주는 count()함수를 사용하는 것이 더 바람직하다.

## list()
```python
entry_list = list(Blog.objects.all())
```

## bool()
* bool() 결과값이 하나라도 존재하면 True를 반환하면 아니면 False를 반환한다.
```python
if Blog.objects.filter(name="modi"): # False
   ...:    print("There is at least one Entry with the headline Test")

if Blog.objects.filter(name="하수진"): # True
   ...:    print("There is at least one Entry with the headline Test")   
```

# 쿼리셋을 반환하는 메소드

## filter()
* 기존의 QuerySet정보를 다시 만들기 위해서 따로 저장해두었다가 필요할 때 사용할 수 있다.
```python
Blog.objects.filter(name__startswith='하')
# 결과 확인
Blog.objects.filter(name__startswith='하').values_list()

<QuerySet [(13, '하수진'), (27, '하수빈')]>
```

## exclude()
* filter()와 반대로 동작한다.
```python
Blog.objects.exclude(name__startswith='하')  
# 결과 확인
Blog.objects.exclude(name__startswith='하').values_list()

<QuerySet [(1, '장주원'), (2, '이영자'), (3, '배정식'), (4, '김영희'), (5, '윤서준'), (6, '김지연'), (7, '오정훈'), (8, '백준혁'), (9, '홍옥자'), (10, '김영호'), (11, '박지원'), (12, '이정자'), (14, '김지현'), (15, '이지현'), (16, '김아름'), (17, '진영길'), (18, '이미정'), (19, '김
보람'), (20, '김도윤'), (21, '이주원'), '...(remaining elements truncated)...']>
```

* 괄호안에 동시에 조건을 적용하면 AND연산처럼 동작한다.

```python
Post.objects.exclude(writer__startswith='이', ip_address__icontains='192')
# 결과 확인
Post.objects.exclude(writer__startswith='이', ip_address__icontains='192').values('writer','ip_address')

<QuerySet [{'writer': '류상현', 'ip_address': '10.54.98.57'}, {'writer': '김경희', 'ip_address': '172.21.152.10'}, {'writer': '홍명자', 'ip_address': '10.159.179.145'}, {'writer': '민서윤', 'ip_address': '192.168.155.244'}, {'writer': '남건우', 'ip_address': '172.28.140.34'}, {'writer': '주아름', 'ip_address': '172.24.125.10'}, {'writer': '이현지', 'ip_address': '10.248.160.25'}, {'writer': '이승민', 'ip_address': '172.30.15.117'}, {'writer': '송도윤', 'ip_address': '172.21.109.236'}, {'writer': '김현숙', 'ip_address': '10.142.105.184'}, {'writer': '송예지', 'ip_address': '10.125.50.117'}, {'writer': '박민지', 'ip_address': '172.23.24.183'}, {'writer': '최민서', 'ip_address': '10.107.22.42'}, {'writer': '김영호', 'ip_address': '172.30.98.251'}, {'writer': '주윤서', 'ip_address': '192.168.159.169'}, {'writer': '한서연', 'ip_address': '192.168.114.65'}, {'writer': '강성훈', 'ip_address': '10.119.12.61'}, {'writer': '노옥자', 'ip_address': '172.23.209.93'}, {'writer': '김정순', 'ip_address': '192.168.10.18'}, {'writer': '서상호', 'ip_address': '192.168.147.235'}, '...(remaining elements truncated)...']>
```
* 괄호 밖에 새로 .exclude를 지정하면 OR연산처럼 작동한다.
```python
Blog.objects.exclude(name__startswith='하').exclude(name__startswith='김')
# 결과 확인
Blog.objects.exclude(name__startswith='하').exclude(name__startswith='김').values_list()

<QuerySet [(1, '장주원'), (2, '이영자'), (3, '배정식'), (5, '윤서준'), (7, '오정훈'), (8, '백준혁'), (9, '홍옥자'), (11, '박지원'), (12, '이정자'), (15, '이지현'), (17, '진영길'), (18, '이미정'), (21, '이주원'), (22, '장미경'), (23, '박현정'), (24, '백영수'), (25, '황종수'), (26, '이정훈'), (28, '진재현'), (29, '송옥순'), '...(remaining elements truncated)...']>
```

## distinct()
* SQL문법에서 SELECT DISTINCT를 사용하는 새로운 QuerySet을 리턴한다. 이렇게 하면 쿼리 결과에서 중복 행이 제거된다.
* 쿼리가 여러 테이블을 걸쳐야 한다면 중복되는 결과를 얻을 수 있다 이럴때 distinct()를 사용한다.
* ! PostgreSQL에서는 distinct()에 Positional arguments를 전달 할 수 있다. 이때 인자 값은 필드 값이다. 이것은 SELECT DISTINCT ON과 같은 SQL쿼리로 변환된다 하지만 Raw SQL과 차이점이 존재하는데 일반적인 distinct()호출의 경우 데이터 베이스는 구별되는 행을 결정할 때 각 행의 각 필드를 비교한다. 하지만 ORM에서는 지정된 필드를 인자로 갖는 distinct()호출의 경우 데이터베이스가 지정된 필드 이름만 비교한다.
* 필드를 인수로 갖는 distinct()
  * 필드 이름을 지정할 때 QuerySet에는 order_by()가 필요하며 order_by()의 필드는 distinct()에 제공된 필드와 동일하게 지정되어야 한다.
  * 예를들어 SELECT DISTINCT ON (a)는 a열의 각 값에 대한 첫 번째 행을 제공한다. 만약 ordering이 되어 있지 않다면 임의의 행이 리턴된다.
* ! DB 종류에 따라 적용이 안될 수도 있고 사용 방법이 상이할 수 있으니 확인이 필요하다.


## annotate()
* 제공된 쿼리 식 목록을 사용하여 QuerySet의 각 객체에 주석을 추가한다. 식은 단순 값, 모델의 필드에 대한 참조 (또는 모든 관계 모델), 또는 객체와 관련된 객체에 대한 계산된 집계 식 (평균, 합계 등)일 수 있다.
* annotate()의 각 인수는 반환되는 QuerySet의 각 객체에 추가되는 주석이다.
* **kwargs를 사용하여 지정된 주석은 키워드 주석의 별칭으로 사용된다. 익명 인수에는 집계 함수의 이름과 집계되는 모델 필드에 따라 생성된 별칭이 있다. 단일 필드를 참조하는 집계식만 익명 인수가 될 수 있다. 그 밖에 모든 것은 키워드 인수여야 한다.

* 새로운 요소를 데이터 쿼리에 추가하고 해당 요소를 따로 출력해볼 수 있도록 해준다. 
  * 데이터가 몇 개 존재하는지를 count라는 함수를 이용하여 annotate해주고 이를 __count로 접근할 수 있다.

```python
from django.db.models import Count
q = Post.objects.annotate(Count('writer'))
q[0].writer
q[0].writer__count
q.filter(writer="이예지").values("ip_address")

# alias 지정 가능
q = Post.objects.annotate(number_of_entries=Count('writer'))
q[0].number_of_entries
```

## reverse()
* 쿼리셋의 순서를 반대로 바꾼다.
  * 기존에 가지고 있던 정렬순서를 reverse()가 반대로 바꾸고 처음부터 5개의 데이터를 슬라이싱한다.
  * 장고에서는 슬라이싱에서 음수를 지원하지 않기 때문에  [-5:0]과 같은 효과를 사용할때 쓴다.
  * ordering 옵션을 명시해주지 않은 상태에서는 reverse가 동작하지 않는다.
```python
q.reverse()[:5]
# 결과 값 확인
q.reverse()[:5].values()
```

## values_list()
* flat=True라는 옵션을 추가하면 튜플이 제거되고 일반 리스트에 데이터가 하나씩 들어있는 형태로 반환된다.
* 하나의 필드이름에 대해서만 flat이 적용되기 때문에 여러개의 필드이름이 flat과 함께 사용될 수 없다.
* 특정 데이터를 추출할 때 get을 함께 사용할 수 있다.

```python
Post.objects.values_list('id').order_by('id')
Post.objects.values_list('id', flat=True).order_by('id')
Post.objects.values_list('writer', flat=True).get(pk=5)
```

* named = True를 전달하여 namedtuple()을 결과로 얻을 수 있다.
  * namedtuple()을 이용하면 결과를 더 읽기 쉽게 만들 수 있지만 namedtuple()형으로 변환되면서 약간의 성능 저하가 발생된다.
```python
Post.objects.values_list('id', 'writer', named=True)
``` 

* 일반적으로 values_list()를 사용하는것은 특정 모델 인스턴스의 특정 필드의 값을 가져올 때 사용한다. 이를 위해 values_list()다음 get()을 호출한다.
```python
Post.objects.values_list('writer', flat=True).get(pk=1)
``` 

* values()및 values_list()는 모두 특정 사용 사례에 대한 최적화를 위한 것이다.
*  M:M 및 기타 다중 관계 (예 : 1:M관계에서 역참조)를 다룰 때 “하나의 행, 하나의 객체”가 적용되지 않고 모두 분리 된다.
```python
Author.objects.values_list('name', 'entry__headline')

<QuerySet [('Noam Chomsky', 'Impressions of Gaza'),
 ('George Orwell', 'Why Socialists Do Not Believe in Fun'),
 ('George Orwell', 'In Defence of English Cooking'),
 ('Don Quixote', None)]>
``` 
* 다수의 책을 작성한 작성자는 여러번 표시되고 항목이 없는 작성자는 entry__headline이 None으로 표시되는 것을 확인 할 수 있다.
  * 역참조에서 동일하게 None으로 표시됨

## dates()
* datetime.date 형태의 데이터를 반환한다. 반환하려고 하는 필드는 datetime.date 속성이어야 한다.
* 첫번째 인자로 필드이름, 두번째 인자로 year, month, day중에 원하는 것을 입력한다. order는 'ASC', 'DESC'로 설정할 수 있으며 기본값은 'ASC'이다.
* 필드는 모델의 DateField어야 한다. kind는 year, month, week, day어야 한다. 결과 목록의 각 datetime.date 객체는 주어진 유형으로 데이터를 잘라낸다.
  * year는 필드에 대한 모든 고유 연도 값이 담긴 list를 반환한다.
  * month는 필드에 대한 고유한 연도/월 값이 담긴 list를 반환한다.
  * week는 필드에 대한 모든 고유한 연도/주 값이 담긴 list를 반환하며 모든 날짜는 월요일이다.
  * day는 필드에 대한 모든 고유한 연/월/일 값이 담긴 list를 반환한다.
```python
# 기본형 
date(field, kind, order='ASC')

Post.objects.dates('created_at', 'day', order='DESC')
```

## datetimes()
* datetime.datetime 형태의 데이터를 반환한다. 
* dates()와 동일한 동작을 가지며 datetime.datetime 속성의 필드를 명시해야한다.
* year, month, day 이외에도 hour, minute, second도 옵션으로 선택할 수 있다.
```python
# 기본형 
datetimes(field_name, kind, order='ASC', tzinfo=None, is_dst=None)
```
* tzinfo는 자르기 전에 datetime이 변환되는 시간대를 정의한다. 
  * 실제로 주어진 datetime은 사용중인 시간대에 따라 다른 표현을 갖는다. 
  * 이 매개 변수는 datetime.tzinfo객체여야 한다. 
    * None이면 Django의 현재 시간대를 사용한다. USE_TZ가 False면 아무런 변화가 없다.
* is_dst는 pytz가 서머타임을 사용하는지에 대한 여부를 나타낸다. 
  * 기본적으로 (is_dst = None) pyzt는 이러한 날짜 시간에 대해 예외를 발생시킨다.

* 데이터베이스의 시간대를 사용하는 datetime()
    * datetime()은 데이터베이스에서 직접 시간대 변환을 수행한다. 
    * 따라서 데이터베이스는 tzinfo.tzname (None)의 값을 해석 할 수 있어야 한다. 
    * 따라서 데이터베이스는 다음과 같은 요구사항이 충족되어야 한다.
      * SQLite : 요구 사항이 없다. 변환은 Python에서 pytz를 사용하여 수행되며 이 패키지는 Django를 설치할때 이미 설치되어 있는 패키지이다.
      * PostgreSQL : 요구사항 없음 
        * (참조:https://www.postgresql.org/docs/current/datatype-datetime.html#DATATYPE-TIMEZONES)
      * Oracle : 요구사항 없음 
        * (참조:https://docs.oracle.com/en/database/oracle/oracle-database/18/nlspg/datetime-data-types-and-time-zone-support.html#GUID-805AB986-DE12-4FEA-AF56-5AABCD2132DF)
      * MySQL : mysql_tzinfo_to_sql을 사용하여 시간대 테이블을 가져온다. 
        * (참고:https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html)


## union()
* SQL의 UNION을 사용하여 둘 이상의 QuerySet 결과를 결합한다.
* UNION 연산자는 기본적으로 고유한 값만 선택한다. (distinct()가 기본적으로 수행됨.) 
  * 이 때 중복 값을 허용하려면 all = True인수를 사용한다.
* 결과 QuerySet에는 LIMIT, OFFSET, COUNT(*), ORDER BY및 열 지정 (슬라이싱, count(), order_by(), value(), values_list())만 허용된다.
```python
# 기본형
union(*other_qs, all=False)

qs1.union(qs2, qs3)
```

## intersection()
* SQL의 INTERSECT를 사용하여 둘 이상의 QuerySet의 교집합을 반환한다.
* intersection()의 제한사항은 union()과 동일하다.
```python
qs1.intersection(qs2, qs3)
```

## difference()
* SQL의 EXCEPT연산자를 사용하여 둘 이상의 QuerySet의 차집합을 반환한다.
* difference()의 제한사항은 union()과 동일하다.
```python
# 기본형
difference(*other_qs)

qs1.difference(qs2, qs3)
```

## select_related()
* 이 경우 두 줄의 코드를 실행하는 동안 각각이 데이터베이스에 접근해야 한다.
```python
# Hits the database.
e = Post.objects.get(id=5)

# Hits the database again to get the related Blog object.
b = e.blog
```
* select_related로 'blog'필드에 한 번 접근했기 때문에 이미 캐싱이 되었고 e.blog에 접근할 때 데이터베이스를 거치지 않아도 된다.
```python
# Hits the database.
e = Post.objects.select_related('category').get(id=5)

# Doesn't hit the database, because e.blog has been prepopulated
# in the previous query.
b = e.category
```
## extra()
* 복잡한 WHERE절을 표현하기 어려울 때 사용할 수 있다. 하지만, 기본 쿼리셋으로 표현가능하면 표현하고 정 안되면 extra()를 사용하기를 권장한다.
* ! 이 방법은 최후의 수단으로 사용할 것
  * extra()는 향후 Django에서 지원을 중단하려는 오래된 API이다. 
    * 다른 쿼리셋 메서드를 사용하여 쿼리를 표현할 수 없는 경우에만 사용할 것을 권장한다. Django는 더 이상 extra()에 대한 버그를 개선하거나 수정하지 않는다.
* SQL injection에 취약한 extra()
  * extra()를 사용할 때는 SQL injection공격에 매우 취약하므로 사용자가 매개 변수를 사용하여 제어할 수 있는 모든 매개 변수를 이스케이프해야 한다.
  * 또한 SQL문자열에서 자리 표시자를 인용하지 않아야 한다. 이 예제는 %s주위의 ''사용으로 이해 SQL injection에 취약하다.
```python
# 기본형
extra(select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
```

### select
* 각 Entry 객체의 발행일자가 2006년 1월 1일 이후인지 비교한 boolean값을 is_recent라는 키워드로 사용하겠다는 의미이다.
```python
Post.objects.extra(select={'is_recent': "created_at > '2006-01-01'"})
```

### where
* SQL구문의 WHERE절을 만드는데 활용한다. where의 각 요소는 AND로 이어진다.
```python
Post.objects.extra(where=["writer='류상현' OR writer = '노옥자'", "writer = '서상호'"])
Post.objects.extra(where=["writer='류상현' OR writer = '노옥자'"])
```
* 위의 문장에서 where안의 요소는 콤마로 구분하여 2가지 요소가 있다. foo와 bar는 OR로 연결되어 있지만 baz는 AND로 연결된다. 이를 SQL문으로 변형하면 다음과 같다.
```python
SELECT * FROM post WHERE (writer='류상현' OR writer='노옥자') AND (writer='서상호')
```

### order_by
* extra를 이용하여 새로 추가한 내용에 대해 ordering옵션을 줄 수 있다.
* is_recent는 extra에 의해 생성되었기 때문에 extra의 order_by 옵션으로 정렬한다.
```python
q = Post.objects.extra(select={'is_recent': "created_at > '2006-01-01'"})
q = q.extra(order_by = ['-is_recent'])
```

### params
* where를 사용할 때 매개변수 표현을 %s로 한다. 이 때, %s에 적용될 매개변수를 params에 적어주면 된다.
* params는 ' '안에 문자열을 입력한다.
```python
Post.objects.extra(where=['writer=%s'], params=['이승민'])
```

## defer()
* 쿼리셋으로 데이터베이스에 접근할 때 꺼내오지 않을 필드명을 선택한다.
* 일부 복잡한 데이터 모델링에서는 모델에 많은 필드가 포함되며, 그중 일부에는 많은 데이터(ex. TextField)가 포함될 수 있거나 Python 객체로 변환하기 위해 무거운 처리가 필요할 수 있다. 
* 데이터를 처음 가져올 때 특정 필드가 필요한지 여부를 알 수 없는 상황에서 쿼리셋의 결과를 사용하는 경우 Django에 데이터베이스에서 검색하지 않도록 지시 할 수 있다.
* select_related()를 사용하여 관련 모델을 검색하는 경우 기본 모델에서 관련모델로 연결되는 필드를 검색에서 제외시키면 안된다. 만약 검색에서 제외된다면 에러가 발생한다.
```python
Post.objects.defer("address", "content")
```
* double underscore (__)를 사용하여 관련 필드를 구분하여 관련된 모델의 필드를 검색에서 제외시킬 수 있다.(select_related를 통해 쿼리셋을 가져올 경우)
```python
Blog.objects.select_related().defer("entry__headline", "entry__body")
```
* 검색에서 제외된 필드 집합을 해제하려면 defer()의 매개변수로 None을 전달한다.
```python
# 모든 필드를 가져온다.
my_queryset.defer(None)
```
* Entry에서 headline과 body필드를 제외하고 나머지 정보만 불러온다. 말그대로 데이터베이스 접근을 미루는 것이다.
```python
class CommonlyUsedModel(models.Model):
    f1 = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'app_largetable'

class ManagedModel(models.Model):
    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)

    class Meta:
        db_table = 'app_largetable'

# Two equivalent QuerySets:
CommonlyUsedModel.objects.all()
ManagedModel.objects.all().defer('f2')
```
* CommonlyUsedModel.objects.all()은 f1 필드밖에 없기 때문에 f1만 읽어온다. 
* ManagedModel.objects.all().defer('f2')은 f1, f2필드가 있는데 f2를 defer시키기 때문에 f1만 불러온다. 
* 따라서, 두 쿼리셋은 똑같이 f1만 불러오는 동작을 한다.

## only()
* defer()과 반대로 동작한다. 명시한 필드만 데이터베이스에서 접근한다.
* 필드가 age, biography, name만 있다고 가정하면 아래의 두 쿼리셋은 같은 필드에 접근한다.
* only()를 사용하고 select_related()를 사용하여 요청 된 필드를 생략하는 것도 에러가 발생한다.
```python
Person.objects.defer("age", "biography")
Person.objects.only("name")
```
* defer는 age, biography만 제외하고 가져오기 때문에 name만 가져오고 only는 명시한 필드인 name만 가져오기 때문에 같은 동작이다.
 ```python
Entry.objects.only("body", "rating").only("headline")
``` 
* only가 여러개 있으면 가장 나중에 호출된 only만 유효하다. 따라서 headline만 선택된다.
```python
Entry.objects.only("headline", "body").defer("body")

== Entry.objects.only("headline")
```  
* headline과 body에 only를 적용했지만 body에 대해서는 defer가 다시 적용되었기 때문에 결국 only('headline')과 같다.
```python
Entry.objects.defer("body").only("headline", "body")

== Entry.objects.only("headline", "body")
```  
* only는 앞의 내용을 재정의한다.
  
## raw()
* SQL쿼리문을 매개변수로 받아서 동작을 처리한다.
* raw()사용시 주의 사항
  * raw()는 항상 새 쿼리를 트리거하고 이전 필터링을 고려하지 않는다. 따라서 일반적으로 Manager 또는 새로운 쿼리셋 인스턴스에서 호출해야 한다.
```python
# 기본형
raw(raw_query, params=None, translations=None)

for p in Person.objects.raw('SELECT * FROM myapp_person'):
...     print(p)
John Smith
Jane Jones
```  
* Person.objects.raw('SELECT * FROM myapp_person')에서 쿼리문은 mypp_person 테이블의 모든 데이터를 선택한다. 
* 이 코드는 Person.objects.all()과 동일하게 동작한다. 
* 이것만 보면 raw()의 장점을 많이 발견할 수 없지만 쿼리문을 다양하게 구성하면 강력한 옵션을 제공할 수 있다

## select_for_update()
* 트랜잭션이 끝날 때까지 행에 락을 걸고 지원되는 데이터베이스에서 SELECT ... FOR UPDATE SQL문을 생성하는 쿼리셋을 반환한다.
* 쿼리셋을 평가 될 때 (이 경우 항목의 항목에 대해) 일치하는 모든 항목은 트랜잭션 블록이 끝날 때까지 락이 걸린다. 즉, 다른 트랜잭션이 해당 항목에 대한 락을 변경하거나 획득하지 못하도록 한다.
* 일반적으로 다른 트랜잭션이 선택한 행 중에 하나에 대해 이미 락이 걸린 경우 락이 해제될 때 까지 쿼리가 차단된다. 
  * 이것이 원하는 동작이 아닌 경우 select_for_update(nowait = True)를 호출한다. 
  * 이렇게하면 호출이 차단되지 않는다 충돌하는 락이 이미 다른 트랜잭션에 의해 획득 된 경우 쿼리셋이 평가 될 때 데이터베이스 에러가 발생한다. 
  * 대신 select_for_update(skip_locked = True)를 사용하여 락이 걸린 행을 무시할 수도 있다. 
    * nowait과 skip_locked는 상호 배타적이며 두 옵션을 모두 활성화 한 상태에서 select_for_update()를 호출하면 ValueError가 발생한다.
* 기본적으로 select_for_update()는 쿼리에서 선택한 모든 행에 락을 건다. 
  * 예를 들어 select_related()에 지정된 관련 객체의 행은 쿼리 셋 모델의 행과 함께 잠긴다. 
  * 원하지 않는 경우 select_related()와 동일한 필드 구문을 사용하여 select_for_update(of = (...))를 통해 락을 걸려는 관련 객체를 지정한다. 
    * 검색어 세트의 모델을 참조하려면 self를 사용한다.
```python
# 기본형
select_for_update(nowait=False, skip_locked=False, of=())
from django.db import transaction

entries = Entry.objects.select_for_update().filter(author=request.user)
with transaction.atomic():
    for entry in entries:
        ...
``` 

* select_for_update(of=(...))에서 상위 모델 락 걸기
  * 다중 테이블 상속을 사용할 때 상위 모델에 락을 걸려면 of인수에 상위 링크 필드 (기본적으로 <parent_model_name>_ptr)를 지정해야 한다.
```python
Restaurant.objects.select_for_update(of=('self', 'place_ptr'))
``` 
* nullable관계에는 select_for_update()를 사용할 수 없다.
```python
Person.objects.select_related('hometown').select_for_update()

Traceback (most recent call last):
...
django.db.utils.NotSupportedError: FOR UPDATE cannot be applied to the nullable side of an outer join
``` 
* nullable관계에는 select_for_update()를 사용할 수 없다.
```python
Person.objects.select_related('hometown').select_for_update().exclude(hometown=None)
<QuerySet [<Person: ...)>, ...]>
```

* 현재 PostgreSQL, Oracle, MySQL데이터베이스는 select_for_update()를 지원한다. 그러나 MariaDB 10.3+는 nowait만 지원되며 MySQL 8.0.1+는 nowait및 skip_locked를 지원한다. MySQL과 MariaDB는 of인수를 지원하지 않는다.

* MySQL과 같이 이러한 옵션을 지원하지 않는 데이터베이스를 사용하여 nowait=True, skip_locked = True또는 select_for_update(of=(...))를 전달하면 NotSupportedError가 발생한다.

* SELECT ... FOR UPDATE를 지원하는 데이터베이스의 자동 커밋 모드에서 select_for_update()를 사용하여 쿼리세트를 평가하는 것은 이 경우 행에 락이 걸리지 않기 때문에 TransactionManagementError가 발생한다. 
* 만약 에러가 발생하지 않게 허용한다면 트랜잭션외부의 트랜잭션에서 실행 될 것으로 예상되는 코드를 호출하여 데이터 손상이 쉽게 발생할 수 있다.

* SELECT ... FOR UPDATE를 지원하지 않는 데이터베이스 (ex. SQLite)에서 select_for_update()를 사용하면 효과가 없다. 
* SELECT ... FOR UPDATE는 쿼리에 추가되지 않으며 자동 커밋 모드에서 select_for_update()를 사용하면 오류가 발생하지 않는다.

* TestCase에서 select_for_update()사용시 주의 사항
  * select_for_update()는 일반적으로 자동 커밋 모드에서 실패하지만 TestCase는 트랜잭션의 각 테스트를 자동으로 래핑하므로 atomic()블록 외부에서도 TestCase에서 select_for_update()를 호출하면 TransactionManagementError를 발생시키지 않고 (아마도 예기치 않게) 통과된다.select_for_update()를 제대로 테스트 하려면 TransactionTestCase를 사용해야 한다.
* 지원되지 않는 표현 : Window function
  * select_for_update()PostgreSQL의 Window function expression을 지원하지 않는다.

## exists()
* QuerySet 의 결과가 존재하는지 쿼리한 결과를 반환합니다.
```python
# return - bool
is_exist = queryset.exists()
``` 

## count()
* QuerySet 의 결과 갯수를 쿼리한 결과를 반환합니다.
```python
# return - int
row_count = queryset.count()
``` 

* * *

# 인스턴스 생성

## 빈 인스턴스 작성
* 빈 인스턴스를 생성합니다. 메모리에만 존재하며, save() 를 호출하기 전까지 데이터베이스에 저장되지 않습니다.
```python
article = Article()
article.title = "게시물 내용"
article.body = "게시물 제목"

# 데이터베이스에 저장
# primary_key=True 필드가 자동 생성이 아니며, 값이 설정되지 않으면 오류 발생.
article.save()
```

## none()
* 객체를 반환하지 않는 쿼리셋을 만든다.
```python
Post.objects.none()
# 확인
from django.db.models.query import EmptyQuerySet
isinstance(Post.objects.none(), EmptyQuerySet)
True
```

## create()
* 인자값으로 객체를 데이터베이스에 생성하고, 해당 인스턴스를 반환합니다.
```python
# return - instance: Model

obj = Article.objects.create(
    name="article 1", body="body 1"
)
``` 

## get_or_create()
* defaults 값을 제외한 인자값으로 get()을 시도합니다. 객체를 찾으면 반환하며, 그렇지 않으면 인자값과 **defaults 로 인스턴스를 만들고 반환합니다.
```python
# return - tuple(instance: Model, created: bool)

obj, created = Article.objects.get_or_create(
    name="article 1",  defaults={"body":"1234}   
)
``` 

# 인스턴스 수정

## save()
* 인스턴스의 필드 값을 저장합니다. 빈 인스턴스이고, primary_key 필드값을 지정하지 않고 Auto 필드이면 값이 자동 설정됩니다.
```python
# return - None

obj = Article.objects.get(id=1)
obj.body = F("body") + "내용 추가"
obj.save()
``` 
|이름|타입|속성|
|:---:|:---:|:---:|
|force_insert|bool(False)|강제로 INSERT 문을 사용합니다. 일반적으로 사용하지 않습니다.|
|force_update|bool(False)|강제로 UPDATE 문을 사용합니다. 일반적으로 사용하지 않습니다.|
|using|db_dialect(None)|저장할 데이터베이스 dialect|
|update_fields|iterable(None)|저장할 필드를 지정합니다. 비어있다면 저장되지 않습니다.|

## update_or_create()
* 쿼리된 단일 인스턴스 변경 또는 생성
* defaults 값을 제외한 인자값으로 get()을 시도합니다. 객체를 찾으면 **defaults 값으로 update()를 호출합니다. 그렇지 않으면 인자값과 **defaults 로 새로운 인스턴스를 만들고 반환합니다.
* QuerySet에 사용하면 인자값과 필터를 합쳐 확인하고, 위와 동일하게 실행됩니다. 이 때 QuerySet 필터 값은 새로운 객체에는 반영되지 않습니다.
* **참고: get이 사용되므로 2개 이상의 객체가 발견되면 Model.MultipleObjectReturned 오류가 발생합니다.**
```python
# return - tuple(instance: Model, created: bool)

obj, created = Article.objects.update_or_create(
    id=123,  defaults={"view_count": 30}    
)
``` 

# 인스턴스 삭제
## save()
* 인스턴스 또는 QueryuSet 결과를 데이터베이스에서 삭제합니다. DELETE 쿼리가 실행됩니다.
* 반환값으로 삭제된 데이터의 행 갯수가 반환됩니다.
```python
# return - int

# 단일 객체 인스턴스 삭제
obj = Article.objects.get(id=1)
deleted_cnt = obj.delete()

# 쿼리와 일치하는 객체 일괄 삭제
queryset = Article.objects.filter(name__contains="django")
deleted_cnt = queryset.delete(0)
``` 
|이름|타입|속성|
|:---:|:---:|:---:|
|using|db_dialect(None)|저장할 데이터베이스 dialect|
|keep_parents|bool(False)|True이며 모델이 타 모델의 외래키 연결을 가지고 있으면<br> 자신은 삭제하지 않고 연결된 자식 모델만 삭제합니다.|
* 참고: keep_parents - 삭제되는 대상은 자신을 가리키는 모델을 지정합니다.

## pickle()
* 피클 모듈은 파이썬 객체 구조를 serialize/de-serialize하기 위한 바이너리 프로토콜을 구현한 것임
* JSON은 텍스트 직렬화 형식(유니코드 텍스트를 출력하지만, 대개는 utf-8 으로 인코딩됩니다)인 반면, pickle은 바이너리 직렬화 형식
  * https://docs.python.org/ko/3/library/pickle.html
* 파이썬은 객체를 파일에 저장하는 pickle 모듈을 제공함
  * https://skyfox83.tistory.com/100?category=902679
  
## Bulk_create()
* 백엔드 개발을 하다 보면 한 번의 요청으로 테이블에 대량의 레코드를 삽입하게 될 경우가 있다. 예를들어 서비스를 이용하는 모든 유저들에게 노티스를 보내고 싶을 때, 다음과 같은 코드로 노티스 레코드를 생성 할 수 있을 것이다.
```python
users = User.objects.all()

for user in users:
    Notification(user=user, contents="반갑습니다.").save()
```
* 하지만 위와 같은 방법으로 for문을 돌며 다수의 오브젝트를 만들어 낼 경우 save() 메소드 한 번당 DB와의 connection이 한번 발생 하며 insert구문을 수행 하게 된다. 
* 즉, 반복 횟수 == connection수가 되어서 서비스에 큰 부하가 생겨 장애를 야기할 수도 있다. 
* 실제로 로컬에서 테스트를 하다가 설정해둔 최대 connection수를 넘겨버린 경우도 있었다
* 이럴때 사용하는것이 bulk operation이며 이 bulk를 사용하면 다수의 레코드를 생성, 업데이트 할 때 한 번의 커넥션 만으로 insert 혹은 update를 수행 할 수 있다.
* 사용법은 매우 간단하다. 만들고자 하는 테이블 모델의 오브젝트 리스트를 만들어 bulk_create의 인자로 넘겨준다.
```python
users = User.objects.all()

# notification 오브젝트 리스트를 만든다.
new_noti_list = [Notification(user=user, contents="반갑습니다.") for user in users]

Notification.objects.bulk_create(new_noti_list)
```
* **Bulk_create 사용시 주의할 점**
  * Bulk_create는 매우 편리한 기능이지만 사용할 때 꼭 주의해야 할 점이 있다. 
  * 바로 bulk 를 사용하면 Django Model 클래스에서 제공 하는 기본 메소드(save, clean... 등) 들을 사용하지 못한다는 점이다. 
  * 어떤 모델은 save(), clean() 메소드 등을 오버라이드 하여 오브젝트 저장 시점에 특별한 액션(트랜잭션, 유효성 검사 등)을 취할 수 있다. 
  * 하지만 bulk 를 사용하면 오브젝트를 DB에 직접 때려박는 식이기 때문에 모델 클래스의 기본 메소드 지원을 받을 수 없다. 
  * 그말은 즉 bulk operation을 통해 데이터 베이스에 유효하지 못한 값이 들어가거나 데이터의 무결성이 깨질 가능성이 생긴다는 것이다.
  * 따라서 bulk를 사용하기 전 해당 모델의 생성에 의해 영향을 받는 모델이 있는지, 모든 필드에 유효한 값이 들어오는지 등의 전수조사를 철저히 해야 한다.

## Queryset 합치기
*  이런 Toy라는 모델이 있을 때, 우리는 Toy.objects.all() 같은 명령어를 통해 Toy 객체의 집합(Queryset)을 얻을 수 있을 것이다. 
*  비지니스 로직을 작성하다 보면 여러 쿼리셋을모아 조합하여 응답으로 보내줘야 할 경우가 있는데 이럴 때 쿼리셋을 합치는 연산을 이용할 수 있다.

```python
# model 예시
class Toy(models.Model):
    name = models.CharField(max_length=50, help_text='이름')
    price = models.IntegerField(help_text='가격')
    company = models.CharField(max_length=50, help_text='판매사')

# Queryset 합치는 예시
qs1 = Toy.objects.filter(price__lte=10000) # 만원 이하인 장난감들
qs2 = Toy.objects.filter(price__gt=20000)  # 2만원이 넘는 장난감들

# 방법1
result_set = qs1 | qs2  # qs1과 qs2를 합친 결과

# 방법2
result_set2 = qs1.union(qs2)
```

### '|' 와 union의 차이점
* 쿼리셋을 합치기 위해 필요한 조건은 합치려고 하는 두 쿼리셋이 같은 필드를 갖고 있어야 한다
  * 엄밀히 말하면 같은 모델이라도 필드명과 타입이 똑같으면 쿼리셋을 합칠 수 있다는 것이다.
  *  물론 필드가 다르더라도 ORM 작성시 annotate를 통해 필요한 컬럼을 붙여 최종적으로 queryset에 담겨있는 모델의 스키마가 같게 해주면 합쳐질 수 있다.
```python
class Toy(models.Model):
    name = models.CharField(max_length=50, help_text='이름')
    price = models.IntegerField(help_text='가격')
    company = models.CharField(max_length=50, help_text='판매사')
    
class Toy2(models.Model):
    name = models.CharField(max_length=50, help_text='이름')
    price = models.IntegerField(help_text='가격')
```
* 위의 Toy와 Toy2 모델은 다른 모델이지만 다음과 같이 company 컬럼을 추가해 주어 쿼리셋을 만들어 주면 Toy 쿼리셋과 합칠 수 있다는 것이다. 
```python
Toy2.objects.annotate(company=Value('company2', output_field=CharField())
```
* 다음 예시
```python
qs1 = Toy.objects.annotate(is_sold_out=Value(True, output_field=BooleanField()).all()
qs2 = Toy2.objects.annotate(company=Value('company2', output_field=CharField(),
			    is_sold_out=Value(False, output_field=BooleanField())).all()
                            
result = qs1 | qs2
```
* qs1 에는 Toy 모델에 is_sold_out 이라는 컬럼을 추가하여 True라는 값으로 채워 넣었고, Toy2는 company와 is_sold_out 컬럼 두 컬럼을 추가하여 qs1과 qs2에 담긴 객체는 name, price, company, is_sold_out 이라는 동일한 4 컬럼을 가지고 있게 되었다.
  * 결과적으로 result쿼리셋 에서는 qs1의 객체들은 is_sold_out이 True, qs2의 객체들은 is_sold_out이 False가 담긴 채 합쳐져 들어가 있을것이라고 예상했다. 하지만 모든 객체의 is_sold_out이 True인게 아니겠는가??
* 문제는 Django ORM 코드의 평가 시점 때문에 생긴 문제였다. 
  * Django는 db접근의 효율을 높이기 위하여 코드를 읽는 순간 db에 접근하여 ORM의 결과를 수행한 결과를 가져오는 것이 아닌 필요시점에 접근하여 가져오게 된다. 
  * 위의 코드 대로 라면 qs1, qs2는 result에 합쳐지는 순간 쿼리를 해서 가져온다. 
  * 그 순간에 '|'연산자와 union의 동작 방식의 차이때문에 결과에도 차이가 생기게 된다.
    * qs1 | qs2 는 각 필드들을 OR 조건을 통해 가져오는 SQL문을 작성했으며,
    * qs1.union(qs2) 는 q1에 해당하는 질의와 qs2에 해당하는 질의를 union연산으로 합친 SQL문을 작성했다.
* 이러한 결과를 위의 Toy모델에 적용시켜 보면 is_sold_out이라는 필드는 Toy에는 True, Toy2에는 False이니 qs1 | qs2 라는 연산을 하면 is_sold_out의 결과는 True or False로 항상 True가 나오는 것이었다.
* **원하는 대로 qs1에는 True, qs2에는 False가 나오게 하려면 qs1질의 따로 qs2질의를 따로 하는 qs1.union(qs2) 로 합쳐야 한다는 결론이 나왔다.**
* 이처럼 '|' 연산자와 union의 수행 방식에 차이에 따라 결과가 달라질 수 있으니 쿼리셋을 합칠때는 주의하도록 하자. 특히 '|'연산자는 두 모델이 필드를 OR하기 때문에 복잡한 annotate로 명시적으로 컬럼을 만들어 주면 오류를 내뱉을 확률이 크니 **annotate를 사용한 쿼리셋, 그리고 Bool필드가 들어간 쿼리셋을 합칠 시에는 union을 이용하도록하자.**
```python
result = qs1.union(q2)
```
* 위 방법을 사용하니 qs1에는 True qs2에는 False로 원하는 값이 들어가 있었다. 
* 이게 어떻게 된 일인가 하고 silk라는 django 프로파일링 툴을 이용하여 ORM - > SQL로 바뀐 결과를 살펴보았다.
> reference : https://github.com/lewis810k/fastcampus/blob/master/33_%EC%BF%BC%EB%A6%AC%EC%85%8B_%EB%A9%94%EC%86%8C%EB%93%9C%281%29.md#%EC%BF%BC%EB%A6%AC%EC%85%8B%EC%9D%98-%ED%99%9C%EC%9A%A9   
> reference : https://yongineer.netlify.app/django/queryset-api/
> reference : https://blog.live2skull.kr/django/django-orm-01-basic/   
> reference : https://gardeny.tistory.com/15   
> reference : https://gardeny.tistory.com/13?category=884965