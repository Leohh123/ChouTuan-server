from datetime import datetime
from django.db import models


class Delivery(models.Model):
    deposit_username = models.TextField()
    pickup_username = models.TextField()
    device_id = models.TextField()
    cabinet_no = models.IntegerField()
    state = models.IntegerField(default=0)
    moment = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{{id={self.id}, deposit_username={self.deposit_username}, pickup_username={self.pickup_username}, device_id={self.device_id}, cabinet_no={self.cabinet_no}, state={self.state}, moment={self.moment}}}"
