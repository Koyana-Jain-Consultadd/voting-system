from django.db import models
import os
from django.contrib.auth.hashers import make_password

# Create your models here.
def user_image_path(instance, filename):
    # Split the filename and extension
    name, extension = os.path.splitext(filename)
    # Get the user's email ID
    email_id = instance.email
    # Generate a new filename based on email ID and current timestamp
    new_filename = f"{email_id}{extension}"
    # Return the new filename
    return os.path.join('user', new_filename)

class User(models.Model):
    u_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=64)
    email=models.CharField(max_length=64,unique=True)
    phone=models.CharField(max_length=15)
    dob=models.DateField(null=True, blank=True)
    adhar_num=models.CharField(max_length=12, default=None)
    user_img=models.FileField(upload_to=user_image_path,max_length=250,null=True, blank=True, default=None)
    gender=models.CharField(max_length=15,null=True, blank=True)
    password=models.CharField(max_length=4096)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the password is not already hashed
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
            # Hash the password before saving
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

def party_image_path(instance, filename):
    # Split the filename and extension
    name, extension = os.path.splitext(filename)
    # Get the user's email ID
    party = instance.sym_name
    # Generate a new filename based on email ID and current timestamp
    new_filename = f"{party}{extension}"
    # Return the new filename
    return os.path.join('parties', new_filename)


class Parties(models.Model):
    p_id=models.AutoField(primary_key=True)
    p_name=models.CharField(max_length=100,default=None)
    sym_name=models.CharField(max_length=24, unique=True)
    sym_img=models.FileField(upload_to=party_image_path,max_length=250,null=True, blank=True, default=None)


class Election(models.Model):
    e_id=models.AutoField(primary_key=True)
    e_name=models.CharField(max_length=150, unique=True)
    e_date=models.DateField(null=True, blank=True)


class Candidates(models.Model):
    c_id=models.AutoField(primary_key=True)
    c_name=models.CharField(max_length=100,default=None)
    adhar_num=models.CharField(max_length=12, default=None)
    state=models.CharField(max_length=50, default=None)
    party =models.ForeignKey(Parties, on_delete=models.CASCADE)


class Result(models.Model):
    election=models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate=models.ForeignKey(Candidates, on_delete=models.CASCADE)
    votes=models.IntegerField(default=0, null=True, blank=True)