# -*- coding: utf-8 -*-
# create by yihui 16:44 20/9/11.
from src.plugins.translate.GoogleTranslate import GoogleTranslator


def to_en_by_google(text):
    t = GoogleTranslator()
    r = t.translate('zh', 'en', text)
    return r['definition']
