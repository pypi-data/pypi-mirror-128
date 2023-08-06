# django-relativedeltastore

A Django model field to store
[dateutil.relativedelta.relativedelta](http://dateutil.readthedocs.io/en/stable/relativedelta.html).

The field is a subclass of [JSONField](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#jsonfield)
and simply stores the kwargs of a [relativedelta](http://dateutil.readthedocs.io/en/stable/relativedelta.html) instance.

The field is mainly meant to store [relativedelta](http://dateutil.readthedocs.io/en/stable/relativedelta.html).
The package [django-relativedelta](https://github.com/CodeYellowBV/django-relativedelta) provides better query support
(for relative units since it uses a sql `INTERVAL`).

The basic arguments for relative and absolute units are supported (`year`, `years` … `microseconds`).
Currently not supported are: `weekday`, `leapdays`, `yearday` & `nlyearday`

The package also provides a form field to edit the value of `RelativeDeltaStoreField` with a custom
serialization format (configurable): `1hour +1days -1seconds`
