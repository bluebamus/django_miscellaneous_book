# 실수하기 쉬운 Queryset의 특징

* Django ORM을 작성하다보면 종종 당연히 '이렇게 수행 될거야' 라고 생각하지만 실제로는 그렇지 않은 부분들이 꽤 많이 존재한다.
* 다룰 주제는 다음과 같다
  * queryset 캐시를 재활용하지 못하는 queryset 호출
  * prefetch_related() 와 filter()의 올바른 사용법
  * 서브쿼리가 발생하는 조건
  * values(), values_list() 사용시 주의점

* * *

# Queryset 캐시를 재활용하지 못하는 queryset 호출

### 캐시를 사용하는 경우
```python
blog_list = list(Blog.objects.prefetch_related('category').all())
blog = blog_list[0]
blog.category.all()
category_name_list = [category for category in blog.category.all() if 'qui' in category.name]
category_name_list
```

### 캐시를 사용하지 못하는 경우
```python
blog_list = list(Blog.objects.prefetch_related('category').all())
blog.category.filter(name__contains='qui')
```

### 결과 값 출력 하는 방법
```python
for temp in blog_list:
    print(temp.category.values())
```

* 문제 발생
  * Blog 모델의 정보를 가져오는데 그 blog의 Category 정보를 함께 미리 불러왔다. 
  * 그 후 카테고리에 대한 정보를 all()로 질의하게 되면 이전 포스팅에서 설명했던 Queryset 객체에서 _result_cache 부분에 저장된 데이터를 불러와서 SQL을 호출하지 않는다. 
  * 하지만 filter 옵션을 통해 조건을 걸게 된다면 그 조건에 대한 SQL문이 새롭게 호출된다.

* **그렇다면 지금 상황에서 이미 가지고 있는 cache 데이터를 재 활용하려면 어떻게 해야할까?**
  * 정답은 바로, 파이썬의 list comprehension 방식을 이용하는 것이다.
  
* ORM을 작성할 때 조건절을 부여하기 위해서 filter() 함수를 당연하고 우선적으로 사용하게 되지만, 이를 사용할 때 주의 해야할 점은 이미 있는 정보에 대해 불필요한 SQL 호출을 야기할 수 있다는 것이다. 
* 이를 방지하기 위해 파이썬 레벨에서 조건절을 처리해주는 방식을 사용해 cache 데이터를 재활용할 수 있다.
* 지금 예시에서는 blog.category.all() 안에서 category의 name에 대한 조건을 부여하였다
  

# prefetch_related() 와 filter()의 올바른 사용법

* 이번에도 Blog 모델의 정보를 가져오고 그 blog에 대한 category의 name에 python이 포함되어 있는지를 확인하는 ORM을 작성해보려고 한다. 
  
```python
blog_queryset = Blog.objects.prefetch_related('category').filter(name__contains='김영희', category__name__contains='modi')
blog_queryset
```

* 막상 이 ORM을 실행해보면 생각했던 것과는 조금 다르게 동작하는 것을 확인할 수 있다. 
  * category의 이름에 대한 where 조건절이 추가 쿼리에 생성되지 않고 메인 쿼리에 생성됨으로써 의도와도 다르고, 불필요한 SQL문이 생성된다.

* 이렇게 동작하는 이유는 다음과 같다.
  * filter() 안에서 category__name으로 역참조 하였기에 메인쿼리에서 category 모델 JOIN 발생
  * prefetch_related() 안에서 category 모델을 역참조 하였기에 catregory 모델에 대한 추가 쿼리 발생

* **바로 이것이 prefetch_related() 와 filter() 의 잘못된 사용방법이다**
  * prefetch 안의 참조된 모델에 대한 조건절을 filter()를 통해 부여하려는 생각이 실수하기 쉬운 부분이다.
  * 올바르게 사용하는 방법은 무엇일까? 두 가지의 방법이 존재한다.
    * prefetch_related() 함수 제거
    * Prefetch() 쿼리셋 재선언을 이용한 조건절 부여

### 1. prefetch_related() 함수 제거

```python
blog_queryset = Blog.objects.filter(name__contains='김영희', category__name__contains='modi')
blog_queryset
```

### 2. Prefetch() 쿼리셋 재선언을 이용한 조건절 부여

```python
blog_queryset = Blog.objects.filter(name__contains='김영희').prefetch_related(Prefetch('category', queryset=Category.objects.filter(name__contains='modi')))
blog_queryset
```


* * *

# 서브쿼리가 발생하는 조건

```python
queryset = Category.objects.prefetch_related(Prefetch('post', queryset=Post.objects.select_related('category').all()))
queryset
```

* 장고에서는 Subquery() 라는 객체를 통해서 서브쿼리를 작성할 수 있다. 
* 하지만 종종 ORM을 작성하다보면 의도치 않게 서브쿼리가 발생하는 경우가 생기는데, 이는 슬로우쿼리가 되기 마련이다. 
  
* 서브쿼리가 발생하는 몇 가지를 예시와 함께 살펴보려고 한다.
  * 쿼리셋안에 쿼리셋이 있는 경우
  * exclude() 에서 역방향 참조모델 사용 시 서브쿼리 발생

### 1. 쿼리셋안에 쿼리셋이 있는 경우

