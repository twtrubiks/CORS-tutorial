# Same-Origin Policy and CORS Tutorial 📝

這篇文章主要是要帶大家了解 Same-Origin Policy 以及 CORS 📝

[Youtube Tutorial](https://youtu.be/Md9wxO6BU_c)

如果有介紹不清楚或有錯誤的地方，歡迎大家 issuse 給我 :smile:

部分說明我會搭配程式碼講解，並且以 [Django](https://www.djangoproject.com/start/) 來當範例，

範例基本上是以這兩篇為基礎修改而成的 :

* [Django 基本教學 - 從無到有 Django-Beginners-Guide](https://github.com/twtrubiks/django-tutorial)

* [Django-REST-framework 基本教學 - 從無到有 DRF-Beginners-Guide](https://github.com/twtrubiks/django-rest-framework-tutorial)

所以如果是對 [Django](https://www.djangoproject.com/start/) 不熟悉且又想學的人，建議先看一下上面兩篇文章 :grin:

溫馨小提醒  :kissing_heart:

[django-rest-framework-backed](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-rest-framework-backed) 是基於 [Django-REST-framework 基本教學 - 從無到有 DRF-Beginners-Guide](https://github.com/twtrubiks/django-rest-framework-tutorial) 修改而成。

[django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) 則是基於 [Django 基本教學 - 從無到有 Django-Beginners-Guide](https://github.com/twtrubiks/django-tutorial) 修改而成。

## 前言

因為我主要是做後端的，所以我開發的 API 通常都是經過 [Postman](https://www.getpostman.com/) 或是 [Paw](https://paw.cloud/) ，又或是其他的測試 API 的工具

測試通過後，確認這些 API 沒問題之後，就再將這些 API 整理成文件 ( 之前有介紹過撰寫文件的方式，可參考

[aglio_tutorial](https://github.com/twtrubiks/aglio_tutorial) 以及 [django-rest-framework-swagger-tutorial](https://github.com/twtrubiks/django_rest_framework_swagger_tutorial) )，然後給前端工程師串 API，但有時候再串接時總

是會得到 API 噴錯，一看之後，才發現是跨域的問題 :sweat: ，所以既然碰上了，也躲不掉，就乾脆來寫一篇文章，

順便也讓自己多了解一點吧 :satisfied:。

在開發網站的時候，遇到跨域請求是個家常便飯的問題，因為涉及到網站安全，所以 browser 是會拒絕跨域請求的。

我會把 Same-Origin Policy 以及 CORS 放在一起介紹的原因是因為他們互相有關係，Same-Origin Policy 是原因，而

CORS 是我們解決 Same-Origin Policy 的方法之一 （ 為什麼我會說之一呢 ？ 因為還有其他的解決方法，只不過大家

比較常用的解決方案是 CORS  ）。讓我們開始介紹吧 :grinning:

## Same-Origin Policy

Same-Origin Policy 又稱 **同源政策**

同源是指協定相同、域名 ( 主機位置 ) 相同、埠號相同。

下面舉幾個例子，讓大家更了解什麼才是同源  :hushed:，是否和  `http://twtrubiks.com/dir1/index.html` 同源

| URL | 是否同源 | 理由 |
| ------------------| ------ | ------ |
| `http://twtrubiks.com/dir2/page2.html` | 同源 |  |
| `http://twtrubiks.com/dir/other/page2.html` | 同源 |  |
| `https://twtrubiks.com/secure.html` | 不同源 | 協定不同 |
| `http://twtrubiks.com:8080/index.html` | 不同源 | 埠號不同 |
| `http://new.com/index.html` | 不同源 | 域名 ( 主機位置 ) 不同 |

同源政策的目的，是為了保證用戶訊息的安全，防止惡意的網站竊取資料。

但是有時候會帶給我們一些不便的地方，

為了解決同源政策的限制，我們必須跨域，跨域方法的實現我們可以使用:

* JSONP
* Websocket
* CORS
* Cross-document messaging ( html5 postMessage )

## 突破同源政策的限制，跨域

這次的重點，我將介紹 **JSONP** 以及 **CORS** 並且用程式碼介紹，讓大家更清楚了解 :+1:。

我們先來看看跨域的錯誤訊息，再看錯誤訊息之前，我先解釋一下目錄底下的資料夾，

首先，模擬前後端分離，雖然都是用 [Django](https://www.djangoproject.com/start/) 實作的，

我們把 [django-rest-framework-backed](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-rest-framework-backed) 想成是後端，然後把 [django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) 想成是前端 ，

[django-rest-framework-backed](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-rest-framework-backed) run 起來的網址為 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

[django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) run 起來的網址為 [http://127.0.0.1:8002/](http://127.0.0.1:8002/)

還記得前面所說的嗎 ? 埠號不同，就是不同源。

現在我們試試看從前端使用 Ajax 得到 `http://127.0.0.1:8000/api/music/1/` 這支 API 的資料，

我們將 [django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) 裡面的 templates/[hello_django.html](https://github.com/twtrubiks/CORS-tutorial/blob/master/django-frontend/templates/hello_django.html) 修改為

( 就是簡單的 Jquery Ajax )

```javascript
     // ajax
    var url = 'http://127.0.0.1:8000/api/music/1/';

    $.ajax({
        url: url,
        method: 'GET'
    }).success(function (data, textStatus, jqXHR) {
        console.log('success');
        console.log(data);
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log('failed');
        console.log(jqXHR)
    });
```

然後我們進去 [http://127.0.0.1:8002/hello/](http://127.0.0.1:8002/hello/) 按下 F12 開發人員工具

接著你會看到一段 ERROR

**XMLHttpRequest cannot load http://127.0.0.1:8000/api/music/1/. No 'Access-Control-Allow-Origin' header is present on the requested resource. Origin 'http://127.0.0.1:8002' is therefore not allowed access.**

![](https://i.imgur.com/oIqK58q.png)

這就是跨域的限制，簡單說，當我的前端 [django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) 對後端 [django-rest-framework-backed](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-rest-framework-backed)

發起 Ajax request 時，就會發生跨域的問題，原因就是因為 Same-Origin Policy。

### JSONP

JSONP 是跨域的一種方法，但不推薦，原因後面會解釋。JSONP 的全名為 JSON with Padding，

最簡單的概念就是使用跨域的 html tag  ( 像是  `<script src=""></script>` ) 的方式來存取， 又或是大

家常用的 img tag，所以一定只能發送 GET Method 。

我知道有些人現在可能會在想，阿你西勒供三小 :question: :question: :question:（黑人問號）

剛剛在上面大家看過跨域會噴的錯誤了，

那讓我們再來看看一個例子，假如我用 img tag 讀取一張圖片，看看會發生什麼事情，

我們將 [django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) 裡面的 templates/[hello_django.html](https://github.com/twtrubiks/CORS-tutorial/blob/master/django-frontend/templates/hello_django.html) 增加

```html
<img src="https://raw.githubusercontent.com/twtrubiks/django-shop-tutorial/master/shop/static/img/no_image.png" >
```

疑？ 我們竟然可以正常讀取圖片 :hushed:

![](https://i.imgur.com/CcSYs60.png)

這是為什麼呢 ？ 難道是什麼妖術 :scream:

原因就是這類的 html tag 是可以跨域的，其他還有像是 script tag ，link tag ......

在網頁上使用 script tag 時可以不受跨域的限制，JSONP 就是利用這個來實現跨域。

在網頁上直接發起一個跨域的 Ajax 請求是不被允許的，但是，如果透過跨域的 html tag

即可突破這個限制，就像剛剛為大家展示的可以在自己的頁面上使用 img tag 讀取一張跨域的圖片。

那我們該如何實現呢 ？

首先，需要將 Ajax 中的 dataType 從 JSON 改為 JSONP（ API 也需要支持 JSONP）格式。

然後 JSONP 只能使用 GET Method 發起跨域 request。跨域 request 還需要 Server 端配合，

也就是設定 callback，這樣才能完成跨域 request。

說了那麼多，讓我用程式碼來實作一遍  JSONP 跨域，

首先，我們先來改後端，也就是 [django-rest-framework-backed](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-rest-framework-backed) 的部分，將 musics/[views.py](https://github.com/twtrubiks/CORS-tutorial/blob/master/django-rest-framework-backed/musics/views.py) 的部分增加

```python
# [ GET ] /api/music/all_singer/
@list_route(methods=['get'])
def all_singer(self, request):
    result = 'callback' + "(" + json.dumps({"key": "value", "key2": "value"}) + ")"
    response = HttpResponse(result)
    return response
```

回傳 callback({"key": "value", "key2": "value"}) 資料格式

然後我們在前端 [django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) 的部分，將 templates/[hello_django.html](https://github.com/twtrubiks/CORS-tutorial/blob/master/django-frontend/templates/hello_django.html) 增加

```javascript
// ajax use jsonp dataType
var url_jsonp = 'http://127.0.0.1:8000/api/music/all_singer/';
$.ajax({
    url: url_jsonp,
    type: "GET",
    dataType: "jsonp",
    jsonp: "callback",
    jsonpCallback: "callback",
    success: function (data) {
        var result = JSON.stringify(data);
        console.log(result);
    }
});
```

接著我們再來看看結果

![](https://i.imgur.com/WgPcjqD.png)

從圖中可以看出我們成功地透過 JSONP 的方法跨域了 :yum:

不過不推薦 JSONP 這種方法，

缺點除了是只能發送 GET Method ( 也就是如果你想要用 POST Method 是沒辦法的 ) 之外，

script tag 會將 js 代碼執行，所以可能會被攻擊 （ 被植入惡意代碼），

而你的後端也必須配合，不夠友善 :pensive:

唯一優點就是不會有瀏覽器相容問題（ 相容性強 ），因為是透過 html tag 完成跨域。

## CORS

什麼是 CORS？ 他可以吃嗎  :joy:

CORS 全名為 Cross-Origin Resource Sharing，又稱 跨域資源共享，

是一種跨域訪問的機制，可以讓 Ajax 實現跨域訪問。

CORS 的原理，我們先從下面兩張圖來看

拒絕請求的 XHR Headers

![](https://i.imgur.com/KqZNBcd.png)

接受請求的 XHR Headers

![](https://i.imgur.com/3Ydv6kh.png)

當透過  XMLHttpRequest ( XHR ) 發送 request 時，browser 會在請求中加入一個 Origin，

然後檢查 Origin 是否通過，如果接受，就可以得到資料，並且 response header 裡會包含

`Access-Control-Allow-Origin: *` ; 反之，如果不通過，就會被檔下來，並且 response header

裡 **不會** 包含 `Access-Control-Allow-Origin`。

說穿了，其實在 Server 的 response header 中，加入 `Access-Control-Allow-Origin: *` 就可以支持 CORS

讓我用程式碼來實作一遍 CORS，

我們直接去修改 [Django](https://www.djangoproject.com/start/)  中的 musics/[views.py](https://github.com/twtrubiks/CORS-tutorial/blob/master/django-rest-framework-backed/musics/views.py) ，

```python
# [GET] /api/music/{pk}/detail/
@detail_route(methods=['get'])
def detail(self, request, pk=None):
    music = get_object_or_404(Music, pk=pk)
    result = {
        'singer': music.singer,
        'song': music.song
    }
    response = HttpResponse( json.dumps(result))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
```

然後我們在前端 [django-frontend](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-frontend) 的部分，將 templates/[hello_django.html](https://github.com/twtrubiks/CORS-tutorial/blob/master/django-frontend/templates/hello_django.html) 增加

```javascript
 // ajax backed add Response Header: Access-Control-Allow-Origin
var url_view = 'http://127.0.0.1:8000/api/music/1/detail/';
$.ajax({
    url: url_view,
    method: 'GET'
}).success(function (data, textStatus, jqXHR) {
    console.log('success');
    console.log(data);
}).error(function (jqXHR, textStatus, errorThrown) {
    console.log('failed');
    console.log(jqXHR)
});
```

![](https://i.imgur.com/osvB7uB.png)

我們成功的跨域 :smiley:

透過簡單的  `Response Header: Access-Control-Allow-Origin:*` 方法即可完成。

但這並不是一個很好的方法，比較標準的應該是去 Django 中的 [Middleware](https://docs.djangoproject.com/en/1.11/topics/http/middleware/) 裡實現才對，

為什麼我會這樣說，在  [Django](https://www.djangoproject.com/start/) 官網中的 CORS 部分有提到

***The best way to deal with CORS in REST framework is to add the required response headers in middleware.
This ensures that CORS is supported transparently, without having to change any behavior in your views.***

來源可參考 [http://www.django-rest-framework.org/topics/ajax-csrf-cors/#cors](http://www.django-rest-framework.org/topics/ajax-csrf-cors/#cors)

幸運的，也有人實作出來 :grinning:

[django-cors-headers](https://github.com/ottoyiu/django-cors-headers/)

簡單介紹一下使用方法，

安裝 django-cors-headers，先使用命令提示字元（ cmd ） 執行下列指令

```cmd
pip install django-cors-headers
```

接著到 [django-rest-framework-backed](https://github.com/twtrubiks/CORS-tutorial/tree/master/django-rest-framework-backed) 裡的  django_rest_framework_tutorial/[settings.py](https://github.com/twtrubiks/CORS-tutorial/blob/master/django-rest-framework-backed/django_rest_framework_tutorial/settings.py) 裡增加

```cmd
INSTALLED_APPS = (
    ...
    'corsheaders',
    ...
)
```

然後我們再到 MIDDLEWARE 裡面增加

```cmd
MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
```

要注意順序的問題（為了鍛鍊自己，所以我決定不翻譯，我絕對不是懶 ），原因解釋如下

**CorsMiddleware should be placed as high as possible, especially before any middleware that can generate responses such as Django's CommonMiddleware or Whitenoise's WhiteNoiseMiddleware. If it is not before, it will not be able to add the CORS headers to these responses.**

最後我們再加上

```python
CORS_ORIGIN_ALLOW_ALL = True
```

**Configure the middleware's behaviour in your Django settings. You must add the hosts that are allowed to do cross-site requests to CORS_ORIGIN_WHITELIST, or set CORS_ORIGIN_ALLOW_ALL to True to allow all hosts.**

**CORS_ORIGIN_ALLOW_ALL**
If True, the whitelist will not be used and all origins will be accepted. Defaults to False.

也有白名單的功能 **CORS_ORIGIN_WHITELIST**，設定如下

```pyhton
CORS_ORIGIN_WHITELIST = (
     'google.com',
     'hostname.example.com',
     '127.0.0.1:8002',
)

```

現在我們把 Server run 起來，然後前端的部份，一樣使用文章前面的程式碼，

也就是一開始介紹被跨域限制的部份。

```javascript
    // ajax
    var url = 'http://127.0.0.1:8000/api/music/1/';

    $.ajax({
        url: url,
        method: 'GET'
    }).success(function (data, textStatus, jqXHR) {
        console.log('success');
        console.log(data);
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log('failed');
        console.log(jqXHR)
    });
```

這次，我們成功的跨域了 :clap:

![](https://i.imgur.com/YGPPvnk.png)

如果你仔細觀察 XMLHttpRequest ( XHR )，你會發現多了 `Access-Control-Allow-Origin：*`

沒 CORS 時，

![](https://i.imgur.com/rQncAYc.png)

有 CORS 時，

![](https://i.imgur.com/b5Mbq4h.png)

更多詳細的資料可參考 [django-cors-headers](https://github.com/ottoyiu/django-cors-headers/)

對於 Server 端來說，如果要提供跨站存取的權限就是設定 `Response Header: Access-Control-Allow-Origin`。

在實作方面可以透過寫 [Middleware](https://docs.djangoproject.com/en/1.11/topics/http/middleware/) 來處理。

CORS 的優點，簡單方便，也不用特別去改變後端的程式，像 JSONP 就真的小麻煩:expressionless:，而且 CORS 也支援

POST Method，唯一的缺點可能就是有些瀏覽器不支援，但我相信這會慢慢改善，別再用 IE 7，IE 8 了 :angry:

## 後記

這次介紹了 Same-Origin Policy 以及 CORS 給大家認識，希望大家以後面試被問到或是遇到這類的問題時，

可以很清楚的了解說到底是為什麼？免得當別人提到這些東西時，你完全不了解。

這次也搭配了程式碼教學，這樣整體看下來相信大家會比較有 feel  :heart_eyes:，我們從原理先了解，了解之後，我們

再從實作面下去解決，相信會更能增加大家對他的了解。

其實還有一個東西也可以介紹，稱為 CSRF ( Cross Site Request Forgery )，但這次就暫時先不介紹，大家

有興趣的話，可以先看 [Same-Origin Policy, CORS and CSRF](https://hackmd.io/s/H1cY3TTYe#same-origin-policy-cors-and-csrf) 壓壓驚，下次有機會我再整理給大家:smile:

最後，因為文章內容很多是我去網路上查資料，自己再加以整理的，如果有介紹不清楚或有錯誤的地方，

歡迎大家 issuse 給我，謝謝大家 :relaxed:

## 執行環境

* Python 3.6.2

## Reference

* [Same-Origin Policy, CORS and CSRF](https://hackmd.io/s/H1cY3TTYe#same-origin-policy-cors-and-csrf)
* [django-cors-headers](https://github.com/ottoyiu/django-cors-headers/)

## License

MIT license
