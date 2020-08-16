from django.db import models

# Create your models here.

class Search(models.Model):
    search = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now = True)

    #When a search object will call it will return search string
    def __str__(self):
        return '{}'.format(self.search)

    #Database table name change
    class Meta:
        verbose_name_plural = 'Searches'