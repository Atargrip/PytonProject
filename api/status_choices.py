from django.db import models


# [‘started’, ‘ended’, ‘in process’, ‘awaiting’, ‘canceled’]
class StatusChoice(models.TextChoices):
    STARTED = 'начето'
    ENDED = 'окончено'
    IN_PROCES = 'в процессе'
    AWAITING = 'ожидается'
    CANCELED = 'отменено'