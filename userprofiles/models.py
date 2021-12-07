from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django_countries.fields import CountryField


# TERMS & CONDITIONS

class TermUser(models.Model):
    agree = models.BooleanField()

    def __str__(self):
        return str(self.agree)


# DROPDOWN LISTS

class Industry(models.Model):
    industry_name = models.CharField(max_length=100, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'Industries'

    def __str__(self):
        return str(self.industry_name)


class Profession(models.Model):
    profession_name = models.CharField(max_length=100, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'Profession'

    def __str__(self):
        return str(self.profession_name)


class Business(models.Model):
    business_name = models.CharField(max_length=200, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return str(self.business_name)


class Employment(models.Model):
    employment_name = models.CharField(max_length=200, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'Employment'

    def __str__(self):
        return str(self.employment_name)


class Status(models.Model):
    status_name = models.CharField(max_length=200, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'Status'

    def __str__(self):
        return str(self.status_name)


MEMBERSHIP_CHOICES = (
    ('Premium', 'pre'),
    ('Free', 'free')
)


class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES, default='Free',
        max_length=30
      )
    description = models.TextField(default='')
    description1 = models.TextField(default='')
    description2 = models.TextField(default='')
    description3 = models.TextField(default='')
    description4 = models.TextField(default='')
    price = models.IntegerField(default=15)
    stripe_price_id = models.CharField(
        default='', max_length=50)

    def __str__(self):
        return str(self.membership_type)


# USERPROFILES

class Userprofile(models.Model):

    # Personal information
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='profileavatars', default='profileavatar.png')
    picture = models.ImageField(
        upload_to='images', default='profileavatar.png')
    first_name = models.CharField(
        max_length=254, blank=False, null=True)
    last_name = models.CharField(
        max_length=254, blank=False, null=True)
    membership = models.ForeignKey(
        Membership, related_name='usermembership', on_delete=models.SET_NULL, null=True)  # noqa: E501
    stripe_customer_id = models.CharField(max_length=50, default='')
    email = models.EmailField(
        max_length=100, null=False, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=False)
    country = CountryField(blank_label='Country', null=True, blank=False)

    # Work Information
    title = models.CharField(
        max_length=254, blank=True, default=None, null=True)
    company_name = models.CharField(
        max_length=254, blank=True, null=True)
    company_number_vat = models.CharField(
        max_length=254, blank=True, default=None, null=True)
    industry = models.ForeignKey(
        Industry, null=True, on_delete=models.SET_NULL, blank=True, default=None)  # noqa: E501
    profession = models.ForeignKey(
        Profession, null=True, on_delete=models.SET_NULL, blank=True, default=None)  # noqa: E501
    description = models.TextField(max_length=250, null=True, verbose_name="Description")  # noqa: E501
    status = models.ForeignKey(
        Status, null=True, on_delete=models.SET_NULL, blank=True, default=None)

    # Matching Preference
    business = models.ForeignKey(
        Business, null=True, on_delete=models.SET_NULL, blank=True, default=None)  # noqa: E501
    employment = models.ForeignKey(
        Employment, null=True, on_delete=models.SET_NULL, blank=True, default=None)  # noqa: E501
    locations = CountryField(blank_label='Locations', null=True, blank=False)

    # Other
    following = models.ManyToManyField(
        User, related_name='following', blank=True)
    updated = models.DateTimeField(auto_now=True, blank=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=True)

    def __str__(self):
        # pylint: disable=maybe-no-member
        return str(self.username)

    @property
    def get_full_name(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
