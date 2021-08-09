# QuerySet select_related, prefetch_related
* Django ORM을 처음 사용한다면 다음과 같이 매칭해서 이해하면 편하다.
  * 대체로 select_related()는 Join을 의도하고
  * prefetch_related()는 +1 Query를 의도하고 사용한다.
```python
.select_related('정방향_참조_필드')   # 해당 필드를 join해서 가져온다.
.prefetch_related('역방향_참조_필드') # 해당 필드는 추가쿼리로 가져온다.
```

# 명시하지 않아도 발생하는 Query
## select_related()로 명시하지 않아도 JOIN하는 경우
```python
# 1-1 이 QuerySet은 select_related()사용하지 않았어도 
# 필요한 조건을 inner join으로 해결하고 있다
# ORM이 이렇게 똑똑합니다...
(OrderedProduct.objects
 .filter(id=1, related_order__descriptions='sdfsdf')
 #.select_related('related_order'))
"""
SELECT *
    FROM "orm_practice_app_orderedproduct" 
    INNER JOIN "orm_practice_app_order" 
        ON ("orm_practice_app_orderedproduct"."related_order_id" = "orm_practice_app_order"."id")
    WHERE ("orm_practice_app_orderedproduct"."id" = 1 AND "orm_practice_app_order"."descriptions" = '주문의 상세내용입니다...1')
"""
```
* select_related()를 사용하지 않더라도 필요하다 판단되면 JOIN한다.
  * 하지만 이 경우 아래 주석처리한 .select_related(‘related_order’) 구문을 같이 붙여주는 것이 좋다.
* **select_related또는 prefetch_related 없는 QuerySet에서 Join 또는 +1 Query(추가 쿼리)가 발생했다면
명시적으로라도 select_related와 prefetch_related를 붙여주는 것이 좋다.**
  * 제 3자가 소스코드를 읽었을때 “이 필드는 JOIN을 해서 가져왔구나” 또는 “추가쿼리로 조회했구나” 와 같은 정보를 좀 더 명확하게 알수 있기 때문이다.

## prefetch_related()와 함께 불필요한 JOIN이 발생하는 경우
```python
# 문제가 없는 경우

# product_set을 prefetched_related로 가져오는 쿼리셋 선언
company_queryset: QuerySet = Company.objects.prefetch_related('product_set').filter(name='company_name1')
# 쿼리셋을 수행하면 아래와 같은 쿼리 2개 발생 (문제 없음)
comapny_list: List[Company]= list(company_queryset)
 """
  SELECT "orm_practice_app_company"."id", "orm_practice_app_company"."name", "orm_practice_app_company"."tel_num", "orm_practice_app_company"."address" 
      FROM "orm_practice_app_company" 
          WHERE "orm_practice_app_company"."name" = 'company_name1';
  
  -- prefetch_related() 구절이 아래 SQL을 부른다 --       
  SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id" 
      FROM "orm_practice_app_product" 
          WHERE "orm_practice_app_product"."product_owned_company_id" IN (1, 21);
 """
```
* 조건절을 하나만 더 추가한 경우
  * 이 경우는 prefetch_related()를 사용했음에도 불구하고 QuerySet이 Join으로 데이터를 조회한다.
