from rest_framework.views import APIView
from profiles.serializers import RegisterSerializer,UserSerializer,ProfileSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from profiles.models import Profile, FollowRelation

from django.shortcuts import get_object_or_404
from rest_framework import status

# Create your views here.

class RegisterView(APIView):
    permission_classes=(permissions.AllowAny,)
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        user_serializer = UserSerializer(user)
        
        return Response(user_serializer.data)

class ProfileSearchView(ListAPIView): #bu viewde listeleme yapılacağı için kullanıyouz
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username','')
        
        if username:
            return Profile.objects.filter(user__username__icontains=username)
        
        return Profile.objects.none()
    

class FollowProfileView(APIView): #daha esnek bir yapı kurmak istediğimiz için APIView dan miras eldık
    
    def post(self,request,username): #username urlden gelecek parametreolarak
        profile_to_follow = get_object_or_404(Profile,user__username=username)
        if request.user.profile == profile_to_follow: #istegi gonderen ile takip edilmek istenen user aynı mı kontrolü
            return Response({"error": "You can not follow yourself"},status=status.HTTP_400_BAD_REQUEST)
        
        obj, created = FollowRelation.objects.get_or_create(follower=request.user.profile, following =profile_to_follow) # ilişki yoksa kaydet yoksa etme 
        
        # Check if the follow relation was just created
        if created:
            return Response({"success": "User followed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"info": "You are already following this user"}, status=status.HTTP_200_OK)
        
        # return ResourceWarning({
        #     "success":"User followed successfully"
        # },status=status.HTTP_200_OK)
        
class UnFollowProfileView(APIView): #daha esnek bir yapı kurmak istediğimiz için APIView dan miras eldık
    
    def post(self,request,username): #username urlden gelecek parametreolarak
        profile_to_unfollow = get_object_or_404(Profile,user__username=username)
        
        follow_relation = FollowRelation.objects.filter(follower=request.user.profile, following=profile_to_unfollow)
        
        if follow_relation.exists(): #takipten cıkılacak user takip ediliyor mu, takip edilmeyen bir profile unfollow iisteği atılmamalı
            follow_relation.delete()
            return Response({"success": "user unfollowed successfully"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "you are not following this user"},status=status.HTTP_400_BAD_REQUEST)
    
    
class FollowedListView(ListAPIView):
    serializer_class=ProfileSerializer
    
    def get_queryset(self):
        user_profile = self.request.user.profile
        return user_profile.followers.all()
    