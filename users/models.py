from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, gender, password=None):
        """
        Creates and saves a User with the given email, firstname, lastname, gender and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, gender, password):
        """
        Creates and saves a superUser with the given email, firstname, lastname, gender and password.
        """
        user = self.create_user(email,
        	password=password,
            firstname=firstname,
            lastname=lastname,
            gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
	email = models.EmailField(max_length=40, unique=True)

	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30)
	gender = models.CharField(max_length=1)
	facebook_user_id = models.CharField(max_length=30, null=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)


	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['firstname', 'lastname', 'gender',]

	def get_full_name(self):
        # The user is identified by their email address
		return self.email
	
	def get_short_name(self):
        # The user is identified by their email address
		return self.email

    # On Python 3: def __str__(self):
	def __unicode__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
		return self.is_admin