```python
blog_queryset = Blog.objects.filter(id='1').values_list('id', flat=True)
category_queryset = Category.objects.filter(blog__id__in=blog_queryset)
category_queryset
```
* 위의 결과 처럼 쿼리셋안에 쿼리셋이 있는 경우 서브쿼리가 발생하게 된다
  * 먼저 위치한 blog_queryset이 실제로 수행되어 있지 않은 상태이기 때문에
  * 장고의 Lazy Loading 특성에 의해 category_queryset 이 실행되는 타이밍에 blog_queryset도 같이 수행되기 때문에 서브쿼리가 발생하게 된다.
  
### 1-1. 서브쿼리가 발생하지 않는 해결법

```python
# list()를 통해 blog_queryset을 즉시 실행
blog_queryset = list(Blog.objects.filter(id='1').values_list('id', flat=True))
category_queryset = Category.objects.filter(blog__id__in=blog_queryset)
category_queryset
```

* 위의 코드처럼 list()를 통해 blog_queryset을 즉시 사용함으로써 category_queryset을 사용할 때 서브쿼리가 생성되지 않도록 한다.

### 2. filter()에서 역방향 참조모델 사용시

```python
category_queryset = Category.objects.filter(name__contains='modi', post__title__contains='quid')
category_queryset
```
* filter()에서 역방향 참조모델을 사용시 정상적으로 JOIN된 메인 쿼리를 확인할 수 있다. 
  * 하지만 모든 부분은 똑같이하고 역방향 참조모델만 exclude()에 넣게되면 의도하지 않은 서브쿼리가 발생하게 된다.
  
### 2-1. exclude()에서 역방향 참조모델 사용시 서브쿼리 발생 (~Q() 객체)

```python
category_queryset = Category.objects.filter(name__contains='modi').exclude(post__title__contains='quid')
category_queryset
```

* 바로 전에 작성했던 ORM에서 filter() 부분만 그대로 옮겨 왔음에도 불구하고 역방향 참조모델이 존재할 경우에는 서브쿼리가 발생함을 확인할 수 있다. 
  * filter() 안에서 ~Q() 객체를 사용하더라도 서브쿼리는 동일하게 발생한다.

### 2-2. exclude()에서 정방향 참조모델 사용시

```python
category_queryset = Category.objects.filter(name__contains='quid').exclude(blog__name__contains='modi')
category_queryset
```

* 하지만 exclude()에서 정방향 참조모델을 사용할 때에는 정상적으로 JOIN 되는 것을 확인할 수 있다. 
  * 역방향 참조모델에서만 서브쿼리가 발생하게 되는데, 정확한 이유는 찾지 못하였다.

### 2-3. 서브쿼리가 발생하지 않는 해결법

```python
category_queryset = Category.objects.prefetch_related(Prefetch('blog', queryset=Blog.objects.exclude(name__contains='quid'))).filter(name__contains='modi')
category_queryset
```

* 이전 포스팅에서 다루었던 Prefetch() 객체와 prefetch_related()를 통하여 따로 추가 쿼리를 생성하는 방식으로 해결할 수 있다.
* 서브쿼리의 경우 데이터가 조금이라도 많아지면 성능에 심각한 영향을 미치기 때문에 의도적으로 사용하는 것이 아니라면 발생되지 않게 하는 것이 상당히 중요하다. 
* 대부분의 경우에 서브쿼리가 필요하지 않다고 생각하기 때문에 만약 서브쿼리가 발생한 경우라면 ORM을 다른 방법으로 작성해보면서 문제를 해결해야 할 것이다.

* * *

# values(), values_list() 사용시 주의점

```python
queryset = Blog.objects.filter(id=1).prefetch_related(Prefetch('category', queryset=Category.objects.filter(name__contains='modi')), Prefetch('category__post', queryset=Post.objects.filter(title__contains='quis')))
queryset
```

* values(), values_list()를 사용할때에는 Eager Loading 옵션인 select_related(), prefetch_related() 옵션을 전부 무시하게 된다.
* 그 이유는 values는 DB의 Raw단위로 데이터를 반환하기 때문에 객체와 관계들간의 매핑이 일어나지 않기 때문이다. 

## values() 사용시 Eager Loading 무시

```python
# select_related() 무시
category_queryset = Category.objects.select_related('post__title').filter(id=1).values()
category_queryset
```
* value()를 사용할 경우 select_related()와 관련된 JOIN 옵션이 완전히 무시된 것을 확인할 수 있다. 
* prefetch_related()의 경우에도 동일한 결과를 볼 수 있다.

## values_list() 사용시 Eager Loading 무시

```python
# prefetch_related() 무시
category_queryset = Category.objects.prefetch_related('post').filter(id=2).values_list('post')
category_queryset
```
* prefetch_related()를 사용하여 Post 모델에 대한 추가 쿼리를 가져오라고 Eager Loading 하였지만 전부 수행되지 않았다.
* 또한, values_list()에서도 Post 모델을 가져오지 않고 단순히 foreign key의 정보만 가져와서 1, 2, 3 ...와 같은 결과가 나온 것을 확인할 수 있다.

* 위에서 잠깐 언급하였지만 Eager Loading 옵션이 무시되는 이유는 단순하고 명료하다. 
* values(), values_list()는 DB의 Raw 단위로(데이터의 가로 한줄을 뜻함)데이터를 반환하는 특성 때문에 객체와 관계들 간의 매핑이 일어날 수 없기 때문이다.

> reference : https://leffept.tistory.com/316?category=950490