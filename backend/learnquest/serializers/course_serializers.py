from serializers_import import *
from section_serializers import EnrolledViewSectionSerializer, UnenrolledViewSectionSerializer
from authentication.serializer import DisplayUserSerializer

class UnauthorizedViewCourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only = True)
    sections= serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Course
        fields = ["rating", "title", "instructor", "image", "price", "description", "created_at", "updated_at", "sections"]
        
    def get_rating(self, instance):
        return instance.rating
    
    def get_sections(self, instance):
        return UnenrolledViewSectionSerializer(instance= instance.sections, many = True).data
    
class AuthorizedViewCourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only = True)
    sections = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["rating", "title", "instructor", "image", "price", "description", "created_at", "updated_at", "sections"]
        
    def get_rating(self, instance):
        return instance.rating
    
    def get_sections(self, instance):
        return EnrolledViewSectionSerializer(instance= instance.sections, many = True).data
    
    
class InstructorViewCourseSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField(read_only = True)
    rating = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["rating", "title", "instructor", "students", "image", "price", "description", "created_at", "updated_at", "sections"]
        
    def get_students(self, instance):
        return DisplayUserSerializer(instance= instance.students, many = True).data
    
    def get_rating(self, instance):
        return instance.rating
    
class RequestCreateCourseSerializer(serializers.Serializer):
    pass


class ResponseCreateCourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["rating", "title", "instructor", "students", "image", "price", "description", "created_at", "updated_at"]
        
    def get_rating(self, instance):
        return instance.rating
    
class RequestUpdateCourseSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=True, required= False)
    price = serializers.FloatField(required= False)
    description =  serializers.CharField(allow_null=True, required= False)
    image = serializers.ImageField(required= False)
    

class ResponseUpdateCourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["rating", "title", "instructor", "students", "image", "price", "description", "created_at", "updated_at"]
        
    def get_rating(self, instance):
        return instance.rating