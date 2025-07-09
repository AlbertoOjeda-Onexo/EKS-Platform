from openai import OpenAI
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from HumanResources.models.vacant_position_model import VacantPosition
from HumanResources.serializers.vacant_position_serializer import VacantPositionSerializer
from decouple import config
from dotenv import load_dotenv

load_dotenv()

# --- Configuración del API KEY de OpenAI ---
OPENAI_API_KEY = config('OPEN_AI_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Función para generar una publicación de una vacante específica ---
@method_decorator(csrf_exempt, name='dispatch')
class publish_vacant_description(View):
    def get(self, request, pk):
        try:
            # --- Obtener la vacante desde la base de datos ---
            vacante = VacantPosition.objects.filter(idVacantPosition=pk, fdl=0).first()
            if not vacante:
                return JsonResponse({"error": "Vacante no encontrada"}, status=404)

            # --- Serializar la vacante ---
            serializer = VacantPositionSerializer(vacante)
            data = serializer.data

            # --- Formatear datos clave como texto ---
            formatted_data = f"""
                                Título: {data.get('title')}
                                Descripción interna: {data.get('description')}
                                Fecha de vencimiento: {data.get('expire_date')}
                                Estatus: {data.get('status')}

                                Detalles:
                            """
            for campo in data.get("valores_dinamicos", []):
                formatted_data += f"- {campo['fieldName']}: {campo['value']}\n"

            # --- Solicitamos la descripción para la publicación al agente ---
            response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un generador profesional de publicaciones de empleo. "
                            "Eres un asistente de talento especializado en crear publicaciones de empleo para EKS Solutions, "
                            "una consultoría en tecnología empresarial y partner de Oracle en México. "
                            "Su cultura se basa en valores como confianza, compañerismo, innovación, excelencia, compromiso, integridad y ética profesional. "
                            "Además participan activamente en proyectos de RSE y voluntariado."
                            "Tu objetivo es transformar datos estructurados de vacantes "
                            "en una publicación atractiva para sitios de empleo."
                            "**Tono:** Profesional, cercano, positivo, enfocado en crecimiento profesional y aprendizaje."
                            "**Etiquetas y hashtags:** Incluir hashtags relevantes (#Oracle, #Tecnología, #Consultoría, #TalentoJoven, #Innovación, #Puebla, etc.)."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            "Genera una descripción profesional, llamativa y clara de esta vacante:\n\n" + formatted_data
                        )
                    }
                ]
            )

            return JsonResponse({'text': response.output_text})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
                                
