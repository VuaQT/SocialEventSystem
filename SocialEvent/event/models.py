from django.db import models
from rest_framework.exceptions import ValidationError


class Admin(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    email = models.CharField(max_length=100, db_index=True)
    password = models.CharField(max_length=50)
    date_created = models.DateField()
    def __str__(self):
        return str(self.id) + " " + self.email


class Visitor(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    username = models.CharField(max_length=50, db_index=True)
    password = models.CharField(max_length=50)
    date_created = models.DateField()
    def __str__(self):
        return str(self.id) + " " + self.username


class Category(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.id) + " " + self.name


class EventGeneral(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=300)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField()
    number_like = models.IntegerField(auto_created=0)
    c_id = models.ForeignKey(Category, db_index=True, on_delete=models.CASCADE)
    date_created = models.DateField()
    def clean(self):
        if(self.start_date > self.end_date):
            raise ValidationError('Start date is after end date')
    def __str__(self):
        return str(self.id) + " " + self.title


class EventContent(models.Model):
    id = models.OneToOneField(
        EventGeneral, on_delete=models.CASCADE, primary_key=True, db_index=True)
    description = models.TextField() # index ?
    def __str__(self):
        return str(self.id) + " " + self.description


class Photo(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    event_id = models.ForeignKey(EventGeneral, related_name='photopaths', db_index=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=500)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.path)


class Participate(models.Model):
    visitor_id = models.ForeignKey(Visitor, db_index=True, on_delete=models.CASCADE)
    event_id = models.ForeignKey(EventGeneral, db_index=True, on_delete=models.CASCADE)
    date_participated = models.DateField()

    class Meta:
        unique_together = (('visitor_id', 'event_id'),)
        indexes = [
            models.Index(fields=['visitor_id', 'event_id']),
        ]


class Like(models.Model):
    visitor_id = models.ForeignKey(Visitor, db_index=True, on_delete=models.CASCADE)
    event_id = models.ForeignKey(EventGeneral, db_index=True, on_delete=models.CASCADE)
    date_liked = models.DateField()

    class Meta:
        unique_together = (('visitor_id', 'event_id'),)
        indexes = [
            models.Index(fields=['visitor_id', 'event_id']),
        ]


class Comment(models.Model):
    visitor_id = models.ForeignKey(Visitor, db_index=True, on_delete=models.CASCADE)
    event_id = models.ForeignKey(EventGeneral, db_index=True, on_delete=models.CASCADE)
    content = models.TextField()
    date_commented = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['visitor_id', 'event_id']),
        ]

