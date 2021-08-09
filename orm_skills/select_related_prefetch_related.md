# 테스트 방법

> commander : python manage.py shell_plus --print-sql --ipython

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
category = Category.objects.prefetch_related('post').get(name='modi')
for c in category.post.all():
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

## 추가 - QuerySet 캐시 사용 예제
```python
from django.utils.functional import cached_property

class Company(models.Model):
    name: str = models.CharField(max_length=128, null=False)
    tel_num: str = models.CharField(max_length=128, null=True)
    address: str = models.CharField(max_length=128, null=False)
  
  # @property여도 sql은 발생안함 하지만 매번 호출시마다 list comprehension이 풀리는게 싫어서 @cached_property를 사용함
   @cached_property
    def fire_product_list(self):
        return [product for product in self.product_set.all() if "불닭" in product.name]
   
  # cached_property 굳이 안써도 상관없음
   @property
    def noodle_product_list(self):
        return [product for product in self.product_set.all() if "라면" in product.name]

    

class Product(models.Model):
    name: str = models.CharField(null=False, max_length=128)
    price: int = models.PositiveIntegerField(null=False, default=0)
    product_owned_company: Company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=False)
# 위와 같이 property를 선언해놓고   `prefetch_related("product_set") `옵션만 있으면  
# company = company_query[0]
# company.fire_product_list # sql 발생 x
# company.noodle_product_list  # sql 발생 x
# 로직도 깔끔하고 sql도 안나간다 
company_queryset =Company.objects.prefetch_related("product_set") 




# 하지만 이렇게 `to_attr`을 지정하는경우이면 company.noodle_product_list 호출시 N+1문제 발생
company_queryset = (Company.objects
       .prefetch_related(Prefetch("product_set",queryset=Product.objects.filter(name__contains="불닭")
             ,to_attr="fire_product_list") # 해당 attr이 생성됨 
      )
)

# property를 사용해도 무조건 N+1 Problem 발생하는 경우

# self.xxx 로 접근해야 queryset의 즉시로딩 옵션의 해택을 볼수있다. 
# 아래와 같이 선언시 즉시로딩 옵션(prefetch_related,select_related)이 queryset에 주어져도 무조건 N+1 Problem발생
# @cached_property로 선언한다고 N+1 Problem이 해소되지 않는다 
#  @cached_property는 인스턴스 레벨 캐시이다 queryset의 캐시과 전혀 관련없음을 참고
@property
    def noodle_product_list(self):
        return [product for product in Product.objects.filter(company_id=self.id) if "라면" in product.name]
```

## QuerySet 이 생성하는 SQL 구조
* 이런식으로 QuerySet을 작성하면 아래와 같은 SQL이 발생한다.
* QuerySet이 만드는 SQL은 이 구조를 벗어나지 않는다. (FilteredRelation(), extra()같은 메서드들을 사용안한다는 전제 )
* 따라서 내가 원하는 SQL 또는 데이터 들이 이런 구조를 벗어나는지 한번 고민해보자
* 벗어난다면 NativeSQL 또는 .raw(RawQuerySet)을 사용하자

### QuerySet
```python
queryset = (Model.objects
            .select_related('정방향_참조필드1,','정방향_참조필드2',....) # n개 만큼 JOIN 한다. 
            .annotate(커스텀프로퍼티_블라블라=F('모델필드아무거나'),  
                      커스텀프로퍼티2_블라블라=Case(
                          When(Case조건절_모델필드아무거나__isnull=False,  # filter질의는 아무거나 다 가능 __gte, __in 등등...
                               then=Count('특정모델필드')), # 해당 값 기준으로 Count() 함수를 질의함
                          default=Value(0, output_field=IntegerField(
                                      help_text='해당 애트리뷰트 결과값을 django에서 무슨타입으로 받을건지 선언하는 param입니다.'),
                          ),
                      ))
            .filter(각종_질의~~~~)
            .prefetch_related(
                        Prefetch('역방향_참조필드', # 추가 쿼리는 새로운 쿼리셋이다 여기서 쿼리셋에 원하는 튜닝이 가능 
                                       queryset=(역방향_참조모델.objects
                                                 .select_related('역방향_참조모델의_정방향참조모델').filter(역방향_각종_질의문))
                                                # .prefetch_related('역방향_참조모델의_역(정)방향참조모델') 이런식으로도 가능
                                )
            )
            )
```

### SQL
```python
SELECT *
       모델필드아무거나 AS 커스텀프로퍼티_블라블라,
       CASE
           WHEN Case조건절_모델필드아무거나 IS NOT NULL
               THEN COUNT('특정모델필드')
        ELSE 0 END AS 커스텀프로퍼티_블라블라2,  # IntegerField()는 쿼리에서는 영향없음
      
FROM `orm_practice_app_order`
         LEFT INNER JOIN '정방향 참조필드1'  # INNER OUTER 는 ForignKey(null= True or False 값에 의해 결정
                         ON (~~~~)
         LEFT OUTER JOIN '정방향 참조필드2'  # INNER OUTER 는 ForignKey(null= True or False 값에 의해 결정
                         ON (~~~~)
WHERE (각종_질의~~~~)


SELECT *
FROM 역방향_참조모델
         INNER JOIN '역방향_참조모델의_정방향참조모델'
                    ON (~~~~~)
WHERE (역방향_각종_질의문 AND 메인쿼리의_Model.`related_id` IN (1,2,3,4,....));
```

> reference : https://leffept.tistory.com/312?category=950490   
> reference : https://github.com/KimSoungRyoul/Django_ORM_pratice_project/issues/9   
> reference : https://github.com/KimSoungRyoul/Django_ORM_pratice_project/issues/6