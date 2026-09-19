# -*- coding: utf-8 -*-
"""Toplu (bulk) intake yükleyicisi.

Kaynak repolardan gelen, açıklamalı ama tek tek part dosyasına yazmak yerine
toplu tutulan bağlantılar data/bulk_notes*.json içinde; her kayıt
{u,n,t,tr,en,c,s} = url, ad, etiketler, TR, EN, kategori, kaynak.
"""
import io
import os
import glob
import json


def load(add):
    d = os.path.dirname(__file__)
    for p in sorted(glob.glob(os.path.join(d, 'bulk_notes*.json'))):
        for r in json.load(io.open(p, encoding='utf-8')):
            add(r['u'], r['n'], r['t'], r['tr'], r['en'], r['c'], r['s'])
