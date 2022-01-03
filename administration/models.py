from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Clients(models.Model):
    first_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    phone = PhoneNumberField(unique=True, null=False, blank=False)
    email = models.EmailField(max_length=65, blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'name']),
        ]


class Dogs(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(Clients, on_delete=models.CASCADE)
    transponder = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Parks(models.Model):
    name = models.CharField(max_length=2, unique=True)
    availability = models.BooleanField()

    def __str__(self):
        return self.name


class Reservations(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    park = models.ForeignKey(Parks, on_delete=models.CASCADE)
    price = models.SmallIntegerField(blank=False)
    dog_1 = models.ForeignKey(Dogs, on_delete=models.CASCADE, related_name='dog_1_relation')
    dog_1_arrival = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
    dog_1_departure = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
    dog_2 = models.ForeignKey(Dogs, on_delete=models.CASCADE, blank=True, null=True, related_name='dog_2_relation')
    dog_2_arrival = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    dog_2_departure = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    dog_3 = models.ForeignKey(Dogs, on_delete=models.CASCADE, blank=True, null=True, related_name='dog_3_relation')
    dog_3_arrival = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    dog_3_departure = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    dog_4 = models.ForeignKey(Dogs, on_delete=models.CASCADE, blank=True, null=True, related_name='dog_4_relation')
    dog_4_arrival = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    dog_4_departure = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    dog_5 = models.ForeignKey(Dogs, on_delete=models.CASCADE, blank=True, null=True, related_name='dog_5_relation')
    dog_5_arrival = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    dog_5_departure = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        indexes = [
            models.Index(fields=['dog_1_arrival', 'dog_1_departure',
                                 'dog_2_arrival', 'dog_2_departure',
                                 'dog_3_arrival', 'dog_3_departure',
                                 'dog_4_arrival', 'dog_4_departure',
                                 'dog_5_arrival', 'dog_5_departure']),
        ]
