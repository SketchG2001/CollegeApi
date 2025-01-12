from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, null=True, blank=True)


class States(models.Model):
    stateChoice = [
        ('12', 'Arunachal Pradesh'),
        ('02', 'Himachal Pradesh'),
        ('23', 'Madhya Pradesh'),
        ('27', 'Maharashtra'),
        ('34', 'Puducherry'),
        ('09', 'Uttar Pradesh'),
        ('22', 'Chhattisgarh'),
        ('20', 'Jharkhand'),
        ('17', 'Meghalaya'),
        ('03', 'Punjab'),
        ('16', 'Tripura'),
        ('10', 'Bihar'),
        ('07', 'Delhi'),
        ('32', 'Kerala'),
        ('11', 'Sikkim'),
        ('38', 'The Dadra And Nagar Haveli And Daman And Diu'),
        ('05', 'Uttarakhand'),
        ('35', 'Andaman And Nicobar Islands'),
        ('28', 'Andhra Pradesh'),
        ('18', 'Assam'),
        ('04', 'Chandigarh'),
        ('06', 'Haryana'),
        ('01', 'Jammu And Kashmir'),
        ('37', 'Ladakh'),
        ('15', 'Mizoram'),
        ('21', 'Odisha'),
        ('36', 'Telangana'),
        ('30', 'Goa'),
        ('24', 'Gujarat'),
        ('29', 'Karnataka'),
        ('31', 'Lakshadweep'),
        ('14', 'Manipur'),
        ('13', 'Nagaland'),
        ('08', 'Rajasthan'),
        ('33', 'Tamil Nadu'),
        ('19', 'West Bengal'),
    ]
    state = models.CharField(max_length=11, unique=True, null=True, blank=True, choices=stateChoice)
