from django.db import models
from profiles.models import Profile

# Create your models here.
class Vocabulary(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='vocabularies') # related_name ile Profile uzerinden Profile ile ilişkilendirilmiş vocabulary nesnelerine erişmemizi sağlar
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) #blank=True  yani zorunlu değil
    
    def __str__(self):
        return f"{self.name} ({self.profile.user.username})"

class Word(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE,related_name='words') # vocabulary nesnesi üzerinden word nesnelerine erişim sağlanacak
    text = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    example_sentence = models.TextField()
    
    def __str__(self):
        return f"{self.text}"
    