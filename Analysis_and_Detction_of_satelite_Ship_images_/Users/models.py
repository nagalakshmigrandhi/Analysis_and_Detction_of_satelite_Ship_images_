from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, locality, state, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        if not mobile:
            raise ValueError('Users must have a mobile number')
        if not locality:
            raise ValueError('Users must have a locality')
        if not state:
            raise ValueError('Users must have a state')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile,
            locality=locality,
            state=state,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, locality, state, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile,
            locality=locality,
            state=state,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=100)
    mobile = models.CharField(_('mobile number'), max_length=15)
    locality = models.CharField(_('locality'), max_length=100)
    state = models.CharField(_('state'), max_length=50)
    status = models.CharField(_('status'), max_length=20, default='activated')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile', 'locality', 'state']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0] if self.name else self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_image = models.ImageField(upload_to='history/inputs/')
    output_image = models.ImageField(upload_to='media/history/outputs/')
    num_ships = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Prediction History'
        verbose_name_plural = 'Prediction History'
        ordering = ['-created_at']

    def __str__(self):
        return f"Prediction {self.id} - {self.user.email}"
