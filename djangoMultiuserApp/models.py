from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserAccountManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email or len(email) <=0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")
        user = self.model(
            email=self.normalize_email(email),
            )
        # set the encrypted password using setter method of model instance
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password):
        """Create and save a new superuser with given details"""
        user = self.create_user(
            email = self.normalize_email(email),
            password=password
            )
        user.is_admin = True  ## added this line to make it admin by default
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class UserAccount(AbstractBaseUser):
    class Types(models.TextChoices):
        
        STUDENT='ST', 'Student'
        TEACHER ='TE','Teacher'
    role = models.CharField(max_length=8, choices=Types.choices, default=Types.TEACHER)
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_student  = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)
    def has_perm(self , perm, obj = None):
        return self.is_admin
      
    def has_module_perms(self , app_label):
        return True
   
    
    def save(self,*args,**kwargs):
        if not self.role or self.role == None:
            self.role = UserAccount.Types.TEACHER
        # if self._state.adding:  # Only set the password when creating a new instance
        #     self.password = make_password(self.password)
        return super().save(*args,**kwargs)


class StudentManager(models.Manager):
    def create_user(self,email,password=None):
        if not email or len(email) <=0:
            raise ValueError("Eamil field is required")
        if not password:
            raise ValueError("Password is Must")
        email = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save()
        return user
    def get_queryset(self,*args,**kwargs):
        queryset =  super().get_queryset(*args,**kwargs)
        queryset = queryset.filter(role = UserAccount.Types.STUDENT)
        return queryset

class Student(UserAccount):
    class Meta:
        proxy = True
    objects = StudentManager()

    def save(self , *args , **kwargs):
        self.role = UserAccount.Types.STUDENT
        self.is_student = True
        if self._state.adding:  # Only set the password when creating a new instance
            self.password = make_password(self.password)
        return super().save(*args , **kwargs)

class TeacherManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save()
        return user
        
    def get_queryset(self , *args , **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(role = UserAccount.Types.TEACHER)
        return queryset
    
class Teacher(UserAccount):
    class Meta :
        proxy = True
    objects = TeacherManager()
      
    def save(self  , *args , **kwargs):
        self.role = UserAccount.Types.TEACHER
        self.is_teacher = True
        if self._state.adding:  # Only set the password when creating a new instance
            self.password = make_password(self.password)
        return super().save(*args , **kwargs)

class StudentProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user.email)

class TeacherProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user.email)

@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ST":
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=Teacher)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TE":
        TeacherProfile.objects.create(user=instance)

# from django.db import models
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# class UserAccount(AbstractUser):
#     class Role(models.TextChoices):
#         ADMIN = "ADMIN", "Admin"
#         STUDENT = "STUDENT", "Student"
#         TEACHER = "TEACHER", "Teacher"

#     base_role = Role.ADMIN
#     # USERNAME_FIELD = "email"
#     role = models.CharField(max_length=50, choices=Role.choices)

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.role = self.base_role
#         if self._state.adding:  # Only set the password when creating a new instance
#             self.password = make_password(self.password)

#         return super().save(*args, **kwargs)
#     # def save(self,*args,**kwargs):
#     #     if not self.role or self.role == None:
#     #         self.role = UserAccount.Types.TEACHER
#     #     if self._state.adding:  # Only set the password when creating a new instance
#     #         self.password = make_password(self.password)
#         # return super().save(*args,**kwargs)
#     def __str__(self):
#         return str(self.email)


# class StudentManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=UserAccount.Role.STUDENT)


# class Student(UserAccount):

#     base_role = UserAccount.Role.STUDENT

#     student = StudentManager()

#     class Meta:
#         proxy = True

#     def welcome(self):
#         return "Only for students"


# @receiver(post_save, sender=Student)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "STUDENT":
#         StudentProfile.objects.create(user=instance)


# class StudentProfile(models.Model):
#     user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
#     student_id = models.IntegerField(null=True, blank=True)


# class TeacherManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=UserAccount.Role.TEACHER)


# class Teacher(UserAccount):

#     base_role = UserAccount.Role.TEACHER

#     teacher = TeacherManager()

#     class Meta:
#         proxy = True

#     def welcome(self):
#         return "Only for teachers"


# class TeacherProfile(models.Model):
#     user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
#     teacher_id = models.IntegerField(null=True, blank=True)


# @receiver(post_save, sender=Teacher)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "TEACHER":
#         TeacherProfile.objects.create(user=instance)