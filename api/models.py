from django.db import models


# Creation of Members Class.
# NOTE - Phase 2 option is to change phone_number to support multiple phone number formats, including
# potentially international using - https://github.com/stefanfoulis/django-phonenumber-field

# Need to add validator for Phone number for purely numeric field


class Member(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    id = models.BigIntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    client_member_id = models.BigIntegerField()
    account_id = models.BigIntegerField()

    class Meta:
        ordering = ['created']


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name


