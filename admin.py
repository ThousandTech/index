from django.contrib import admin
from .models import Websites

# Register your models here.
@admin.register(Websites)
class WebsitesAdmin(admin.ModelAdmin):

    list_display = ["name","url","created_at"]
    # 列表页显示哪些列的内容

    search_fields = ["name","url"]
    # 搜索框可搜索哪些内容

    list_filter = ["created_at"]
    # 右侧筛选器可用筛选项

    ordering = ["-created_at"]