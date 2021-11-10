from django.contrib.auth.models import User
from django.db import models
from api.relations import generate_ref_code


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12,blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')

    def __str__(self):
        return f"{self.user.username} = {self.code}"

    def get_recommended_profiles(self):
        qs = Profile.objects.all()
        my_recs = [p for p in qs if p.recommended_by == self.user]
        return my_recs

    def save(self, *args, **kwargs):
        if self.code == '':
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)

    # class Meta:
    #     managed = False  # remove this line
    #     db_table = 'users'
