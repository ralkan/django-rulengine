from django.db import models
from rulengine.core import DataType, ConditionOperator, RuleOperator


class RuleContext(models.Model):
    code = models.CharField(max_length=255)

    def __unicode__(self):
        return self.code


class ContextValue(models.Model):
    DATASTRUCTURE_CHOICES = (
        (DataType.STRING, 'String'),
        (DataType.INTEGER, 'Integer'),
        (DataType.FLOAT, 'Float'),
        (DataType.DATE, 'Date'),
    )
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255, choices=DATASTRUCTURE_CHOICES)

    rule_context = models.ForeignKey(
        'djrulengine.RuleContext', related_name='context_values',
        null=True, blank=True)
    implemented = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s (%s)' % (
            self.name, dict(self.DATASTRUCTURE_CHOICES)[self.data_type])


class Rule(models.Model):
    RULE_OPERATOR_CHOICES = (
        (RuleOperator.AND, 'And'),
        (RuleOperator.OR, 'Or'),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    rule_context = models.ForeignKey(
        'djrulengine.RuleContext', related_name='rules')
    operator = models.CharField(max_length=255,
                                choices=RULE_OPERATOR_CHOICES,
                                default=RULE_OPERATOR_CHOICES[0][0])

    def __unicode__(self):
        return '%s' % (self.name if self.name else 'Rule')


class Condition(models.Model):
    CONDITION_OPERATOR_CHOICES = (
        (ConditionOperator.EQUAL, 'Equal'),
        (ConditionOperator.NOT_EQUAL, 'Not Equal'),
        (ConditionOperator.LESS, 'Less Than'),
        (ConditionOperator.GREATER, 'Greater Than'),
        (ConditionOperator.LESS_EQUAL, 'Less Than or Equal'),
        (ConditionOperator.GREATER_EQUAL, 'Greater Than or Equal'),
        (ConditionOperator.CONTAINS, 'String Contains'),
        (ConditionOperator.IN, 'In'),
    )
    context_key = models.ForeignKey(
        'djrulengine.ContextValue', related_name='conditions')
    operator = models.CharField(max_length=255,
                                choices=CONDITION_OPERATOR_CHOICES)
    value = models.CharField(max_length=255)
    rule = models.ForeignKey('djrulengine.Rule', related_name='conditions')

    def __unicode__(self):
        return '%s %s %s' % (self.context_key.name, self.operator, self.value)
