from django.db import models
from django.contrib.auth import get_user_model

# At the beginning there is only one default User model.
# But in time you could create your own custom User model.

# Only one model will be active at time. There can also be situation
# where you use i.e your custom model, but for some reason it couldn't 
# be found or whatsoever so only the default one is accessable. 

# To make sure that we will always have some user model that we can use 
# (and thus prevent error of lacking user model), we should use reference
# to current active user model by using the code line below.
User = get_user_model()

class Profile(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user     = models.IntegerField()
    bio         = models.TextField(blank=True, null=True)
    profileimg  = models.ImageField(upload_to='profile_images', 
                                    default='blank-profile-picture.png')
    location    = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.get_username()