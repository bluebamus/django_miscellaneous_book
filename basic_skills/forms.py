from django import forms

from .validators import validate_tasty
from .models import Flavor, IceCreamStore

# 단지 폼에만 validate_tasty()를 이용하고자 할 때는 어떻게 해야 할까?
# 타이틀 말고 다른 필드에 이를 적용하고 싶을 때는 어떻게 할 것인가?
# 이러한 경우들을 처리하기 위해 커스텀 필드 유효성 검사기를 이용하는 커스텀 FlavorForm을 작성하기로 한다.

class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].validators.append(validate_tasty)
        self.fields["slug"].validators.append(validate_tasty)

    class Meta:
        model = Flavor
        fields = '__all__'


# 1. 다중 필드에 대한 유효성 검사
# 2. 이미 유효성 검사가 끝난 데이터베이스의 데이터가 포함된 유효성 검사

# 위 두 가지 경우 전부 커스텀 로직으로 clean() 또는 clean_<field_name>() 메서드를 오버라이딩 할 수 있는 최적의 경우다. 

# 기본 또는 커스텀 필드 유효성 검사기가 실행된 후, 장고는 다음 과정으로 
# clean() 메서드나 clean_<field_name>() 메서드를 이용하여 입력된 데이터의 유효성을 검사하는 절차를 진행한다.

# 1. clean() 메서드는 어떤 특별한 필드에 대한 정의도 가지고 있지 않기 때문에 
#   두 개 또는 그 이상의 필드들에 대해 서로 간의 유효성을 검사하는 공간이 된다.
# 2. 클린(clean) 유효성 검사 상태는 영속 데이터에 대해 유효성을 검사하기에 좋은 장소다. 
#    이미 유효성 검사를 일부 마친 데이터에 대해 불필요한 데이터베이스 연동을 줄일 수 있다.

class IceCreamOrderForm(forms.Form):

    slug = forms.ChoiceField(choices=[])
    # slug = forms.ChoiceField(choices=[],verbose_name="Flavor") #에러 발생
    # slug = forms.ChoiceField("Flavor",choices=[]) #에러 발생
    # CharField를 이용해 변환해 사용하면 verbose_name를 쓸수있을듯, lebel은 가능한듯
    # reference : https://pythonq.com/so/django/733731
    toppings = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields["slug"].choices = [(x.slug, x.title) for x in Flavor.objects.all()]
        self.fields["slug"].verbose_name="Flavor"
        
    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if Flavor.objects.get(slug=slug).scoops_remaining <= 0:
            msg='error'
            raise forms.ValidationError(msg)
        return msg

    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get("slug", "")
        toppings = cleaned_data.get("toppings", "")

        if "chocolate" in slug.lower() and "chocolate" in toppings.lower():
            msg = "Your order has too much chocolate."
            raise forms.ValidationError(msg)
        return cleaned_data


# 하나의 models, 두 개의 view, 두 개의 form
# form의 __init__을 어떻게 쓸 수 있는지, form의 상속을 어떻게 다루면 되는지 알 수 있음

class IceCreamStoreCreateForm(forms.ModelForm):

    class Meta:
        model = IceCreamStore
        fields = ("title", "block_address", )


class IceCreamStoreUpdateForm(IceCreamStoreCreateForm):

    def __init__(self, *args, **kwargs):
        super(IceCreamStoreUpdateForm, self).__init__(*args, **kwargs)
        self.fields["phone"].requird = True
        self.fields["description"].required = True

    class Meta(IceCreamStoreCreateForm.Meta):
        fields = ("title", "block_address", "phone", "description", )


# @ 중요함 : 장고의 폼 인스턴스 속성을 추가하는 방법 이해하기

# 때때로 장고 폼의 clean(), clean_FOO(), save() 메서드에 추가로 폼 인스턴스 속성이 필요할 때가 있다. 
# 이럴 경우에는 request.user 객체를 이용하면 된다.

# view에서 먼저 kwargs['user']에 넣어줘야함

class TasterForm(forms.ModelForm):

    class Meta:
        model = Flavor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') # request.user 객체를 self 변수, 인스턴스 변수에 넣어줌
        super().__init__(*args, **kwargs)


# @ 중요함 : 폼이 유효성을 검사하는 방법 알아두기

# form.is_valid()가 호출될 때 여러 가지 일이 다음 순서로 진행된다.

# 1.폼이 데이터를 받으면 form.is_valid()는 form.full_clean() 메서드를 호출한다.

# 2. form._full_clean()은 폼 필드들과 각각의 필드 유효성을 하나하나 검사하면서 다음과 같은 과정을 수행한다.
# 2-1. 필드에 들어온 데이터에 대해 to_python()을 이용하여 파이썬 형식으로 변환하거나 변환할 때 문제가 생기면 ValidationError를 일으킨다.
# 2-2. 커스텀 유효성 검사기를 포함한 각 필드에 특별한 유효성을 검사한다. 문제가 있을 때 ValidationError를 일으킨다.
# 2-3. 폼에 clean_<field>() 메서드가 있으면 이를 실행한다.

# 3. form.full_clean()이 form.clean() 메서드를 실행한다.

# 4.ModelForm 인스턴스의 경우 form.post_clean()이 다음 작업을 한다.
# 4-1. form.is_valid()가 True나 False로 설정되어 있는 것과 관계없이 ModelForm 데이터를 모델 인스턴스로 설정한다.
# 4-2. 모델의 clean() 메서드를 호출한다. 참고로 ORM을 통해 모델 인스턴스를 저장할 때는 모델의 clean() 메서드가 호출되지는 않는다.



# @ 모델폼 데이터는 폼에 먼저 저장된 이후 모델 인스턴스에 저장된다

# ModelForm에서 폼 데이터는 두 가지 각기 다른 단계를 통해 저장된다.
# 1. 첫 번째로 폼 데이터가 폼 인스턴스에 저장된다.
# 2. 그 다음에 폼 데이터가 모델 인스턴스에 저장된다.

# form.save() 메서드에 의해 적용되기 전까지는 ModelForm이 모델 인스턴스로 저장되지 않기 때문에 
# 이렇게 분리된 과정 자체를 장점으로 이용할 수 있다.

# 예를 들면 폼 입력 시도 실패에 대해 좀 더 자세한 사항이 필요할 때, 
# 사용자가 입력한 폼의 데이터와 모델 인스턴스의 변화를 둘 다 저장할 수 있다.

# import json

# from django.contrib import messages
# from django.core import serializers
# from .models import ModelFormFailuserHistory


# class FlavorActionMixin(self):

#     @property
#     def success_msg(self):
#         return NotImplemented

#     def form_valid(self, form):
#         messages.info(self.request, self.success_msg)
#         return super(FlavorActionMixin, self).form_valid(form)

#     def form_invalid(self, form):
#         form_data = json.dumps(form.cleaned_data)
#         model_data = serializers.seralize("json", [form.instance])[1:-1]
#         ModelFormFailuserHistory.objects.create(
#                 form_data=form_data,
#                 model_data=model_data
#         )
#         return super(FlavorActionMixin, self).form_invalid(form)


# Form.add_error()를 이용하여 폼에 에러 추가하기

class IceCreamReviewForm(forms.Form):
    # tester 폼의 나머지 부분

    def clean(self):
        cleaned_data = super().clean()
        flavor = cleaned_data.get("flavor")
        age = cleaned_data.get("age")

        if flavor == 'coffee' and age < 3:
            msg = 'Coffee Ice Cream is not for Babies.'
            self.add_error('flavor', msg)
            self.add_error('age', msg)

        return cleaned_data