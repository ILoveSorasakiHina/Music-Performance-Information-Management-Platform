from django.db import models

# 主辦/協辦Model
class Organizer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# 地點Model
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'address')

    def __str__(self):
        return self.name

# 活動Model
class Event(models.Model):
    version = models.CharField(max_length=4)
    uid = models.CharField(max_length=50, unique=True, primary_key=True,db_index=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=3)
    description = models.TextField()
    image_url = models.URLField(max_length=200)
    web_sale = models.URLField(max_length=200, null=True, blank=True)
    source_web_promote = models.URLField(max_length=200, null=True, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    edit_modify_date = models.DateTimeField(null=True)
    source_web_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    hit_rate = models.IntegerField(default=0,db_index=True)
    show_unit = models.CharField(max_length=300)
    discount_info = models.TextField(null=True, blank=True)
    description_filter_html = models.TextField(null=True, blank=True)
    master_unit = models.ManyToManyField(Organizer, related_name='master_events')
    sub_unit = models.ManyToManyField(Organizer, related_name='sub_events')
    support_unit = models.ManyToManyField(Organizer, related_name='support_events')
    other_unit = models.ManyToManyField(Organizer, related_name='other_events')

    def __str__(self):
        return self.title

# 表演資訊Model
class ShowInfo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE , related_name = 'showinfos')
    time = models.DateField()
    end_time = models.DateTimeField()
    on_sale = models.BooleanField()
    price = models.CharField(max_length=200, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event} at {self.location} on {self.time}"
