from django.contrib.auth.models import User
from django.core import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import UserSerializer
from api.models import Profile


@api_view(['POST', 'GET', ])
def home(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    data = {}
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


@api_view(['POST', ])
def registration_view(request):
    profile_id = request.session.get('ref_profile')
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered new user"
            data['username'] = user.username
            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)
                registered_user = User.objects.get(id=user.id)
                registered_profile = Profile.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
            else:
                data['username'] = user.username
                data['password'] = user.password
        else:
            data = serializer.errors
        return Response(data ,status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def my_recommendations_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    my_recs = profile.get_recommended_profiles()
    spec_list = {','.join(str(v) for v in my_recs)}
    return Response(spec_list,status=status.HTTP_200_OK)
