# 테스트 방법

> commander : python manage.py shell_plus --print-sql --ipython

# _set vs related_name

* ForeignKey에 related_name를 설정하지 않으면 역참조를 하는 경우, class명_set이 자동으로 설정된다.
* 하나의 외래키의 경우는 상관이 없으나, 두개 이상의 Foreign Key가 존재하는 경우 자동 생성되는 이름이 겹칠 수 있다.
* 이럴 경우 related_name를 명시해 주면, 해당 명칭으로 역참조 되는 클래스를 호출할 수 있다.

```python
class Category(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='category')

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='post')
```

* * *

# Queryset 연습 1

```python
queryset = Category.objects.prefetch_related('post') # post_set 대신 related_name에 선언한 post 사용
queryset
```
* prefetch_related() 부분에 선언한 필드(post 클래스 참조) 때문에 역참조를 위한 메인 쿼리 이후 한 개의 추가 쿼리가 발생한다.
  
# Queryset 연습 2

```python
queryset = Post.objects.select_related('category').filter(category=1)
queryset
```

* select_related() 부분에 선언한 필드 때문에 메인쿼리에서 JOIN이 발생하게 되었다. 추가 쿼리는 발생하지 않았다.

* 필드를 여러 개로 줄 경우 JOIN은 필드의 갯수에 비례해 늘어나게 된다.

* * *

# Queryset 심화 연습 1

```python
queryset = Category.objects.prefetch_related(Prefetch('post', queryset=Post.objects.select_related('category').all()))
queryset
```

* prefetch_related() 안에서 Prefetch()를 통해 쿼리셋을 재 선언하였고, 그 안에서 select_related()를 이용하였다.

  * 메인 쿼리로서 Category 모델의 정보를 가져오는 것
  * prefetch로 인해 추가 쿼리가 발생하였고 쿼리셋의 재 선언을 통해 select_related() 옵션을 주었으므로 추가쿼리에서의 JOIN 발생   

* prefetch_related() -> 추가쿼리 / select_related() -> JOIN 발생의 규칙을 알고 있다면 생성되는 SQL을 예측할 수 있다.

# Queryset 심화 연습 2

```python
queryset = Blog.objects.filter(id=1).prefetch_related(Prefetch('category__post', queryset=Post.objects.filter(title__contains='quis')))
queryset
```

* Prefetch의 필드를 category__post로 정함으로써 post 모델에 관련된 정보까지 미리 가져오도록 하였다. 그렇기 때문에 총 3개의 쿼리가 발생하였다.

  * 메인 쿼리로서 Blog 모델의 정보를 가져오는 것
  * 추가 쿼리 1 - Category 모델의 정보를 가져오는 쿼리
  * 추가 쿼리 2 - Post 모델의 정보를 가져오는 쿼리 (title로 필터를 주었으므로 where절 발생)

* * *

# Queryset 심화 연습 3

```python
queryset = Blog.objects.filter(id=1).prefetch_related(Prefetch('category', queryset=Category.objects.filter(name__contains='modi')), Prefetch('category__post', queryset=Post.objects.filter(title__contains='quis')))
queryset
```

* 이번 예시에서 한 가지 달라진 점은 바로 Category와 Post에 대한 조건절을 Prefetch()를 두번 사용해 따로 분리해주었다는 점이다.
* 이렇게 하면 모델에 대한 조건절을 각각 부여할 수 있다.

* * *

# ORM이 생성하는 SQL 구조 / 추천하는 ORM 작성 순서


```python
queryset = (Model.objects
                .select_related('정방향_참조필드1,','정방향_참조필드2',....) 
                # N개 만큼 JOIN 함 
                    .annotate(커스텀속성1=F('모델필드'),  
                        커스텀속성2=Case(
                            When(모델필드__isnull=False,  
                                # when : case의 조건절, filter에 관련한 옵션 전부 사용 가능
                                then=Count('모델필드')), 
                                # 모델 필드에서 Count() 함수를 질의함
                            default=Value(0, output_field=IntegerField(),
                            # output_field=장고에서 무슨 타입으로 결과를 받을 지 선언하는 부분
                            ),
                        )
                    )
                        .filter(필터옵션)
                .prefetch_related(
                    Prefetch('역방향_참조필드', 
                    # 추가 쿼리 발생, 쿼리셋의 재 선언을 통해 다양한 튜닝 가능 
                        queryset=(역방향_참조모델.objects
                                    .select_related('역방향_참조모델의_정방향참조모델')
                                        .filter(역방향_각종_질의문))
                                    # .prefetch_related('역방향_참조모델의_역(정)방향참조모델') 
                                    # 위처럼 사용도 가능함
                    )
                )
            )
```

```python
SELECT *
       모델필드 AS 커스텀 속성1,
       CASE
           WHEN 모델필드 IS NOT NULL
               THEN COUNT('모델필드')
        ELSE 0 END AS 커스텀 속성2,  # IntegerField()는 쿼리 영향 X
      
FROM `메인쿼리 Model`
         LEFT INNER JOIN '정방향 참조필드1'  
         # INNER, OUTER 는 ForignKey의 null 옵션 값에 의해 결정
                         ON (~~~~)
         LEFT OUTER JOIN '정방향 참조필드2'  
         # INNER, OUTER 는 ForignKey의 null 옵션 값에 의해 결정
                         ON (~~~~)
WHERE (필터 옵션)


SELECT *
FROM 역방향_참조모델
         INNER JOIN '역방향_참조모델의_정방향참조모델'
                    ON ( )
WHERE (역방향_각종_질의문 AND 메인쿼리의_Model.`related_id` IN (1,2,3,4,....));
```

* 위와 같은 순서로 ORM을 작성하는 것이 실제로 생성되는 SQL의 순서와 가장 유사하다.

  * 유심히 살펴보면 같은 옵션을 여러 번 사용하면 대부분 비슷한 구조로 SQL이 생성된다.
  * 지만 모든 경우에 같은 구조를 생성한다는 것은 보장할 수 없으므로 유독 느려지거나(서브쿼리, 슬로우쿼리) 하는 부분에 대해서는 실제로 어떻게 수행되는지 꼭 디버깅 해 볼 필요가 있을 것이다.
  
> reference : https://leffept.tistory.com/314?category=950490