from django.db import models
from django.urls import reverse,NoReverseMatch
from django.core.exceptions import ValidationError

# Create your models here.
class Websites(models.Model):

    name = models.CharField(max_length=20)

    description = models.TextField()

    url = models.URLField(
        blank=True,
        default=""
    )

    route_name = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="站内路由,形如guestbook:entry_list"
    )

    search_aliases = models.JSONField(
        default=list,
        blank=True,
        help_text='字符串数组，形如["monitor","监控"]'
    )

    is_active = models.BooleanField(default=True)

    show_in_random = models.BooleanField(default=True)

    search_enabled = models.BooleanField(default=False)

    search_order = models.PositiveIntegerField(
        default=100,
        help_text="搜索分数一致时数值小的优先"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

        verbose_name = "网址"
        verbose_name_plural = "网址"

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(route_name="") & ~models.Q(url="")
                ) | (
                    ~models.Q(route_name="") & models.Q(url="")
                ),
                name="index_websites_one_target",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(search_enabled=False) | ~models.Q(route_name="")
                ),
                name="index_websites_search_route",
            ),
        ]

    def __str__(self):
        target = self.route_name or self.url
        return f"{self.name}: {target}"

    def get_target_url(self):
        if self.route_name:
            return reverse(self.route_name)

        return self.url

    def clean(self):
        super().clean()

        self.route_name = (self.route_name or "").strip()

        aliases = self.search_aliases
        if aliases is None:
            aliases = []
        if not isinstance(aliases, list):
            raise ValidationError({
                "search_aliases": "别名必须是字符串数组，例如 [\"留言板\", \"guestbook\"]",
            })

        cleaned_aliases = []
        for item in aliases:
            if not isinstance(item, str):
                raise ValidationError({
                    "search_aliases": f"别名 {item!r} 不是字符串",
                })
            item = item.strip()
            if not item:
                raise ValidationError({
                    "search_aliases": "别名不能是空白字符串",
                })
            cleaned_aliases.append(item)
        self.search_aliases = cleaned_aliases

        if bool(self.url) == bool(self.route_name):
            msg = ("站内路由和外部链接只能填一个"
                   if self.url else "站内路由和外部链接必须填一个")
            raise ValidationError({"url": msg, "route_name": msg})

        if self.route_name:
            try:
                reverse(self.route_name)
            except NoReverseMatch:
                raise ValidationError({
                    "route_name": f"路由 “{self.route_name}” 不存在，或需要参数无法直接跳转",
                })

        if self.search_enabled and not self.route_name:
            raise ValidationError({
                "search_enabled": "只有填写了站内路由的记录才能开启搜索",
            })