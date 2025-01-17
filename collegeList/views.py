from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.renderers import JSONRenderer
from .serializers import SignUpSerializer, StateSerializer
import asyncio
from playwright.async_api import async_playwright
from .models import States


async def fetch_data(url):
    colleges = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        )
        page = await context.new_page()

        response = await page.goto(url)
        if response.status == 200:
            json_data = await response.json()
            print("Response received successfully")

            for li in json_data['list']:
                colleges.append(li)
        else:
            print(f"Failed to fetch data. Status code: {response.status}")
        await browser.close()
        return colleges


def get_filtered_colleges(state_filter):
    url = f"https://pdf.aishe.nic.in/aishereports/report66?collegeType=ALL&reportType=JSON&stateCode={state_filter}&surveyYear=2022&universityName=ALL&universityType=ALL"
    colleges = asyncio.run(fetch_data(url))
    return {state_filter: colleges}


class SignupView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def get(self, request):
        # Return an empty form (serializer instance)
        serializer = SignUpSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User created successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        response = super().post(request, *args, **kwargs)

        # If the token is successfully generated, return it with a custom message
        if response.status_code == status.HTTP_200_OK:
            return redirect(reverse('college-data'))

        # If there's an issue, return the response
        return response


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.session)
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken.for_user(refresh_token)
            token.blacklist()
            return Response({
                "message": "Successfully logged out!",
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)


# LoginRequiredMixin
class CollegeListView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StateSerializer

    def get(self, request):
        full_url = request.build_absolute_uri()
        print(f"Full URL: {full_url}")
        serializer = self.get_serializer(data=request.query_params)

        if serializer.is_valid():
            state_filter = serializer.validated_data['state']
            colleges = get_filtered_colleges(state_filter)
            return Response({"url": full_url,state_filter: colleges}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)