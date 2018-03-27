from rulengine.core import Rule, Condition
from rulengine import execute as _execute

from .models import Rule as RuleModel, ContextValue


class RuleManager(object):
    code = None
    context = None

    def __init__(self, *args, **kwargs):
        if not self.code:
            raise ValueError('Please specify self.code')

        self.context = self.initialize_context(*args, **kwargs)
        if not isinstance(self.context, dict):
            raise ValueError('self.context must return a dict object.')

    def initialize_context(self, *args, **kwargs):
        raise NotImplementedError('You should implement get_context method')

    def update_context_value_flags(self):
        specified_context_values = ContextValue.objects.filter(
            rule_context__code=self.code).values_list('name', 'implemented')

        implemented_context_values = map(
            lambda cv: cv[0],
            filter(
                lambda cv: cv[1] is False and cv[0] in self.context,
                specified_context_values))
        if implemented_context_values:
            ContextValue.objects.filter(
                rule_context__code=self.code,
                name__in=implemented_context_values).update(implemented=True)

        unimplemented_context_values = map(
            lambda cv: cv[0],
            filter(
                lambda cv: cv[1] is True and cv[0] not in self.context,
                specified_context_values))
        if unimplemented_context_values:
            ContextValue.objects.filter(
                rule_context__code=self.code,
                name__in=unimplemented_context_values).update(
                    implemented=False)

    def get_rules(self):
        rule_entries = RuleModel.objects.filter(
            rule_context__code=self.code,
            conditions__isnull=False).prefetch_related(
                'conditions', 'conditions__context_key').all()

        return map(lambda e: Rule(operator=e.operator, conditions=map(
            lambda c: Condition(value=self.context.get(c.context_key.name),
                                operator=c.operator,
                                comparison_value=c.value,
                                data_type=c.context_key.data_type),
            e.conditions.all())), rule_entries)

    def execute(self):
        self.update_context_value_flags()
        return _execute(self.get_rules())
