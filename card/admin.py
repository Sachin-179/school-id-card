from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.urls import reverse

from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'dob', 'father_name', 'mother_name', 'contact_no', 'standard', 'address', 'display_photo_thumbnail', 'admission',
        'session', 'print_id_card'
    )

    def print_id_card(self, obj):
        url = reverse('generate_id_cards', args=[obj.pk])
        return format_html('<a class="button" href="{}">Print</a>', url)

    print_id_card.short_description = 'Print ID Card'
    print_id_card.allow_tags = True

    def display_photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.photo.url)
        return 'No Photo'

    display_photo_thumbnail.short_description = 'Photo Thumbnail'


admin.site.register(Student, StudentAdmin)
