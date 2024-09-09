from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django_extensions.db.models import TimeStampedModel


class UserManager(BaseUserManager):
    """Gestionnaire personnalisé pour le modèle User."""

    def create_user(self, email, username, role, password=None):
        """Créer et enregistrer un utilisateur avec un email, un username, un rôle et un mot de passe."""
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email.")
        if not role:
            raise ValueError("L'utilisateur doit avoir un rôle.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """Créer et enregistrer un super-utilisateur avec un email, un username et un mot de passe."""
        user = self.create_user(email, username, role=Account.Role.ADMIN, password=password)
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

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='account_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='account_user_permissions_set')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


# Gestionnaires de modèles proxy
class DiplomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.DIPLOME)


class Diplome(Account):
    """Modèle proxy pour les utilisateurs ayant le rôle 'Diplomé'."""
    objects = DiplomeManager()

    class Meta:
        proxy = True


class InstitutionManager(models.Manager):
    """
        models.Manager est la classe de base par défaut fournie par Django pour gérer les requêtes de base de données d'un modèle
        elle répond parfaitement à nos besions de gestion et de filtrage de requêtes.
    """
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
