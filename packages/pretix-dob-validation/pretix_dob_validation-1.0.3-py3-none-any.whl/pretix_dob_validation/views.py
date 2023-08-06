import json
import logging
import re
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.generic import FormView
from i18nfield.forms import I18nFormField, I18nTextInput
from i18nfield.strings import LazyI18nString
from i18nfield.utils import I18nJSONEncoder
from pretix.base.models import Event, Question
from pretix.control.views.event import EventSettingsViewMixin

logger = logging.getLogger(__name__)


class DobValidationSettingsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.obj = kwargs.pop("obj")
        super().__init__(*args, **kwargs)

        fields = []
        for q in self.obj.questions.filter(
            type__in=[Question.TYPE_DATE]
        ):
            fields.append((q.identifier, q))

        for identifier, label in fields:
            self.fields[f"{identifier}:min"] = forms.IntegerField(
                label=escape(_('Minimum age for "{field}" ({identifier})').format(field=label, identifier=identifier)),
                required=False,
                min_value=0,
                max_value=199,
            )
            self.fields[f"{identifier}:max"] = forms.IntegerField(
                label=escape(_('Maximum age for "{field}" ({identifier})').format(field=label, identifier=identifier)),
                required=False,
                min_value=0,
                max_value=199,
            )
            self.fields[f"{identifier}:message"] = I18nFormField(
                label=escape(_('Error message for "{field}" ({identifier})').format(field=label, identifier=identifier)),
                required=False,
                locales=self.obj.settings.locales,
                initial=LazyI18nString.from_gettext(
                    gettext_noop("You are not permitted to proceed with this age."),
                ),
                widget=I18nTextInput,
            )


class SettingsView(EventSettingsViewMixin, FormView):
    model = Event
    form_class = DobValidationSettingsForm
    template_name = "pretix_dob_validation/settings.html"
    permission = "can_change_event_settings"

    def get_success_url(self) -> str:
        return reverse(
            "plugins:pretix_dob_validation:settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["obj"] = self.request.event
        kwargs["initial"] = self.request.event.settings.dob_validation_config
        return kwargs

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if form.has_changed():
                self.request.event.settings.dob_validation_config = json.dumps(
                    form.cleaned_data, cls=I18nJSONEncoder
                )
                self.request.event.log_action(
                    "pretix.event.settings",
                    user=self.request.user,
                    data={"dob_validation_config": form.cleaned_data},
                )
            messages.success(self.request, _("Your changes have been saved."))
            return redirect(self.get_success_url())
        else:
            messages.error(
                self.request,
                _("We could not save your changes. See below for details."),
            )
            return self.render_to_response(self.get_context_data(form=form))
