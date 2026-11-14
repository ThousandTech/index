from django.shortcuts import render,redirect
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from .services import get_random_websites, match_target_url
import random


# Create your views here.

# 过渡页配置：展示 REDIRECT_DELAY 秒后跳转到 REDIRECT_URL
REDIRECT_URL = "thousand-tech.com"
REDIRECT_DELAY = 7            # 等待秒数
PROBABILITY_THRESHOLD = 0.1


@never_cache
def index(request):

    random_val = random.random()
    if random_val > PROBABILITY_THRESHOLD:
        return render(
            request,
            "index/home.html",
            {
                "recommended_websites":get_random_websites()
            }
        )

    else:
        return render(
            request,
            "index/transfer.html",
            {
                "redirect_url": REDIRECT_URL,
                "redirect_delay": REDIRECT_DELAY,
            },
        )


@never_cache
@require_GET
def search(request):
    query = request.GET.get("q","")
    target_url = match_target_url(query)
    return redirect(target_url)
