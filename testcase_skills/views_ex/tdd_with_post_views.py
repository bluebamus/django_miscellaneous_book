from django.shortcuts import render
from django.http import HttpResponse

# reference : https://wikidocs.net/11061

#  테스트만 통과하기 위한 방법으로 POST 요청으로 받은 값 그대로 돌려주는 형태로 코드를 수정한다.

def home_page(request):
    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    # return render(request, 'home.html')

    # test_uses_home_template 테스트는 요청이기 때문에 
    # item_text 변수가 존재하지 않아 이렇게 테스트를 실패한다. 
    # 따라서 키 값이 존재하지 않을 경우 예외처리를 위해 아래와 같이 뷰를 수정한다.

    # return render(request, 'home.html', {
    #     'new_item_text': request.POST['item_text']
    # })

    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', '')
    })