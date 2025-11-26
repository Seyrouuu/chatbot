from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# Variables globales pour les modèles
translator = None
summarizer = None

def get_translator():
    global translator
    if translator is None:
        from transformers import pipeline
        translator = pipeline("translation_en_to_ar", model="Helsinki-NLP/opus-mt-en-ar")
    return translator

def get_summarizer():
    global summarizer
    if summarizer is None:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        text = data.get("text")
        action = data.get("action")

        if not text or not action:
            return JsonResponse({"error": "Missing text or action"}, status=400)

        try:
            if action == "translate":
                result = self.translate_text(text)
            elif action == "summarize":
                result = self.summarize_text(text)
            else:
                return JsonResponse({"error": "Invalid action"}, status=400)

            return JsonResponse({"result": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def translate_text(self, text):
        try:
            model = get_translator()
            result = model(text[:500])[0]['translation_text']  # Limiter la longueur
            return result
        except Exception as e:
            return f"Translation error: {str(e)}"

    def summarize_text(self, text):
        try:
            model = get_summarizer()
            result = model(text[:1000], max_length=150, min_length=30)[0]['summary_text']
            return result
        except Exception as e:
            return f"Summarization error: {str(e)}"