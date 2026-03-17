from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tarefa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return self.nome