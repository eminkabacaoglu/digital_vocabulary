import profile
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from vocabularies.serializers import VocabularySerializer,WordSerializer
from rest_framework.views import APIView
from profiles.models import Profile
from vocabularies.models import Vocabulary, Word
from vocabularies.permissions import IsOwnerOrReadOnly,IsOwnerOfVocabularyOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.

class VocabularyListCreateView(ListCreateAPIView):
    serializer_class = VocabularySerializer
    
    # kullanıcının vocabulart listi gelmesi için queryset i özelleştiriyoruz
    def get_queryset(self):
        profile_id = self.request.query_params.get("profile_id") #api/vocabulary/?profile_id=1 böylebir talp gelmesi duruu için
        if profile_id:
            profile = get_object_or_404(Profile, id=profile_id)
        else:
            profile = get_object_or_404(Profile,user=self.request.user)
            # profile = self.request.user.profile #u şekilde de olur yukardaki gibi de
        
        queryset = Vocabulary.objects.filter(profile=profile)
        
        return queryset
    
    def perform_create(self, serializer): #perform_create methodunu override ediyoruz, bu method serializer ı save methodu calısmadan önce çalışır
        serializer.save(profile=self.request.user.profile) #VocabularySerializer içindel, fieldlarda profile yok ama modelimizde var yani save ederken göndermemiş lazım
        
        
class VocabularyDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Vocabulary.objects.all()
    serializer_class=VocabularySerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly] #bir kullanıcının farklı bir kullanıcının vocabulary nesnesi üerinde güncelleme ve silme yapamaması için yazıyoruz
    lookup_field ='id' #pk deseydik otmatik algılanırdı ve burayı eklemeye gerek olmazdı ama urls.pyde id dediğimiz için view de loop up parametresini id yapmalıyız, örnek olsun diye yaptık
    

class WordListCreateView(ListCreateAPIView):
    serializer_class = WordSerializer
    
    def get_queryset(self):
        vocabulary_id =self.kwargs.get("vocabulary_id")
        foundVocabulary = get_object_or_404(Vocabulary, id = vocabulary_id)
        
        print("self.kwargs: ",self.kwargs) #self.kwargs:  {'vocabulary_id': 1}
        
        return Word.objects.filter(vocabulary=foundVocabulary)
    
    
    def perform_create(self, serializer): #perform_create methodunu override ediyoruz, bu method serializer ı save methodu calısmadan önce çalışır
        vocabulary_id =self.kwargs.get("vocabulary_id")
        foundVocabulary = get_object_or_404(Vocabulary, id = vocabulary_id,profile=self.request.user.profile) #kendi vocabularysş hariç ekleme yapamasın<
        
        serializer.save(vocabulary=foundVocabulary)
        
class WordDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = WordSerializer
    queryset = Word.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOfVocabularyOrReadOnly]
    
    def get_object(self): # override ediyoruz
        vocabulary_id =self.kwargs.get("vocabulary_id")
        word_id =self.kwargs.get("word_id")
        
        word = get_object_or_404(Word,id=word_id,vocabulary_id=vocabulary_id)
        self.check_object_permissions(self.request, word) # get object kullandığımız için permission classlarıı manuel tetikliyoruz
        
        # IsOwnerOfVocabularyOrReadOnly gibi obje düzeyinde yetki denetimi yapan bir permission sınıfının tam anlamıyla işlemesi için self.check_object_permissions(self.request, word) metoduna ihtiyaç vardır.
        
        return word

class CopyVocabularyView(APIView): #öelleştirmenın oldugu görece karmaşık bir view ondan Apiview tanımladık
    
    def post(self,request,vocabulary_id):
        original_vocabulary =get_object_or_404(Vocabulary, id=vocabulary_id) # self.kwargs.get("vocabulary_id") bu da olur
        copied_vocabulary = Vocabulary.objects.create(
            profile = request.user.profile,
            name=f"Copy of {original_vocabulary.name}",
            description=f"Copy of {original_vocabulary.description}"
            
        )
        
        words = Word.objects.filter(vocabulary=original_vocabulary)

        for word in words:
            Word.objects.create(
                vocabulary = copied_vocabulary,
                text=word.text,
                meaning=word.meaning,
                example_sentence = word.example_sentence
            )
            
            return Response({
                "success":"Vocabualary copied successfully"
            })