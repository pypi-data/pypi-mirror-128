from django import forms
from django.db import transaction

from nautobot.dcim.models import Device
from nautobot.utilities.forms import DynamicModelChoiceField


class MoveForm(forms.Form):
    to = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        display_field="display_name",
        query_params={
            "status": "planned",
        },
        required=True,
    )
    delete_existing = forms.BooleanField(
        label="Remove connections",
        help_text="Should existing connections on the moved device be deleted?",
        required=False,
    )

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        self.component_types = [
            "consoleports",
            "consoleserverports",
            "powerports",
            "poweroutlets",
            "interfaces",
            "rearports",
            "frontports",
            "devicebays",
        ]
        self.connectable_component_types = [
            "consoleports",
            "consoleserverports",
            "powerports",
            "poweroutlets",
            "interfaces",
            "rearports",
            "frontports",
        ]

        return super().__init__(*args, **kwargs)

    def clean_to(self):
        other = self.cleaned_data["to"]

        for component_type in self.component_types:
            this_prop = getattr(self.instance, component_type)
            other_prop = getattr(other, component_type)

            if this_prop.count() != other_prop.count():
                raise forms.ValidationError(
                    f"The devices are incompatible: the number of {component_type} doesn’t match."
                )

            for component in this_prop.all():
                if not other_prop.filter(name=component.name).exists():
                    raise forms.ValidationError(
                        f"The devices are incompatible: the {component_type} named {component.name} doesn’t exist on the device {other.name}."
                    )

        return other

    def clean_delete_existing(self):
        delete_existing = self.cleaned_data.get("delete_existing", False)

        if delete_existing:
            return delete_existing

        for component_type in self.connectable_component_types:
            prop = getattr(self.instance, component_type)
            if prop.filter(cable__isnull=False).exists():
                raise forms.ValidationError(
                    f"The device to move still has connected {component_type}."
                )
        if self.instance.devicebays.filter(installed_device__isnull=False).exists():
            raise forms.ValidationError(
                "The device to move still has connected device bays."
            )

        return delete_existing

    def save(self):
        other = self.cleaned_data["to"]
        delete_existing = self.cleaned_data.get("delete_existing", False)

        with transaction.atomic():
            for component_type in self.connectable_component_types:
                for component in getattr(other, component_type).all():
                    this_component = getattr(self.instance, component_type).get(
                        name=component.name
                    )
                    if this_component.cable and delete_existing:
                        this_component.cable.delete()
                    if not component.cable_id:
                        continue
                    component.cable.delete()
                    if component.cable.termination_a == component:
                        component.cable.termination_a = this_component
                    if component.cable.termination_b == component:
                        component.cable.termination_b = this_component
                    component.cable.pk = None
                    component.cable.save()

            self.instance.devicebays.all().delete()
            other.devicebays.all().update(device=self.instance)

            self.instance.site = other.site
            self.instance.rack = other.rack
            self.instance.position = other.position
            self.instance.face = other.face
            other.delete()
            self.instance.save()

        return self.instance
