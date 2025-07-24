import time
import json
from openai import OpenAI
from django.db import connection
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from decouple import config
from dotenv import load_dotenv

load_dotenv()

# Crea tu client con tu Key de OpenAI
OPENAI_API_KEY = config('OPEN_AI_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# Define tu assistant_id previamente en la consola de OpenAI o en tu código
ASSISTANT_ID = config('ASSISTANT_ID') 

@csrf_exempt
def ask_chatbot(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get('question')

        if not question:
            return JsonResponse({'error': 'No se ha proporcionado una pregunta'}, status=400)

        # Crear un nuevo hilo (thread)
        thread = client.beta.threads.create()

        # Añadir el mensaje del usuario
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Crear un run (proceso de respuesta del assistant)
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Polling hasta que se complete el run
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                return JsonResponse({'error': f"Fallo al generar respuesta: {run_status.status}"}, status=500)
            time.sleep(1)

        # Obtener los mensajes (respuesta del assistant)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_messages = [
            msg.content[0].text.value
            for msg in messages.data
            if msg.role == "assistant"
        ]

        if not assistant_messages:
            return JsonResponse({'error': 'No se obtuvo respuesta del asistente'}, status=500)

        return JsonResponse({'response': assistant_messages[0]}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
