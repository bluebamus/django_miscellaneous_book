
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from ..models_ex.models_two_scoops_of_django import Flavor
from django import forms

# reference : https://blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=pjok1122&logNo=221609547295
# sub reference : https://m.blog.naver.com/pjok1122/221608776435

# @ 1. DetailView (Template에 추가 데이터 전달하기)

class OrderForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

# (1) 모델을 직접 넘겨주는 방법 말고도 queryset을 넘겨주는 방법이 있습니다. 
#     모델을 넘겨주는 것과 생성된 모든 객체를 넘겨주는 것은 동일합니다.

# (2) DetailView에서 생성된 context는 template에서 product라는 이름으로 접근이 가능합니다.

# (3) context는 현재 Product라는 모델의 데이터만 접근이 가능합니다. 
#     만약 template에게 다른 데이터를 더 전달하고 싶다면 get_context_data를 오버라이딩해야 합니다.

# (4) 오버라이딩 전에 정의되어있던 get_context_data를 먼저 호출합니다.

# (5) 자신이 원하는 값을 dict 형태로 추가할 수 있습니다.    

class ProductDetail(DetailView):
    template_name = "product/detail.html"
    #queryset = Product.objects.all()                                (1)
    model = Flavor
    context_object_name = "product"                                # (2)

    def get_context_data(self, **kwargs):                          # (3)
        #생성된 context는 Template으로 전달됨.
        context = super().get_context_data(**kwargs)               # (4)
        context['form']=OrderForm(self.request)                    # (5)
        return context


    
# @ 2. ListView (queryset 만들기)

# 앞서 queryset을 만들 수 있다고 했지만, request의 session 값을 통해 데이터를 전달하고 싶은 경우 불가능합니다. 
# 이때에는 queryset을 생성하는 메서드를 오버라이딩해서 사용할 수 있습니다.

class OrderList(ListView):
    template_name = "order/list.html"
    #model = Flavor
    context_object_name = "orders"
    def get_queryset(self, **kwargs):                                                          # (1)
        #user는 객체이므로, user 밑에 email과 비교를 원한다면 user__email 사용
        queryset = Flavor.objects.filter(user__email=self.request.session.get('user'))          # (2)
        return queryset

# (1) 쿼리 셋을 생성하는 메서드입니다.

# (2) OrderList 필드 영역에서는 사용할 수 없었던 self 연산을 메서드 내에서는 사용이 가능하다는 장점이 있습니다.


# @ 3. Form (생성자 오버라이딩)

from django.db import transaction

class OrderForm(forms.Form):
    # 주문 객체 생성. (Order의 모델에는 user도 포함되어있음. )
    # Session은 request에 존재하므로 Form에서는 사용 불가.
    # 따라서 FormView의 생성자가 request를 포함하도록 변경

    def __init__(self, request, *args, **kwargs):          #     (1)
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required':'수량을 입력해주세요.'
        }, label="수량")
    product = forms.IntegerField(                           #    (2)
        error_messages={
            'required':'상품을 선택해주세요.'
        },
    label="상품", widget=forms.HiddenInput
    )

    def clean(self):

        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        email = self.request.session.get('user')             #     (3)
        self.product = product

        if quantity and product and email:
            product = Flavor.objects.get(pk=product)
            user = Flavor.objects.get(email=email)
            if product.stock < quantity:
                self.add_error('quantity', '재고보다 많은 주문은 할 수 없습니다.')
                return
            with transaction.atomic():                   #         (4)
                order = Flavor(
                    user=user,
                    product=product,
                    quantity=quantity
                )
                order.save()
                product.stock-=quantity
                product.save()
        
# (1) 생성자 오버라이딩입니다. 
#     request를 필수적으로 전달하도록 변경하고, self.request로 접근할 수 있도록 
#     self.request = request로 대입합니다. 
#     현재 로그인 한 사용자의 정보를 가져오기 위해서 사용되는 부분입니다. 

# (2) product는 상품에 대한 id를 저장하기 위해 만들어졌으나 
#     HiddenInput으로 설정하여 실제로 값이 출력되지는 않도록 합니다. 
#     여기서 user를 Form에 작성하지 않는 이유는 user를 Hidden으로 설정하더라도, 
#     크롬의 "검사하기" 기능으로 얼마든지 로그인 없이 유저를 변경할 수 있기 때문입니다.

# (3) self.request를 사용하여 객체를 가져오는 과정입니다.

# (4) transaction.atomic은 여러 개의 SQL 문을 하나의 연산으로 보고 처리하도록 하는 함수입니다. 
#     order는 접수가 되었는데, 에러로 인해 상품의 재고가 감소하지 않는 문제점을 사전에 제거합니다. 
#     ( 위치는 django.db.transaction에 존재합니다. )


# @ 4. FormView (객체의 전달 인자 추가)

from django.views.generic.edit import FormView
from django.shortcuts import render

class OrderCreate(FormView):
    form_class = OrderForm
    success_url = "/product/"
    
    #Form 객체를 생성할 때, request도 같이 전달하도록 변경해야 함.
    def get_form_kwargs(self, **kwargs):                          #        (1)
        kw = super().get_form_kwargs(**kwargs)
        kw.update({                                                #       (2)
            'request': self.request
        })
        return kw

    #실패 했을 때, 어디로 redirect할 지 결정을 안했기 때문에 에러 발생.
    def form_invalid(self, form):                                   #      (3)
        #실패 했을 때의 작업.
        #form : <tr><th><label> .... </td></tr> 형태의 html코드를 가지고 있는 객체.
        #redirect하면 ProductDetail에서 OrderForm을 새로 생성하기 때문에 에러 메시지가 전달되지 않음.

        product = Flavor.objects.get(pk=form.product)
        return render(self.request, 'product/detail.html', {'form': form, 'product':product})


# (1) get_form_kwargs()는 form_class로 지정된 Form 객체를 만드는 메서드입니다.

# (2) kw.update({ }) 명령을 통해 인자를 추가할 수 있습니다. 
#     인자를 추가하는 이유는, 위에서 OrderForm의 생성자에 request를 필수 요소로 지정했기 때문입니다. 

# (3) 현재 연결된 template_name이 없기 때문에 실패했을 때의 작업을 처리해주어야 합니다. 
#     form_invalid(self, form)은 실패했을 때의 처리하는 메서드입니다.

# (4) render를 이용해서 html 코드를 뿌려주고, 에러 메시지가 담겨있는 form과 현재의 상품정보인 product를 전달합니다.


# @ 5. Form, Template, FormView의 동작 과정(★★)

# (1) FormView의 form_class를 template_name에게 전달해줍니다.

# (2) Template에서 form이라는 이름으로 Form을 사용할 수 있습니다.

# (3) Template의 <form>에서 POST로 데이터가 넘어올 경우, Form 객체의 clean() 메서드가 실행됩니다.

# (4) Form 객체의 clean() 메서드는 사전에 정의된 조건, 모든 데이터가 기입되었는지를 확인합니다.

# (5) clean()이 오버라이딩 되었다면 개발자가 추가한 조건 또한 통과하는지 검사합니다.

# (6) 통과하지 못한 경우 self_add_error('필드명', '에러 설명')을 이용해 에러를 추가하고, 
#     통과한 경우 객체를 생성하거나 일을 처리합니다.

# (7) 최종적으로 clean()에서 유효성 검사가 끝나고, 유효하다면 
#     FormView에서 정의한 form_valid()를 호출하고 success_url로 redirect 됩니다.

# (8) 유효하지 못한 경우, form_invalid()를 호출합니다.