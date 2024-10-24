from django.db import models
from django.utils.timezone import localtime



class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


    def get_duration(self):
        time_leaved_at = localtime(self.leaved_at)
        time_entered_at = localtime(self.entered_at)
        return (time_leaved_at - time_entered_at).total_seconds()

    def format_duration(self, duration):
        hours, minutes = int(duration // 3600), int((duration % 3600 // 60))
        return f"{hours} ч. {minutes} м."

    def is_visit_long(self, minutes=60):
        duration = self.get_duration()
        return duration // 60 > minutes


