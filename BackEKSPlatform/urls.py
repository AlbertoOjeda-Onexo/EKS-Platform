"""
URL configuration for BackEKSPlatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Api.views.chatbot_assistant_view import ask_chatbot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('Api.urls')),
    path('api/humanResources/', include('HumanResources.urls')),
    path('api/training/', include('Training.urls')),

    # Agentes de IA con OpenAI
    path('api/chat/ask/', ask_chatbot, name='chat_bot'),    
    # path('api/chat/file_scanner/', file_scanner.as_view(), name='openai_file_scanner'),
    # path('api/chat/field_filler/', fields_filler.as_view(), name='openai_field_filler')
]
