from django.urls import path


from vocabularies.views import CopyVocabularyView,VocabularyListCreateView, VocabularyDetailView,  WordListCreateView,WordDetailView

urlpatterns = [
    path('',VocabularyListCreateView.as_view(),name='vocabularies'), # api/vocabulary/ ye ek olarak api/vocabulary/?profile_id=1 dersek de 1 nid l, profilin vocabulerylerini isteleyeveğiz
    # path('<int:pk>/',VocabularyDetailView.as_view(),name='vocabulary_detail'),
    path('<int:id>/',VocabularyDetailView.as_view(),name='vocabulary_detail'), #pk deseydik otmatik algılanırdı id dediğimiz için view de loop up parametresini id yapmalıyız, örnek olsun diye yaptık
    
    path('<int:vocabulary_id>/words/',WordListCreateView.as_view(),name='words'),
    path('<int:vocabulary_id>/words/<int:word_id>',WordDetailView.as_view(),name='word_detail'),
    
    path('<int:vocabulary_id>/copy',CopyVocabularyView.as_view(),name='copy_vocabulary'),
]