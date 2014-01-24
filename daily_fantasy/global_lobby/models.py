from django.db import models

class Contest(models.Model):

    scrape_id = models.IntegerField()
    site = models.CharField(max_length= 30)
    url = models.CharField(max_length = 300)
    title = models.CharField(max_length= 300)
    sport = models.CharField(max_length=10)
    size = models.IntegerField()
    entries = models.IntegerField()
    buyin = models.DecimalField(max_digits= 15, decimal_places=2)
    payout = models.DecimalField(max_digits= 15, decimal_places=2)
    start = models.DateTimeField()

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return self.__repr__()