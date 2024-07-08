from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserSerializer, OrganizationSerializer, Organization, AddUserToOrganizationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
import uuid
from .models import User



class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': {
                        'userId': user.userId,
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone,
                    }
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': {
                        'userId': user.userId,
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone,
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Bad request',
                'message': 'Authentication failed',
                'statusCode': 401
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'userId'
    lookup_url_kwarg = 'userId'
    permission_classes = [IsAuthenticated]


class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    

class OrganizationDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'orgId'
    lookup_url_kwarg = 'orgId'
    permission_classes = [IsAuthenticated]

class OrganizationCreateView(generics.CreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(orgId=str(uuid.uuid4()))
        
class AddUserToOrganizationView(generics.GenericAPIView):
    serializer_class = AddUserToOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId):
        organization = get_object_or_404(Organization, orgId=orgId)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, userId=serializer.validated_data['userId'])
        organization.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organization successfully"
        })
