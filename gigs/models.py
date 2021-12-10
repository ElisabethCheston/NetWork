from django.db import models
# from django.contrib.auth.models import User
from userprofiles.models import Userprofile, Industry, Profession, Membership  # noqa: E501
from django.urls import reverse
from django_countries.fields import CountryField


# GIG

class Gig(models.Model):
    title = models.CharField(max_length=50, blank=False)
    picture = models.ImageField(upload_to='images', blank=True)
    industry = models.ForeignKey(
        Industry, null=True, on_delete=models.SET_NULL, blank=True, default=None)  # noqa: E501
    profession = models.ForeignKey(
        Profession, null=True, on_delete=models.SET_NULL, blank=True, default=None)  # noqa: E501
    city = models.CharField(max_length=50, blank=False)
    country = CountryField(blank_label='Country', null=True, blank=False)
    position = models.TextField(max_length=250)
    overview = models.TextField(max_length=250)
    requirements = models.TextField(max_length=250)
    contact = models.TextField(max_length=250)
    author = models.ForeignKey(
        Userprofile, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    allowed_membership = models.ManyToManyField(Membership)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('gig_detail', kwargs={'pk': self.pk})

    def my_gigs(self):
        return self.gig_set.all()

    class Meta:
        ordering = ('-created',)

    def get_liked(self):
        # pylint: disable=maybe-no-member
        return self.liked.all()

    @property
    def like_count(self):
        # pylint: disable=maybe-no-member
        return self.liked.all().count()

    def get_user_liked(self, user):
        pass
