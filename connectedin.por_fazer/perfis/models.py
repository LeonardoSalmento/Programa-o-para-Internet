from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Perfil(models.Model):
#     nome = models.CharField(max_length=255, null=False)
#     telefone = models.CharField(max_length=20, null= False)
#     nome_empresa = models.CharField(max_length=255, null=False)
#     email = models.CharField(max_length=255, null=False)
#     contatos = models.ManyToManyField('Perfil')

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    #sem email
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self', related_name = 'meus_contatos')
    usuario = models.OneToOneField(User, related_name="perfil", on_delete = models.CASCADE)
    
    @property
    def email(self):
        return self.usuario.email


    def __str__(self):
        return self.nome

    def desfazer_amizade(self, perfil_a_excluir):
        perfil_a_excluir.contatos.remove(self.id)
        self.contatos.remove(perfil_a_excluir.id)
        

    def convidar(self, perfil_convidado):
        if self.pode_convidar(perfil_convidado):
            convite = Convite(solicitante=self,convidado = perfil_convidado)
            convite.save()  

    def pode_convidar(self, perfil_convidado):
        return self.id != perfil_convidado.id and perfil_convidado not in self.contatos.all()

    def redefinir_senha(self):
        pass        
        


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):        
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()

    def recusar(self):
        self.delete()


