from modeltranslation.translator import translator, TranslationOptions
from .models import CodeFragment

class EditorTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(CodeFragment, EditorTranslationOptions)
