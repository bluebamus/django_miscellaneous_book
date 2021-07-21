from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class UserLoginLog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=("User"),
        related_name="login_logs",
        blank=True,
        null=True,
    )
    ip_address = models.GenericIPAddressField(verbose_name=("IP Address"))
    user_agent = models.CharField(
        verbose_name=("HTTP User Agent"),
        max_length=300,
    )

    class Meta:
        verbose_name = "user login log"
        verbose_name_plural = "user login logs"
        ordering = ("-created",)

    def __str__(self):
        return "%s %s" % (self.user, self.ip_address)
