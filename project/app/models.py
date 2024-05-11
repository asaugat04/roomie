from django.db import models
from django.contrib.auth.models import User




class Room(models.Model):
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    roommate_max_capacity = models.IntegerField()
    listed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='room_image', blank=True, null=True)


    def __str__(self):
        return self.location
    



class Profile(models.Model):
    food_preference_choices = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    user_type_choices = [
        ('Single','Single'),
        ('Couple','Couple'),
        ('Family','Family'),
    ]
    user_type_2_choices = [
        ('Student','Student'),
        ('Employee','Employee'),
        ('Others','Others'),
    ]


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    temp_address = models.CharField(max_length=100)
    perm_address = models.CharField(max_length=100)
    phone_no = models.IntegerField()
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    food_preference = models.CharField(max_length=10, choices=food_preference_choices)
    gender = models.CharField(max_length=10, choices=gender_choices)
    user_type = models.CharField(max_length=10, choices=user_type_choices)
    user_type_2 = models.CharField(max_length=10, choices=user_type_2_choices)
    interests = models.TextField()


    lives_in = models.ForeignKey(Room, on_delete=models.DO_NOTHING, null=True, blank=True)




    def get_full_name(self):
        return self.user.first_name + " " + self.user.last_name
    def __str__(self):
        return self.user.username




class RoomRequest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.profile.user.username + ' - ' + self.room.location