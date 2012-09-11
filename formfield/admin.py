from django.contrib.admin import ModelAdmin
from .fields import JSONField
from .widgets import AdminJSONFieldWidget


class JSONFieldAdminMixin(object):
    """Register JSONField with JSON Field Widget"""
    formfield_overrides = {
        JSONField: {'widget': AdminJSONFieldWidget}
    }


class JSONFieldModelAdmin(JSONFieldAdminMixin, ModelAdmin):
    """Convenience premix."""
    pass
