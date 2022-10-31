import os

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from Maple.settings import base
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    list_display = ('username', 'phone', 'sms_code', 'game_name', 'new_game_image', 'is_valid')
    list_filter = ('provider',)
    search_fields = ('username',)
    ordering = ('date_joined',)
    actions = ['make_valid']
    
    def new_game_image(self, obj):
        if obj.game_image.name:
            img_url = os.path.join(base.MEDIA_URL, obj.game_image.url)
        else:
            img_url = ""
        return mark_safe('<img src="%s" width="150" height="150"/>' % img_url)

    new_game_image.short_description = '遊戲截圖'
    new_game_image.allow_tags = True

    @admin.action(description='驗證通過')
    def make_valid(self, request, queryset):
        result = 0
        for q in queryset:
            if q.phone and q.game_name and q.game_image:
                q.is_valid = True
                q.save()
                result += 1
        # q = queryset.update(is_valid=True)
        self.message_user(request, ngettext(
            '%d story was successfully marked as published.',
            '%d stories were successfully marked as published.',
            result,
        ) % result, messages.SUCCESS)

    # def get_form(self, request, obj=None, **kwargs):
    #     kwargs["fields"] += ['game_name', 'phone']
    #     form = super().get_form(request, obj, **kwargs)
    #     return form
