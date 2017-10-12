from django import forms
from django.contrib import admin
from django.core.urlresolvers import resolve
from nested_inline.admin import (
    NestedTabularInline, NestedStackedInline, NestedModelAdmin)
from .models import RuleContext, Rule, Condition, ContextValue


class ConditionInlineForm(forms.ModelForm):
    rule_context = None

    def __init__(self, *args, **kwargs):
        super(ConditionInlineForm, self).__init__(*args, **kwargs)
        self.fields['context_key'].queryset = (
            self.fields['context_key'].queryset.filter(
                implemented=True, rule_context=self.rule_context))


class ConditionInline(NestedTabularInline):
    model = Condition
    form = ConditionInlineForm
    fk_name = 'rule'
    extra = 1

    def get_rule_context_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.args:
            return RuleContext.objects.get(pk=resolved.args[0])
        return None

    def get_formset(self, request, obj=None, **kwargs):
        parent = self.get_rule_context_from_request(request)
        self.form.rule_context = parent
        return super(ConditionInline, self).get_formset(request, obj, **kwargs)


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
