function buildQuery(params) {
    return Object.keys(params).map(function (key) {return key + '=' + encodeURIComponent(params[key])}).join('&')
}
function buildUrl(baseUrl, queries) {
    return baseUrl + '?' + buildQuery(queries)
}

// 네이버 sdk 에서는 token 으로 설정되어 있는데 이렇게 하면 
// 어러분의 서버에서 인증토큰을 받는 것이 아니라 브라우저에서 전달하는 인증토큰을 사용해야 하기 때문에 
// 보안에 취약할 수 있습니다. 

// 즉 이 방식으로 전달받은 것들로 사용자 가입을 한다면 
// 악의적으로 다른 사람의 access_token 을 도용해도 확인할 수 있는 방법이 없습니다. 

// 여러분이 소셜로그인된 사용자의 회원정보를 서버에 저장하지 않는 경우에 적합한 방식입니다. 
// 여기서는 네이버 소셜로그인을 하고 회원정보를 이용해서 서버에 회원을 가입시키고 
// 회원정보를 저장할 것이기 때문에 code 타입으로 설정하셔야 합니다.

// state 는 아주 중요한 값입니다. 
// csrf 등의 공격으로 사용자가 해당 서비스를 접속하지 않고 
// 소셜로그인을 시도하는 경우를 차단하기 위해서 필요한 값입니다. 

// 임의의 문자열이 필요한데 서버에서도 올바른 값인지 비교할 수 있도록 
// 로그인 csrfmiddlewaretoken 을 이용했습니다. 

function naverLogin() { // 네이버 로그인
    params = {
        response_type: 'code',
        client_id:'76QbowB7fMfu3DkfWCiI',
        redirect_uri: location.origin + '/naveroauth/user/login/social/naver/callback/' + location.search,
        state: document.querySelector('[name=csrfmiddlewaretoken]').value
    }
    console.log(params.redirect_uri)
    url = buildUrl('https://nid.naver.com/oauth2.0/authorize', params)
    location.replace(url)
}