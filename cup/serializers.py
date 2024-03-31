from rest_framework import serializers
from .models import Client, Project, User
from rest_framework import serializers
from .models import Client


       
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']
     
class ProjectSerializer(serializers.ModelSerializer):
    
    client_name = serializers.ReadOnlyField(source='client.client_name')
    class Meta:
        model = Project
        fields = ['id', 'project_name','created_at','created_by','client_name']


class ClientSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Client
        fields = ['id', 'client_name','created_at','created_by']        

class ClientDetailSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Client
        fields = ['id', 'client_name','created_at','created_by','updated_at']  

class ClientGetAllSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    
    class Meta:
        model = Client
        fields = ['id', 'client_name','created_at','created_by','updated_at','projects']          



# class ProjectSerializer_for_post(serializers.ModelSerializer):
#     user = UserSerializer(many=True, read_only=True)

#     class Meta:
#         model = Project
#         fields = ['id', 'project_name', 'client', 'user']

#     def create(self, validated_data):
#         users_data = validated_data.pop('user', [])
#         project = Project.objects.create(**validated_data)
#         project.user.set(users_data)
#         return project


# class ProjectSerializerall(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = '__all__'  # 


class ProjectReadSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    def get_users(self, obj):
        return UserSerializer(obj.users, many=True).data
    
    def get_client(self, obj):
        return obj.client.client_name

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'client', 'users', 'created_at', 'created_by')

class ProjectWriteSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client')
    users = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ['project_name', 'client_id', 'users']


    def create(self, validated_data):
        users_data = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        project.users.set(users_data)
        return project