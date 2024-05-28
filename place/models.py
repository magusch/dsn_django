from django.db import models


class Place(models.Model):
    place_name = models.CharField(max_length=500)
    place_address = models.CharField(max_length=2000, blank=True,)
    place_url = models.CharField(max_length=500, blank=True,)
    url_to_address = models.CharField(max_length=500, blank=True,)
    place_metro = models.CharField(max_length=500, blank=True,)
    place_city = models.CharField(max_length=500, default='SPb', blank=True,)

    def markdown_address(self):
        markdown_address = ''
        if self.url_to_address != '':
            markdown_address += f"[{self.place_name}, {self.place_address}]({self.url_to_address})"
        else:
            markdown_address += f"{self.place_name}, {self.place_address}"

        if self.place_metro != '':
            markdown_address += f", м.{self.place_metro}"

        return markdown_address

    def __str__(self):
        return f"{self.place_name}, {self.place_address}"


class PlaceKeyword(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    place_keyword = models.CharField(max_length=200)

    def __str__(self):
        return (f"{self.place_keyword}, {self.place.place_address}")


class TestEventPlace(models.Model):
    event_name = models.CharField(max_length=200)
    event_address = models.CharField(max_length=200)
    place_keyword = models.ForeignKey(PlaceKeyword, on_delete=models.CASCADE)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return models.CharField(queryset=PlaceKeyword.objects.all())
        #return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):
        obj.event_address = obj.event_name
        super().save_model(request, obj, form, change)

    def __str__(self):
        return (self.event_name)

    def save_formset(self, request, form, formset, change):
        print(self.event_name)
