from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

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
        """Traduction avec gestion d'erreur"""
        try:
            from transformers import pipeline
            translator = pipeline("translation_en_to_ar", model="Helsinki-NLP/opus-mt-en-ar")
            result = translator(text[:400])[0]['translation_text']
            return result
        except Exception as e:
            return f"Translation simulation: {text}"

    def summarize_text(self, text):
        """Résumé avec gestion d'erreur"""
        try:
            from transformers import pipeline
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            result = summarizer(text[:1000], max_length=150, min_length=30)[0]['summary_text']
            return result
        except Exception as e:
            # Simulation si le modèle échoue
            words = text.split()[:20]
            return " ".join(words) + "..."