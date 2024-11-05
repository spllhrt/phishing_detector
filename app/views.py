from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, PhishingRequestSerializer
from .models import EmailAnalysis
from .phishing_detector import perform_phishing_detection
import logging
import nltk

# Download necessary packages (only needed once)
nltk.download('punkt')  # For tokenization
nltk.download('stopwords')  # If you're using stop words
nltk.download('punkt_tab')
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate user with email instead of username
        try:
            user = User.objects.get(email=email)  
            if user.check_password(password):  
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PhishingDetectionView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PhishingRequestSerializer(data=request.data)
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            subject = serializer.validated_data['subject']
            content = serializer.validated_data['content']

            email_data = EmailAnalysis(sender=sender, subject=subject, content=content)
            email_data.save()

            try:
                detection_result = perform_phishing_detection({'sender': sender, 'subject': subject, 'content': content})
                email_data.is_phishing = detection_result['is_phishing']
                email_data.confidence_score = detection_result['confidence_score']
                email_data.save()  # Save the updated is_phishing and confidence score

                message = "This email is considered phishing." if detection_result['is_phishing'] else "This email is not considered phishing."
                return Response({'is_phishing': detection_result['is_phishing'], 'message': message, 'confidence_score': detection_result['confidence_score']}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error in PhishingDetectionView: {str(e)}")
                return Response({'detail': 'There was an error detecting phishing. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
