import requests
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import UserSerializer
from api.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken


@api_view(['POST', 'GET', ])
def home(request, *args, **kwargs):
    """
    retrieve:
        Return a user instance.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """
    code = str(kwargs.get('ref_code'))
    data = {}
    print(request.COOKIES)
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered new user by ref"
            data['username'] = user.username
            if request.session['ref_profile'] is not None:
                recommended_by_profile = Profile.objects.get(id=request.session.get('ref_profile'))
                registered_user = User.objects.get(id=user.id)
                registered_profile = Profile.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
            return Response(data)

    except:
        pass
    print(request.session.get_expiry_date())
    data['response'] = f"referred by{profile}"
    return Response(data)


def request_view(request):
    s = requests.Session()
    s.get('https://appforlanguage.com/auth/google/success')
    print(s.__dict__)
    print(s.headers)
    return HttpResponse(s)


@api_view(['POST', ])
def registration_view(request):
    serializer = UserSerializer(data=request.data)
    profile_id = request.session.get('ref_profile')
    if request.method == 'POST':

        data = {}
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data['response'] = "successfully registered new user"
            data['username'] = user.username
            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)
                registered_user = User.objects.get(id=user.id)
                registered_profile = Profile.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
                return Response({
                    'data': data,
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            else:
                data['username'] = user.username
                data['password'] = user.password
                data['access'] = str(refresh)
        else:
            data = serializer.errors
        return Response({
            'data': data,

        })


@api_view(['GET', ])
def my_recommendations_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    my_recs = profile.get_recommended_profiles()
    spec_list = {','.join(str(v) for v in my_recs)}
    return Response(spec_list, status=status.HTTP_200_OK)
