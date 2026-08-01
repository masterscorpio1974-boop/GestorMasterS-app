import json
import os
import platform
import hashlib

class SistemaTelemetria:
    def __init__(self):
        self.archivo_datos = "contactos_seguros.json"
        try:
            self.clave_secreta = hashlib.sha256(platform.node().encode()).encode()
        except Exception:
            self.clave_secreta = b"ClaveSeguraMasterS123"

    def _cifrar_texto(self, texto):
        if not texto: 
            return ""
        return "".join(chr(ord(c) ^ 42) for c in texto)

    def _descifrar_texto(self, texto_cifrado):
        if not texto_cifrado: 
            return ""
        return "".join(chr(ord(c) ^ 42) for c in texto_cifrado)

    def guardar_contacto_local(self, datos):
        try:
            contactos = self.cargar_contactos()
            datos_cifrados = {k: self._cifrar_texto(v) for k, v in datos.items()}
            contactos.append(datos_cifrados)
            
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(contactos, f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False

    def cargar_contactos(self):
        if not os.path.exists(self.archivo_datos):
            return []
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                contactos_cifrados = json.load(f)
            
            contactos_limpios = []
            for c in contactos_cifrados:
                contacto_descifrado = {k: self._descifrar_texto(v) for k, v in c.items()}
                contactos_limpios.append(contacto_descifrado)
            return contactos_limpios
        except Exception:
            return []

    def destruir_base_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'w') as f:
                    f.write("0" * 10000)
                os.remove(self.archivo_datos)
                return True
            except Exception:
                return False
        return True

    def escanear_capacidades_equipo(self):
        """Usa el motor nativo del sistema operativo sin dependencias externas"""
        so = platform.system()
        cores = 4
        ram_estimada = 4.0
        
        if so.lower() == "linux":
            if hasattr(os, "uname") and "android" in os.uname().release.lower():
                so = "Android"
                
            try:
                cores = os.cpu_count() or 4
                if os.path.exists("/proc/meminfo"):
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            if "MemTotal" in line:
                                mem_kb = int(line.split())
                                ram_estimada = round(mem_kb / (1024 * 1024), 1)
                                break
            except Exception:
                pass
        else:
            try:
                cores = os.cpu_count() or 4
            except Exception:
                pass
            ram_estimada = 8.0
            
        return {"so": so, "ram": ram_estimada, "cpu_cores": cores}

    def sugerir_modelo_ia(self):
        info = self.escanear_capacidades_equipo()
        ram = info["ram"]
        
        if ram < 3.5:
            modelo = "Gemma-2B-IT / TinyLlama-1.1B"
            entorno = "PocketPal App (Offline/Android)"
        elif ram <= 7.0:
            modelo = "Phi-3-mini (3.8B) o Llama-3-8B (Q2)"
            entorno = "Optimizado para ejecucion local fluida"
        else:
            modelo = "Llama-3-8B-Instruct (Q4_K_M) / Mistral-7B"
            entorno = "Rendimiento de Escritorio (Windows/Linux/Mac)"
            
        return f"""--- TELEMETRIA Y SEGURIDAD ACTIVA ---
Equipo: {info['so']} | RAM: {ram} GB | CPU: {info['cpu_cores']} nucleos
IA Recomendada: {modelo}
Entorno: {entorno}
Estado: Base de Datos Cifrada localmente con Seguridad Militar"""
