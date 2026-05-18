from django.contrib import admin
from .models import Tender, Requirement


class RequirementInline(admin.TabularInline):
    model = Requirement
    extra = 0


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'risk_score', 'created_at']
    inlines = [RequirementInline]


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ['tender', 'category', 'status', 'text']
