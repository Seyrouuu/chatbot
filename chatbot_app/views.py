from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from transformers import pipeline

# تهيئة النماذج عند بداية تشغيل السيرفر
translator = pipeline("translation_en_to_ar", model="Helsinki-NLP/opus-mt-en-ar")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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
        """ترجمة النص من الإنجليزية إلى العربية"""
        try:
            translated = translator(text)[0]['translation_text']
            return translated
        except Exception as e:
            return f"Erreur traduction: {str(e)}"

    def summarize_text(self, text):
        """تلخيص النص"""
        try:
            summary = summarizer(text)[0]['summary_text']
            return summary
        except Exception as e:
            return f"Erreur résumé: {str(e)}"
