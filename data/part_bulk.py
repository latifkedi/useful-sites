# -*- coding: utf-8 -*-
"""Toplu (bulk) intake yükleyicisi.

Kaynak repolardan gelen, açıklaması olan ama tek tek part dosyasına yazmanın
çok uzun süreceği bağlantılar data/bulk_notes.json'da tutulur; her kayıt
{u,n,t,tr,en,c,s} = url, ad, etiketler, TR, EN, kategori, kaynak.
"""
import io
import os
import json


def load(add):
    p = os.path.join(os.path.dirname(__file__), 'bulk_notes.json')
    if not os.path.exists(p):
        return
    for r in json.load(io.open(p, encoding='utf-8')):
        add(r['u'], r['n'], r['t'], r['tr'], r['en'], r['c'], r['s'])
