from django.db import models


class MicrowaveStatus(models.Model):
    On = models.BooleanField(default=False)     # This is not used
    TTL = models.PositiveSmallIntegerField()
    Power = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} {} {}'.format(self.On, self.TTL, self.Power)

    def to_json(self):
        return {
            'id': self.id,
            'On': self.On,
            'TTL': self.TTL,
            'Power': self.Power,
        }
