from dataclasses import field
from rest_framework import serializers
from vocabularies.models import Vocabulary, Word

class VocabularySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vocabulary
        fields = ('id','name','description') #profile bilgisini göndermeyeceğiziiz iin dahil etmedik o bilgi rew-quest uzerinden gelecek
        

class WordSerializer(serializers.ModelSerializer):
    vocabulary = serializers.PrimaryKeyRelatedField(read_only=True) #PrimaryKeyRelatedField yazarak vocabulary nesnesi değil id olarak dönerecek, ve read ony yaptık ki bodyde değil url uzerinden bu bilgiyi vereceğiz
    
    class Meta:
        model= Word
        fields='__all__'