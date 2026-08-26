# -*- coding: utf-8 -*-
"""Baslangic noktalari.

Arastirmada dizinlerin en buyuk eksigi "kalite ayrimi yok" olarak cikti:
598 kaydin hepsi esit gorununce yeni gelen nereden baslayacagini bilemiyor.
Two or three entries per category, marked as where someone new to the
area should go first. Not "the best" -- "start here".
"""

PICKS = {
    # --- ogrenme
    'https://github.com/ossu/computer-science',                                      # OSSU Computer Science
    'https://pll.harvard.edu/course/cs50-introduction-computer-science',             # CS50
    'https://roadmap.sh/linux',                                                      # roadmap.sh · Linux
    # --- pratik
    'https://exercism.org/',                                                         # Exercism
    'https://leetcode.com/',                                                         # LeetCode
    'https://learngitbranching.js.org/',                                             # Learn Git Branching
    # --- diller
    'https://cppreference.com/',                                                     # cppreference
    'https://go.dev/tour/welcome/1',                                                 # A Tour of Go
    'https://python.yazbel.com/',                                                    # Yazbel Python Belgeleri
    # --- web
    'https://developer.mozilla.org/en-US/',                                          # MDN Web Docs
    'https://javascript.info/',                                                      # The Modern JavaScript Tutorial
    'https://css-tricks.com/',                                                       # CSS-Tricks
    # --- backend
    'https://github.com/donnemartin/system-design-primer',                           # System Design Primer
    'https://fastapi.tiangolo.com/',                                                 # FastAPI
    'https://refactoring.guru/',                                                     # Refactoring Guru
    # --- mobil
    'https://docs.flutter.dev/learn',                                                # Flutter
    'https://docs.expo.dev/',                                                        # Expo
    # --- veritabani
    'https://neon.com/postgresql/tutorial',                                          # PostgreSQL Tutorial
    'https://www.youtube.com/watch?v=pPqazMTzNOM',                                   # Veritabanları Derinlemesine
    # --- devops
    'https://git-scm.com/book/tr/v2',                                                # Pro Git (Türkçe)
    'https://nginx.org/en/docs/',                                                    # nginx
    'https://grafana.com/',                                                          # Grafana
    # --- ag
    'https://www.wireshark.org/#download',                                           # Wireshark
    'https://www.netacad.com/',                                                      # Cisco Networking Academy
    'https://labex.io/linuxjourney',                                                 # Linux Journey
    # --- guvenlik
    'https://tryhackme.com/',                                                        # TryHackMe
    'https://www.hackthebox.com/',                                                   # Hack The Box
    'https://overthewire.org/wargames/',                                             # OverTheWire Wargames
    # --- veri
    'https://www.kaggle.com/',                                                       # Kaggle
    'https://github.com/rasbt/LLMs-from-scratch',                                    # LLMs from Scratch
    'https://github.com/microsoft/Data-Science-For-Beginners/tree/main',             # Data Science for Beginners
    # --- yz_model
    'https://huggingface.co/',                                                       # Hugging Face
    'https://ollama.com/',                                                           # Ollama
    'https://www.perplexity.ai/',                                                    # Perplexity
    # --- yz_altyapi
    'https://modelcontextprotocol.io/',                                              # Model Context Protocol
    'https://www.langchain.com/langgraph',                                           # LangGraph
    'https://langfuse.com/',                                                         # Langfuse
    # --- yz_arac
    'https://cursor.com/',                                                           # Cursor
    'https://aider.chat/',                                                           # Aider
    'https://elicit.com/',                                                           # Elicit
    # --- donanim
    'https://www.onshape.com/en/',                                                   # Onshape
    'https://openipc.org/',                                                          # OpenIPC
    'https://www.mcmaster.com/',                                                     # McMaster-Carr
    # --- gozluk
    'https://github.com/Mentra-Community/MentraOS',                                  # MentraOS
    'https://github.com/Mentra-Community/OpenSourceSmartGlasses',                    # Open Source Smart Glasses
    'https://www.evenrealities.com/smart-glasses',                                   # Even Realities G2
    # --- kuantum
    'https://quantum.cloud.ibm.com/docs/en/guides',                                  # IBM Quantum
    'https://learn.microsoft.com/en-us/azure/quantum/install-overview-qdk',          # Q# Geliştirme Kiti Kurulumu
    # --- araclar
    'https://excalidraw.com/',                                                       # Excalidraw
    'https://regex101.com/',                                                         # regex101
    'https://godbolt.org/',                                                          # Compiler Explorer
    # --- referans
    'https://devdocs.io/',                                                           # DevDocs
    'https://learnxinyminutes.com/',                                                 # Learn X in Y Minutes
    'https://free-for.dev/#/',                                                       # Free for Developers
    # --- bilim
    'https://arxiv.org/',                                                            # arXiv
    'https://www.semanticscholar.org/',                                              # Semantic Scholar
    'https://www.connectedpapers.com/',                                              # Connected Papers
    # --- yeni kategoriler ve son alimlar
    # --- barindirma
    'https://syncthing.net/',                                                        # Syncthing
    'https://immich.app/',                                                           # Immich
    'https://nextcloud.com/',                                                        # Nextcloud
    # --- medya
    'https://www.blender.org/',                                                      # Blender
    'https://squoosh.app/',                                                          # Squoosh
    'https://www.photopea.com/',                                                     # Photopea
    # --- yz_uretim
    'https://github.com/AUTOMATIC1111/stable-diffusion-webui',                       # Stable Diffusion WebUI
    'https://www.comfy.org/',                                                        # ComfyUI
    # --- yz_rag
    'https://github.com/pgvector/pgvector',                                          # pgvector
    'https://www.llamaindex.ai/',                                                    # LlamaIndex
    # --- guvenlik
    'https://haveibeenpwned.com/',                                                   # Have I Been Pwned
    'https://mullvad.net/en',                                                        # Mullvad VPN
    # --- ag
    'https://tailscale.com/',                                                        # Tailscale
    # --- web
    'https://caniuse.com/',                                                          # Can I Use
    # --- devops
    'https://www.shellcheck.net/',                                                   # ShellCheck
    # --- mobil
    'https://godotengine.org/',                                                      # Godot
    # --- donanim
    'https://wokwi.com/',                                                            # Wokwi
    'https://www.kicad.org/',                                                        # KiCad
    # --- araclar
    'https://it-tools.tech/',                                                        # IT Tools
    # --- referans
    'https://ohshitgit.com/',                                                        # Oh Shit, Git!?!
    'https://teachyourselfcs.com/',                                                  # Teach Yourself CS
    # --- sertifika yol haritasi alimi
    'https://pauljerimy.com/security-certification-roadmap/',                        # Security Certification Roadmap
    'https://www.offsec.com/',                                                       # OffSec
    'https://www.comptia.org/',                                                      # CompTIA
    'https://www.giac.org/',                                                         # GIAC
}


def is_pick(url):
    return url in PICKS
