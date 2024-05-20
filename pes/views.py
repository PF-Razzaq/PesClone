
import jwt
import datetime
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,EventsSerializer
from .models import User,PesEvents,PesExecutor
from django.http import HttpResponse
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.contrib.auth.hashers import make_password
from .serializers import ChangePasswordSerializer
from django.db import connection
from rest_framework.decorators import permission_classes,api_view,authentication_classes
from rest_framework import generics, permissions
import logging
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
logger = logging.getLogger(__name__)



User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise AuthenticationFailed('Username and password are required.')

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        with connection.cursor() as cursor:
            cursor.execute("SELECT FSPID, RoutingID FROM FSPs f INNER JOIN pes_user pu ON pu.username = f.Username AND pu.username = %s", [username])
            results = cursor.fetchone()

        if not results:
            raise AuthenticationFailed('FSPID or RoutingID not found for the user.')

        fsp_id, routing_id = results

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=35),
            'iat': datetime.datetime.utcnow()
        }

        # Convert expiration time to Unix timestamp
        payload['exp'] = int(payload['exp'].timestamp())

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'username': username,
            'FSPID': fsp_id,
            'RoutingID': routing_id,
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
class AddRandomCode(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            random_code_int = None
            while not (random_code_int and len(str(random_code_int)) == 4):
                random_code = ''.join(random.choices(string.digits, k=4))
                random_code_int = int(random_code)
            send_mail(
                'Password Reset Code',
                f'Your password reset code is: {random_code_int}',
                'abdulrazzaqchohan1@gmail.com',
                [email],
                fail_silently=False,
                html_message=f'<p>Your OTP is {random_code_int}</p>'
            )
            user.otpCode = random_code_int
            user.save()
            return JsonResponse({'message': 'Random code added successfully'}, status=200)
        else:
            return JsonResponse({'Error': 'Email does not exist in the database'}, status=409)


class CheckCodeExist(APIView):
    def post(self, request):
        code = request.data.get('otpCode')
        try:
            user = User.objects.get(otpCode=code)
            return JsonResponse({'Successfly code match': code}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'Error':'Code mismatched'}, status=409)
        
class ChangePassword(APIView):
    def post(self, request):
        code = request.data.get('otpCode')
        password = request.data.get('password')
        try:
            user = User.objects.get(otpCode=code)
            user.set_password(password)
            user.otpCode = None
            user.save()
            return JsonResponse({'Successfly change Password': code}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'Error':'Code mismatched'}, status=409)
    

# Data insert api



# class CreateRecordAPIView(APIView):
#     def post(self, request):
#         data = request.data

#         with connection.cursor() as cursor:
#             cursor.execute(
#     "INSERT INTO Events (FSPID, eventdate, d_First, d_middle_a, d_middle_b, d_Last, d_Maiden, d_Address, d_Unit, d_City, d_Prov, d_Postal, d_AreaCode, d_exchange, d_phone, d_DOB, d_birth_Country, d_birth_City, d_birth_Prov, d_DOD, d_death_Country, d_death_City, d_death_Prov, d_death_age, d_dispdate, d_disp_Name, d_SIN, e_Salutation, e_First, e_Initial, e_Last, e_Address, e_Unit, e_City, e_Prov, e_Postal, e_AreaCode, e_exchange, e_phone_4, e_relationship) VALUES (%s,GETDATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#     [
#         data.get('FSPID'), data.get('d_First'), data.get('d_middle_a'), data.get('d_middle_b'), data.get('d_Last'), data.get('d_Maiden'),
#         data.get('d_Address'), data.get('d_Unit'), data.get('d_City'), data.get('d_Prov'), data.get('d_Postal'),
#         data.get('d_AreaCode'), data.get('d_exchange'), data.get('d_phone'), data.get('d_DOB'), data.get('d_birth_Country'),
#         data.get('d_birth_City'), data.get('d_birth_Prov'), data.get('d_DOD'), data.get('d_death_Country'), data.get('d_death_City'),
#         data.get('d_death_Prov'), data.get('d_death_age'), data.get('d_dispdate'), data.get('d_disp_Name'), data.get('d_SIN'),
#         data.get('e_Salutation'), data.get('e_First'), data.get('e_Initial'), data.get('e_Last'), data.get('e_Address'),
#         data.get('e_Unit'), data.get('e_City'), data.get('e_Prov'), data.get('e_Postal'), data.get('e_AreaCode'),
#         data.get('e_exchange'), data.get('e_phone_4'), data.get('e_relationship')
#     ]
# )


