# -*- encoding: utf-8 -*-

from django.db.models.fields import Field, IntegerField
from django.core import checks, exceptions
from django.utils.translation import ugettext_lazy as _


class AutoIncreField(Field):
    description = _("Integer")

    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value must be an integer."),
    }

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super(AutoIncreField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(AutoIncreField, self).check(**kwargs)
        # 每张表只能设置一个字段为自增长字段，这个字段可以是主键，也可以不是主键，如果不是主键，则必须设置为一种“键(key)”
        # (primary key)也是键(key)的一种，key还包括外键(foreign key)、唯一键(unique key)
        errors.extend(self._check_key())
        return errors

    def _check_key(self):
        if not self.unique:
            return [
                checks.Error(
                    'AutoIncreFields must set key(unique=True).',
                    obj=self,
                    id='fields.E100',
                ),
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super(AutoIncreField, self).deconstruct()
        del kwargs['blank']
        kwargs['unique'] = True
        return name, path, args, kwargs

    def get_internal_type(self):
        return "AutoIncreField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def db_type(self, connection):
        return 'bigint AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return IntegerField().db_type(connection=connection)

    def validate(self, value, model_instance):
        pass

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
            value = connection.ops.validate_autopk_value(value)
        return value

    def get_prep_value(self, value):
        value = super(AutoIncreField, self).get_prep_value(value)
        if value is None:
            return None
        return int(value)

    def contribute_to_class(self, cls, name, **kwargs):
        assert not cls._meta.auto_field, "A model can't have more than one AutoIncreField."
        super(AutoIncreField, self).contribute_to_class(cls, name, **kwargs)
        cls._meta.auto_field = self

    def formfield(self, **kwargs):
        return None


class AutoIncreFieldFixMinxin(object):
    def save(self, *args, **kwargs):
        super(AutoIncreFieldFixMinxin, self).save(*args, **kwargs)
        auto_field = self.meta.auto_field.name
        new_obj = self.__class__.objects.get(pk=self.pk)
        setattr(self, auto_field, int(getattr(new_obj, auto_field)))