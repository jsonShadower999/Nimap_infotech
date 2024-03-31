
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Client, Project, User
from .serializers import ClientDetailSerializer, ClientSerializer, ClientGetAllSerializer,ProjectReadSerializer,  ProjectSerializer, ProjectWriteSerializer
from .models import Project

from django.contrib.auth.decorators import login_required



# api to retrive details for all clients
@api_view(['GET', 'POST'])
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

#api to retrive details specific to single client
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'GET':
      
        serializer = ClientGetAllSerializer(client)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = ClientDetailSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        client.delete()
        return Response(status=204)

#api for projecgt related data retrival
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectReadSerializer


    def get_serializer_class(self):
        if self.action in ['retrive', 'list']:
            return ProjectSerializer
        return ProjectWriteSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ProjectReadSerializer(serializer.instance).data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        
        return Response(ProjectSerializer(project).data, status=200)


#login the user by using loginuser.html in templates and then register them to retrive all detailsof user with project in same page
@csrf_exempt
def login_page(request):
    if request.method == 'POST':
       # data = json.loads(request.body)
        username = request.POST.get('username')
       #username = data.get('username')
        password = request.POST.get('password')
        User = get_user_model() 
        user = User.objects.get(username=username)
        user_projects = user.project_set.all()
        if user is not None:  # user = authenticate(username=username, password=password)
      
            login(request, user)
            # Redirect to a success page or dashboard
            return render(request, 'loginuser.html', {'user_projects': user_projects,'user':user})
           # return redirect('loginuser',)  # Replace 'dashboard' with the name of your dashboard URL pattern
        else:
            # Handle invalid login credentials
            return render(request, 'loginuser.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'loginuser.html')

