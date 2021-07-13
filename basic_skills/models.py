from django.urls import reverse
from django.db import models

from .validators import validate_tasty

# validate_tasty()를 다른 종류의 디저트 모델에 적용하기 위해 우선 TastyTitleAbstractModel이라는
# 프로젝트 전반에서 이용할 수 있는 추상화 모델을 추가한다. 

# Flavor와 Milkshake 모델이 각기 다른 모델이라 가정할 때 유효성 검사기를 하나의 앱에만 추가하는 것은 적절하지 않을 것이다.

# 따라서 그 대신 core/models.py 모듈을 만들고 TastyTitleAbstractModel을 이곳에 추가하겠다. 
# - 이 테스트에서는 core app을 따로 분리하지 않고 같은 models.py 에서 구현함

class TastyTitleAbstractModel(models.Model):
    title = models.CharField(max_length=255, validators=[validate_tasty])

    class Meta:
        abstract = True


STATUS = (
    (0, "zero"),
    (1, "one"),
)

class Flavor(TastyTitleAbstractModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    scoops_remaining = models.IntegerField(default=0, choices=STATUS)

    def get_absolute_url(self):
        return reverse("flavors:detail", kwargs={"slug": self.slug})

# @ 폼 필드 해킹하기(두 개의 CBV, 두 개의 폼, 한 개의 모델)

# 사용자가 title과 block_address는 입력해야 하지만 phone과 description 필드는 입력하지 않아도 되게 구성되어 있다. 
# 후에 사용자가 phone과 description 필드를 추가적으로 업데이트하는 것이 가능하도록 구성하고 싶다면 어떻게 해야할까?

# 장고 폼을 사용할 땐 반드시 다음 사항을 기억하자.

# 실체화된 폼 객체는 유사 딕셔너리 객체인 fields 속성 안에 그 필드들을 저장한다. 
# 따라서 폼으로 필드의 정의를 복사, 붙이기 하는 대신에 간단하게 ModelForm의 __init__() 메서드에서 새로운 속성을 적용하면 된다.

# go to IceCreamStoreUpdateForm() in froms.py

class IceCreamStore(models.Model):
    title = models.CharField(max_length=100)
    block_address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("store_detail", kwargs={"pk": self.pk})


class ModelFormFailuserHistory(models.Model):
    form_data = models.TextField()
    model_data = models.TextField()