```python
# 이런 경우 문제가 발생한다
# 하지만?
company_queryset: QuerySet = Company.objects.prefetch_related('product_set').filter(name='company_name1', product__name='product_name3')
# 이렇게 product관련 조건절이 한개 더 추가된다면 어떨까
# 쿼리셋을 수행하면 아래와 같은 잘못된 쿼리가 발생한다.
comapny_list: List[Company] = list(company_queryset)
"""
  SELECT "orm_practice_app_company"."id", "orm_practice_app_company"."name", "orm_practice_app_company"."tel_num", "orm_practice_app_company"."address" 
      FROM "orm_practice_app_company"
          INNER JOIN "orm_practice_app_product" ON ("orm_practice_app_company"."id" = "orm_practice_app_product"."product_owned_company_id") 
          --여기서 join이 발생했으면 join으로 product row를 다 조회 하는게 맞는데 join을 통해 조건절 검사만하고 --
          -- 두번째 쿼리에서 product를 한번 더 조회한다 --
      WHERE ("orm_practice_app_company"."name" = 'company_name1' AND "orm_practice_app_product"."name" = 'product_name3')  LIMIT 21;
  
  -- prefetch_related옵션으로 인해 해당 쿼리가 발생 -> 결과적으로 product를 불필요하게 2번 조회함 --
  SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id" 
      FROM "orm_practice_app_product" 
  WHERE "orm_practice_app_product"."product_owned_company_id" IN (1);
"""
# 이런 경우는 
# 1. prefetch_related('product_set') 이 구절을 제거하거나  (Inner Join 만 발생)
# 2. 이후 Prefetch(): +1 Query에 조건 거는 방법 사용
```
* 첫 쿼리에서 Product(orm_proactice_app_product)를 Join 했음에도 불구하고 추가 쿼리에서 한번더 Product를 조회한다.
  * 추가정보: 정방향 참조된 모델들도 prefetch_related()를 통해 join이 아닌 추가 쿼리로 가져올수는 있다.
* 주석처럼 1,2 방법이 있지만 JOIN으로 해결되는게 좋은 선택이다.
```python
# 1-3 이 쿼리는 의도한대로 +1개의 쿼리로 related_order를 조회한다 
# filter절에서 related_order에 대해 별다른 내용이 없어서 반항없이 개발자의 의도대로 따라준다.
OrderedProduct.objects.filter(product_cnt=30).prefetch_related('related_order')
"""
    SELECT * 
    FROM "orm_practice_app_orderedproduct"
     WHERE "orm_practice_app_orderedproduct"."product_cnt" = 30;
    SELECT * 
     FROM "orm_practice_app_order" 
     WHERE "orm_practice_app_order"."id" IN (~~~~~~~);
"""
```

## Prefetch(): +1 Query에 조건 거는 방법
* 상위 발생한 문제에서 의동한 것은 아래와 같은 쿼리였다.
```python
SELECT `orm_practice_app_company`.`id`,
        `orm_practice_app_company`.`name`,
        `orm_practice_app_company`.`tel_num`,
        `orm_practice_app_company`.`address`
  FROM `orm_practice_app_company`
  WHERE `orm_practice_app_company`.`name` = 'company_name1';
      

SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id"
    FROM "orm_practice_app_product"
WHERE "orm_practice_app_product"."product_owned_company_id" IN (1) 
     -- 이런식으로 조건절이 붙기를 기대함 >>> -- AND name = 'product_name3'; 
```
* **이렇게 prefetch_related()로 추가되는 쿼리에 조건을 걸기위해서는 Prefetch() 라는 문법을 사용해서 아래와 같이 QuerySet을 작성해야한다.**
```python
# prefetch_related()로 추가되는 쿼리에 조건을 걸어주고 싶다면 Prefetch()를 사용해야한다
 (Company.objects
         .prefetch_related(
                   Prefetch('product_set', queryset=Product.objects.filter(product__name='product_name3')))
         .filter(name='company_name1')
 )
```
## FilteredRelation(): JOIN ON절에 조건 거는 방법
* Inner Join 의 경우 큰차이가 없지만 Outer Join 의 경우 JOIN ON 절에 조건을 걸어주는 것과 WHERE 절에 조건을 걸어주는 것은 성능 차이를 보일 수 있다.
  * 간단히 이야기하면 ON 절은 JOIN 하면서 조건절을 체크하지만 WHERE절은 JOIN 결과를 완성시킨 후에 조건절을 체크한다.
