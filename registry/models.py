from django.db import models
from django.contrib.auth.models import User
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Center(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.city}"

class Beneficiary(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, help_text="A unique identifier for the beneficiary (e.g., AADHAAR, internal ID)")
    name = models.CharField(max_length=255, help_text="Full name of the beneficiary")
    date_of_birth = models.DateField()
    
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.unique_id})"

class Intervention(models.Model):
    INTERVENTION_TYPES = [
        ('counseling', 'Counseling Session'),
        ('therapy', 'Therapy (Group)'),
        ('medical', 'Medical Checkup'),
        ('other', 'Other'),
    ]

    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    date_of_intervention = models.DateTimeField(auto_now_add=True)
    intervention_type = models.CharField(max_length=50, choices=INTERVENTION_TYPES)
    details = models.TextField(help_text="Detailed notes on the session/intervention provided")
    
    staff_member = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Intervention for {self.beneficiary.name} on {self.date_of_intervention.strftime('%Y-%m-%d')}"

class UserProfile(models.Model):
    USER_ROLES = [
        ('center_staff', 'Center Staff'),
        ('state_admin', 'State Admin'),
        ('super_admin', 'Super Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='center_staff')
    
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True, blank=True)

    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"