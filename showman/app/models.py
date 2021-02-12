from django.db import models

# Create your models here.

class Timestamp(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

class Cities(Timestamp):
    c_name = models.CharField(max_length=30)
    c_url = models.URLField()
    c_file = models.FileField(upload_to='Citywise-data/',default='.')
    class Meta:
        ordering = ('c_name', )

    def __str__(self):
        return self.c_name

class Events(Timestamp):
    city = models.ManyToManyField('Cities')
    e_id = models.CharField(max_length=20)
    title = models.CharField(max_length=40)
    e_url = models.URLField()
    img_url = models.URLField()
    genre = models.CharField(max_length=50)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title
