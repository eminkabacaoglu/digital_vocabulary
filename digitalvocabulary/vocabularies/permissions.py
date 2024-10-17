from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj): # bu özel methodu override ediyoruz
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.profile.user == request.user #objenin user ı ile requesti yapan user aynı ı
    
class IsOwnerOfVocabularyOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): # bu özel methodu override ediyoruz
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.vocabulary.profile.user == request.user