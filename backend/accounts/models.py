from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django_extensions.db.models import TimeStampedModel

class UserManager(BaseUserManager):
    """Gestionnaire personnalisé pour le modèle User."""

    def create_user(self, email, username, role, phone_number,password=None):
        """Créer et enregistrer un utilisateur avec un email, un username, un rôle et un mot de passe."""
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email.")
        if not role:
            raise ValueError("L'utilisateur doit avoir un rôle.")

        # Normalisation de l'email
        email = self.normalize_email(email)
        # Création de l'utilisateur
        user = self.model(email=email, username=username, role=role, phone_number=phone_number,is_active=True)
        # Hachage du mot de passe
        user.set_password(password)
        # Sauvegarde de l'utilisateur dans la base de données
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number,password=None):
        """Créer et enregistrer un super-utilisateur avec un email, un username et un mot de passe."""
        user = self.create_user(email, username, role=Account.Role.ADMIN, password=password, phone_number=phone_number)
        # Définir les permissions de super-utilisateur
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Modèle personnalisé pour les utilisateurs."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DIPLOME = "DIPLOME", "Diplomé"
        INSTITUTION = "INSTITUTION", "Institution"
        EMPLOYE = "EMPLOYE", "Employé"

    username = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)

    role = models.CharField(max_length=50, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Relations avec les groupes et les permissions
    groups = models.ManyToManyField(Group, related_name='account_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='account_user_permissions_set')

    # Champs pour la gestion de l'OTP
    dob = models.DateField(null=True, blank=True)
    otp = models.PositiveIntegerField(null=True, blank=True, unique=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.PositiveIntegerField(default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    # Utilisation du gestionnaire personnalisé
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

# Modèles proxy pour les différents rôles d'utilisateurs
class DiplomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.DIPLOME)

class Diplome(Account):
    """Modèle proxy pour les utilisateurs ayant le rôle 'Diplomé'."""
    objects = DiplomeManager()

    class Meta:
        proxy = True

class InstitutionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.INSTITUTION)

class Institution(Account):
    """Modèle proxy pour les utilisateurs ayant le rôle 'Institution'."""
    objects = InstitutionManager()

    class Meta:
        proxy = True

class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.ADMIN)

class Admin(Account):
    """Modèle proxy pour les utilisateurs ayant le rôle 'Admin'."""
    objects = AdminManager()

    class Meta:
        proxy = True

class EmployeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.ADMIN)

class Employe(Account):
    """Modèle proxy pour les utilisateurs ayant le rôle 'Admin'."""
    objects = EmployeManager()

    class Meta:
        proxy = True