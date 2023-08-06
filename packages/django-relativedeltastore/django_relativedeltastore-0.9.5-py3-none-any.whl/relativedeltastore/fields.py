from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta

from . import extract_relativedelta_args, forms


try:
    # there is no difference in the (postgres) schema, so we can easily swap between the two
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields.jsonb import JSONField


class RelativeDeltaStoreField(JSONField):
    description = _('A dateutil.relativedelta.relativedelta object')

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.RelativeDeltaStoreField,
            **kwargs,
        })

    def from_db_value(self, value, expression, connection):
        if hasattr(super(), 'from_db_value'):  # support new JSONField (django 3.1+)
            value = super().from_db_value(value, expression, connection)
        if value is None:
            return value
        return relativedelta(**value)

    def get_prep_value(self, value):
        if isinstance(value, relativedelta):
            value = extract_relativedelta_args(value)
        return super().get_prep_value(value)

    def validate(self, value, model_instance):
        if isinstance(value, relativedelta):
            value = extract_relativedelta_args(value)
        super().validate(value, model_instance)
