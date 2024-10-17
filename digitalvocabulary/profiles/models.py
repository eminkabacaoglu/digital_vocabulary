from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser): #kendi tanımladığımız user modeline göre uygulamayı çalıştırmak istiyor isek setting dosyasına AUTH_USER_MODEL = 'profiles.CustomUser'bunu eklememiz gerek #ilk migrasyonu bu tanımlamayı yaptıktan sonra yapmak lazım yoksa tutarsızlık hatası gelir, mevcutt durumda da geldi bu yuzden herokudan db yi restleyim tekrar migratin yaparız
    pass

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    followers = models.ManyToManyField('self',through='FollowRelation',symmetrical=False, related_name='followings') #modelin kendisini vereceğimiz için self dedik, takipleşme profiller arası olduğu için<s
    #through='FollowRelation' olusacak junction table FollowRelation modeline göre oluşsun diye bu parametreyi yazdık
    #symetrical=False parametresi ise A kişisi B yi takip ediyor fakat B Ayı takip etmek zorunda değil , biri birini takip ettiğinde tam tersi ilişkinin junction table a eklenmemesi için bu parametreyi yazıyoruz
    #related_name='followings' follower gözündern takip ettiği profilleri ifade eder

    def __str__(self):
        return f"{self.user.username} {self.pk}" #seşf.pk yerine self.id de denebilirdi aynı sey

class FollowRelation(models.Model):
    #foreignkey many-to-one ilişkidir
    follower = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='followed_by')
    following = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='follows')
    created =models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower','following') #manytomant tabloda ilişkinin tek olması için yazdık yani 1 ile 4 eşleşti tekrar 4 ile 1 için de ayrı kayıt olmasın diye
        
    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"