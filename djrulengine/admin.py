from django import forms
from django.contrib import admin
from nested_inline.admin import (
    NestedTabularInline, NestedStackedInline, NestedModelAdmin)
from .models import RuleContext, Rule, Condition, ContextValue


class ConditionInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConditionInlineForm, self).__init__(*args, **kwargs)
        self.fields['context_key'].queryset = (
            self.fields['context_key'].queryset.filter(implemented=True))


class ConditionInline(NestedTabularInline):
    model = Condition
    form = ConditionInlineForm
    fk_name = 'rule'
    extra = 1


class RuleInline(NestedStackedInline):
    model = Rule
    fk_name = 'rule_context'
    extra = 1
    inlines = [ConditionInline]


class ContextValueInline(NestedTabularInline):
    model = ContextValue
    readonly_fields = ('implemented',)
    extra = 1


class RuleContextAdmin(NestedModelAdmin):
    list_display = ('code',)
    inlines = [RuleInline, ContextValueInline]
    ordering = ('id',)


admin.site.register(RuleContext, RuleContextAdmin)
