from django.db import models

class Stuff(models.Model):
    Firstname = models.CharField(max_length=255)
    Lastname = models.CharField(max_length=255)
    Position = models.CharField(max_length=255)
    Year = models.CharField(max_length=4)
    Phone = models.CharField(max_length=10)
    Address = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f"{self.Firstname} {self.Lastname} "