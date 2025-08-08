#!/usr/bin/env python3
"""
Script simple para iniciar el servidor FastAPI
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI...")
    print("🌐 Servidor disponible en: http://localhost:8000")
    print("📚 Documentación en: http://localhost:8000/docs")
    print("🛑 Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 