#         return Response({'Record created successfully'}, status=status.HTTP_201_CREATED)

# For Database
# def my_view(request):
#     data = read_data_from_database()
#     # Process the data as needed
#     return HttpResponse("Data read from database successfully")


# class EventsListCreateView(generics.ListCreateAPIView):
#     queryset = PesEvents.objects.all()
#     serializer_class = EventsSerializer

#     def get_pes_events_data(self):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT eventID, e_Last FROM PesEvents")
#             rows = cursor.fetchall()
#             print('rows',rows)
#             return rows

@api_view(['GET'])
def events_list(request):
    if request.method == 'GET':
        events = PesEvents.objects.all()
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data)
    

@api_view(['POST'])
def events_create(request):
    if request.method == 'POST':
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            # Save the PesEvents object
            pes_event = serializer.save()

            eventID = serializer.data.get('eventID')
            e_Last = serializer.data.get('e_Last')

            random_number = random.randint(1000, 9999)
            
            # Remove apostrophes from the last name
            modified_l_name = e_Last.replace("'", "")

            username = modified_l_name + str(random_number)

            password = str(random.randint(100000, 999999))

            # Connect to the database and save username, password, and Status=1 in PesExecutor table
            executor = PesExecutor.objects.create(Username=username, Password=password, Status=1)
            executor_id = executor.ExecutorID

            # Update the PesEvents object with the executor_id
            pes_event.ExecutorID = executor_id
            pes_event.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PesEvents.objects.all()
    serializer_class = EventsSerializer


@api_view(['GET'])
# @permission_classes([IsAdminUser])
# @authentication_classes([SessionAuthentication])
def filter_pes_events_by_fspid(request, fspid):
    try:
        pes_events = PesEvents.objects.filter(FSPID=fspid)
        serializer = EventsSerializer(pes_events, many=True)
        return Response(serializer.data)
    except PesEvents.DoesNotExist:
        return Response({'message': 'No records found for the specified FSPID'}, status=status.HTTP_404_NOT_FOUND)

# class EventsListCreateView(generics.ListCreateAPIView):
#     queryset = PesEvents.objects.all()
#     serializer_class = EventsSerializer

#     def get(self, request, *args, **kwargs):
#         # Check for JWT in request cookies
#         token = request.COOKIES.get('jwt')

#         if not token:
#             return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return Response({'error': 'Authentication credentials were expired.'}, status=status.HTTP_401_UNAUTHORIZED)

#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         # Check for JWT in request cookies
#         token = request.COOKIES.get('jwt')
#         if not token:
#             return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return Response({'error': 'Authentication credentials were expired.'}, status=status.HTTP_401_UNAUTHORIZED)

#         return super().post(request, *args, **kwargs)

# class EventsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PesEvents.objects.all()
#     serializer_class = EventsSerializer

#     def put(self, request, *args, **kwargs):
#         # Check for JWT in request cookies
#         token = request.COOKIES.get('jwt')

#         if not token:
#             return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return Response({'error': 'Authentication credentials were expired.'}, status=status.HTTP_401_UNAUTHORIZED)

#         return super().put(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         # Check for JWT in request cookies
#         token = request.COOKIES.get('jwt')

#         if not token:
#             return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return Response({'error': 'Authentication credentials were expired.'}, status=status.HTTP_401_UNAUTHORIZED)

#         return super().delete(request, *args, **kwargs)