* ON 절에 조건을 주고싶다면 아래와 같이 FilterdRelation 을 사용하자.
```python
# Join Table의 on 구문에 조건 걸기  여기서 .select_related('this_is_join_table_name')
    (Product.objects
     #.select_related('this_is_join_table_name') 안 붙어도 되지만 쿼리셋 가독성 측면에서 붙는게 더 좋다
     .annotate(this_is_join_table_name=FilteredRelation('product_owned_company',
                                                           condition=Q(product_owned_company__name='company_name34'),
                                                       ),
              )
     .filter(this_is_join_table_name__isnull=False)
    )
"""
SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id" 
FROM "orm_practice_app_product" 
INNER JOIN "orm_practice_app_company" this_is_join_table_name
    ON ("orm_practice_app_product"."product_owned_company_id" =  this_is_join_table_name."id" 
          AND ( this_is_join_table_name."name" = 'company_name34') # 이 조건을 걸기위해 FilterRelation()을 사용한다
        ) 
WHERE  this_is_join_table_name."id" IS NOT NULL ;
"""
```

* 단순히 filter()에 모든 조건을 때려박아도 QuerySet이 최대한 좋은 쿼리를 만들어주지만 의도한 쿼리가 나오지 않는다면
  * prefetch_related()은 Prefetch()로 조건절을 좀 더 섬세하게 다룰 수 있다.
  * select_related()은 FilterRelation()로 조건절을 좀 더 섬세하게 다룰 수 있다.

## QuerySet이 Inner, Outer Join을 선택하는 기준
* 모델을 마이그레이션 할때
  * field= model.ForeignKey( null = False ) 이면 Inner Join 이고
  * field= model.ForeignKey( null = True ) 이면 Left Outer Join 이다.

* 그러면 null=True인 외래키 필드는 inner join을 할 수 없는가?
  * 할 수 없어야 한다.
    * null=True인 엔티티를 QuerySet이 inner join으로 조회한다면 join되는 테이블쪽이 null이면 SQL결과 데이터에서 누락된다.

* 그러나 방법이 없는 것은 아니다.( 하지만 사용하지 않는것이 제일 좋다 )
```python
(Product.objects
    .filter(price__gt=24000, product_owned_company__isnull=False)
    .select_related('product_owned_company')
)
"""
SELECT * 
FROM "orm_practice_app_product" 
  INNER JOIN "orm_practice_app_company" ON ("orm_practice_app_product"."product_owned_company_id" = "orm_practice_app_company"."id")
WHERE ("orm_practice_app_product"."price" > 24000 AND "orm_practice_app_product"."product_owned_company_id" IS NOT NULL);  
"""
```

* Model의 ForiegnKey(null=False)로 수정하기
  * 이렇게 수정만 하고 마이그레이션을 안하면 Table에는 해당 필드가 null=True이지만 QuerySet으로 조회시에는 inner join을 할 수 있다.

* Right Outer Join을 하는 법
  * 불가능하다
  * ORM에서 주체가 되는 엔티티는 항상 왼쪽에 존재한다.
```python
select * from “(left)주체가되는 테이블” join "(right)주체에 연관된 테이블"
```
* 주체가 null 이면서 연관된 데이터가 존재하는 결과값을 가져오는 Right Outer Join이 이루어지는 경우는 없다.
* subquery나 복잡한 query를 만드는 과정에서 right outer join이 발생할 수는 있어도 단순 외래키 관계에서 Right Outer Join이 만들어지는 경우는 없다.
* **Right Outer Join이 필요한 경우가 있다면 거꾸로 조인되는 테이블을 주체로 사용해서 QuerySet을 만들 수 없는지 생각해봐야한다.**
  
> reference : https://medium.com/deliverytechkorea/django-queryset-1-14b0cc715eb7   
> * reference : https://github.com/KimSoungRyoul/Django_ORM_pratice_project/tree/master   

> queryset 동작에 대해 심도 설명 : https://medium.com/deliverytechkorea/django%EC%97%90%EC%84%9C%EB%8A%94-queryset%EC%9D%B4-%EB%8B%B9%EC%8B%A0%EC%9D%84-%EB%A7%8C%EB%93%AD%EB%8B%88%EB%8B%A4-2-5f6f8c6cd7e3

> 테이블 관계에 따른 join 및 캐시 사용법 : https://engineer-mole.tistory.com/137