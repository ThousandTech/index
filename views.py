from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views.decorators.cache import never_cache
# Create your views here.

# 过渡页配置：展示 REDIRECT_DELAY 秒后跳转到 REDIRECT_URL
REDIRECT_URL = "/guestbook/"
REDIRECT_DELAY = 30            # 等待秒数


@never_cache
def index(request):
    return render(
        request,
        "index/transfer.html",
        {
            "redirect_url": REDIRECT_URL,
            "redirect_delay": REDIRECT_DELAY,
        },
    )

