from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from profiles.models import Profile
from vocabularies.models import Word
from rest_framework.response import Response
from rest_framework import status
import random

# Create your views here.
class QuestionView(APIView):
    
    def get(self,request):
        profile = get_object_or_404(Profile, user=request.user)
        
        words = Word.objects.filter(vocabulary__profile=profile)
        
        if words.count()<4: #words bir query settir <QuerySet [<Word: Cat>, <Word: Dog>, <Word: Dog>, <Word: House>]>
            return Response({
                "error":"Not enough words found. Please add at least 4 words"
            },status=status.HTTP_400_BAD_REQUEST)
        
        words_list = list(words)
        selected_word = random.choice(words_list)
        options = [selected_word.meaning]
        
        while len(options)<4:
            wrong_option=random.choice(words_list).meaning
            if wrong_option not in options: # dogru seçenek denk gelebilir , listeye tekrar eklemesin diye yazdık
                options.append(wrong_option)
        
        random.shuffle(options)
        
        question_data = {
            "question":selected_word.text,
            "options":options,
            "correct_answer":selected_word.meaning
        }
        
        return Response(question_data)