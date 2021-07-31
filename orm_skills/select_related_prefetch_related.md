# 사전 요구 지식 
* query : 1개의 메인 쿼리로 부를 수 있음  

* result_cache : SQL의 수행 결과가 저장되는 부분(캐싱), 저장된 데이터가 없을 경우 새로운 SQL문 호출함  

* prefetch_related_lookups : prefetch_relate() 부분에 선언된 값들을 저장함, 추가 쿼리셋이라고 부름  
  
* iterable_class : SQL의 결과값을 python의 어떤 자료구조로 받을 지에 대한 부분, values(), values_list()를 통해 바뀜  

* * *  

# select_related() VS prefetch_related()

* Select_related()는 JOIN을 통해 데이터를 즉시 가져오는(Eager Loading) 방법 (SQL단계에서의 JOIN)  

* Pretfetech_related()는 추가 쿼리를 통해 데이터를 즉시 가져오는 방법 (추가 쿼리 발생, JOIN은 파이썬 level에서 이루어짐)  

* * *

## select_related()의 사용

* select_related는 1:1의 관계에서 사용할 수 있고, 1:N의 관계에서 N이 사용할 수 있다  

* 즉, 정방향 참조(Post 모델에서 Category 모델의 정보를 찾으려고 할 때)에서의 JOIN에 유리하게 사용된다.  

### select_related() 사용 X

```python
post = Post.objects.all()
for p in post:
    print(p.category.name)
```

### select_related() 사용 O

```python
post = Post.objects.select_related('category').all()
for p in post:
    print(p.category.name)
```

* select_related('정방향 참조 필드') 함수를 통해 category에 대한 정보를 미리(Eager Loading) 불러오는 것을 볼 수 있다.  
  
* 또 한가지 유의할 점은, model의 category 필드에서 on_delete=models.SET_NULL(null=True) 옵션을 걸었기에 ORM에서 LEFT OUTER JOIN 구문이 생성되었다.  

* 만약, models.CASCADE 옵션을 걸었다면 INNER JOIN 으로 수행됬을 것이다.  

* 즉, select_related()는 정참조의 JOIN을 통해 Eager Loading 하는 함수라고 할 수 있다.

* * *

## prefetch_related()의 사용

* prefetch_related는 반대로 1:N의 관계에서 1이 사용할 수 있고, M:N의 관계에서 사용할 수 있다.   

* 즉, 역방향 참조(Category 모델에서 Post 모델의 정보를 찾으려고 할 때)에 유리하게 사용된다.

### prefetch_related 사용 O

```python
category = Category.objects.prefetch_related('post').get(name='django')
for c in category.post_set.all():
    print(c.title)
```

* 여기서 유심히 살펴봐야할 점은 Select 쿼리가 두 번 수행되었다는 점인데, 첫 번째의 쿼리는 category의 정보를 위한 쿼리이고 두 번째 쿼리는 prefetch_related('역방향 필드 참조', ...) 에 작성한 필드에 대한 추가 쿼리이다.   

* 즉, 필드 값으로 N개를 줄 경우 각 필드값에 대한 N개의 추가 쿼리가 발생하게 되는 것이다.   

* select_related 와의 가장 큰 차이점은 추가 쿼리가 발생한다는 것이고, 또 다른 차이점은 **발생된 추가 쿼리를 파이썬 단계에서 JOIN을 통해 결과를 만들어낸다는** 점이다.

* * *

##  추가 쿼리셋을 제어하는 방법 - Prefetch()

* prefetch_related의 필드들에 추가적인 조건을 걸고 싶은 경우가 있을 것이다. 그럴때 사용하는 것이 바로 Prefetch() 객체이다.

## Prefetch() 객체의 파라미터

```python
Prefetch(lookup, queryset=None, to_attr=None)
```

* Prefetch()의 기본 파라미터는 위와 같다.   

* lookup의 경우 기존에 prefetch_related()에 작성한 첫 번째 파라미터와 동일하고, queryset의 경우 필요한 옵션들을(filter 등) 포함해 queryset을 재 정의함으로써 lookup에 대한 조건을 부여할 수 있다.   

* 마지막으로 to_attr의 경우에는 prefetching 된 결과 메모리에 저장(cache)하여 재사용 할 수 있게 해주는 옵션이다. 너무 방대한 양의 쿼리가 아니라면 사용하는 것이 퍼포먼스 측면에서의 향상을 가져올 것이다.

## Prefetch() 객체를 활용하여 재 작성한 쿼리

```python
category = Category.objects.prefetch_related(Prefetch('post', to_attr='post.set()',queryset=Post.objects.all())).get(name='modi')
```

* 위에서 작성한 ORM을 Prefetch() 객체를 이용해 재 작성한 쿼리이다. 실제로 호출되는 SQL문을 살펴보면 이전과 비교해 달라진 것이 없음을 알 수 있다. 

## 추가 쿼리셋의 제어

```python
category = Category.objects.prefetch_related(Prefetch('post', to_attr='post.set()',queryset=Post.objects.filter(id=1))).get(name='modi')
```

* * *
* * *

## 정리

* 정리하자면, select_related(), prefetch_related()는 관계 있는 object를 Eager Loading 하기 위해 사용된다. 

* 다만 1:1, 1:N, N:M 관계 중에 따라 다르게 사용하는 것과, 추가적인 쿼리가 생성되는지에 대한 차이가 있을 뿐이다.

* 퍼포먼스 측면에서 이야기 하자면 한번에 많은 데이터를 미리 가져오는 것이 유리할 수도 있고, 때로는 작은 양의 데이터를 여러 번 가져오는 것이 유리할 수 도 있다. 

* 이러한 상황을 적절히 판단하여 위의 두 옵션들을 사용해야 할 것이다. 

* ORM의 특성상 원하는 SQL문을 직접적으로 만들어 낼 수 없기 때문에, 수행하려고 하는 SQL문을 먼저 떠올리는 것보다 필요한 데이터 리스트를 먼저 떠올리면서 ORM을 작성하는 편이 낫다고 생각한다.

> reference : https://leffept.tistory.com/312?category=950490