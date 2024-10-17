from django.urls import path


from exercises.views import QuestionView

urlpatterns = [
    path('questions/',QuestionView.as_view(),name='create-questions'),
]