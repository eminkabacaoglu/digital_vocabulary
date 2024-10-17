from django.dispatch import receiver
from django.db.models.signals import post_save
from profiles.models import Profile

# from profiles.models import CustomUser
from django.contrib.auth import get_user_model # yukarıdakinin yerine bunu yazmak daha mantıklu cınku CustomUser artık aktif user modelimiz

User = get_user_model()

@receiver(post_save, sender = User)
def create_user_profile(sender,instance,created,**kwargs): #yeni bir user oluştugunda tetiklenecek, user nesnesi yeni oluşturulan bir kayıt ise created parametresi true olur, bizim de ilgilendiğimiz durum bu
    if created:
        Profile.objects.create(user=instance) # buradaki instance , fonksiyonu tetkikleyen,kaydedilen, user nesnesini temsil eder