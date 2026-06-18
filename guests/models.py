from django.db import models


class Guest(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Prénom')
    last_name = models.CharField(max_length=100, verbose_name='Nom')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Téléphone')
    id_number = models.CharField(max_length=50, blank=True, verbose_name='N° Pièce identité')
    id_type = models.CharField(
        max_length=20,
        choices=[('passport', 'Passeport'), ('id_card', "Carte d'identité"), ('driver_license', 'Permis de conduire')],
        blank=True,
        verbose_name='Type pièce identité'
    )
    nationality = models.CharField(max_length=100, blank=True, verbose_name='Nationalité')
    address = models.TextField(blank=True, verbose_name='Adresse')
    city = models.CharField(max_length=100, blank=True, verbose_name='Ville')
    country = models.CharField(max_length=100, blank=True, verbose_name='Pays')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date de naissance')
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
