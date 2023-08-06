from collections import defaultdict
from datetime import date, timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from i18nfield.strings import LazyI18nString
from pretix.base.settings import settings_hierarkey
from pretix.control.signals import nav_event_settings
from pretix.presale.signals import (
    question_form_fields_overrides,
)


@receiver(nav_event_settings, dispatch_uid="dob_validation_nav")
def navbar_info(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(
            request.organizer, request.event, "can_change_event_settings", request=request
    ):
        return []
    return [
        {
            "label": _("DOB validation"),
            "url": reverse(
                "plugins:pretix_dob_validation:settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_dob_validation",
        }
    ]


@receiver(
    question_form_fields_overrides, dispatch_uid="dob_validations_fields_overrides"
)
def form_fields_overrides(sender, position, request, **kwargs):
    o = defaultdict(lambda: {"validators": []})
    for k, v in sender.settings.dob_validation_config.items():
        if k.endswith(":message") or not v:
            continue

        today = (position.subevent or sender).date_from.astimezone(sender.timezone).date()
        if k.endswith(":min"):
            fname = k.split(":")[0]
            max_value = date(today.year - int(v), today.month, today.day - 1 if today.day == 29 and today.month == 2 else today.day)
            o[fname]["validators"].append(
                MaxValueValidator(
                    limit_value=max_value,
                    message=str(
                        LazyI18nString(
                            sender.settings.dob_validation_config.get(
                                f"{fname}:message",
                                _("You are not permitted to proceed with this age."),
                            )
                        )
                    ),
                )
            )
        if k.endswith(":max"):
            fname = k.split(":")[0]
            min_value = date(today.year - int(v), today.month, today.day - 1 if today.day == 29 and today.month == 2 else today.day) - timedelta(days=1)
            o[fname]["validators"].append(
                MinValueValidator(
                    limit_value=min_value,
                    message=str(
                        LazyI18nString(
                            sender.settings.dob_validation_config.get(
                                f"{fname}:message",
                                _("You are not permitted to proceed with this age."),
                            )
                        )
                    ),
                )
            )
    return o


settings_hierarkey.add_default("dob_validation_config", "{}", dict)
