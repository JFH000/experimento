import json
import base64
import random

# Contador interno
_modificados = 0

def modificar_mensaje_cifrado(mensaje_cifrado_json, probabilidad=0.8):
    """
    Modifica el campo 'data' del mensaje cifrado para invalidar el HMAC.
    """
    global _modificados

    mensaje = json.loads(mensaje_cifrado_json)
    data_base64 = mensaje['data']

    # Decodificar el contenido cifrado
    encrypted_bytes = bytearray(base64.b64decode(data_base64))

    # Con cierta probabilidad, lo modificamos
    if random.random() < probabilidad:
        num_bytes = random.randint(1, 3)
        for _ in range(num_bytes):
            i = random.randint(0, len(encrypted_bytes) - 1)
            encrypted_bytes[i] ^= random.randint(1, 255)  # Modificación aleatoria

        # Re-codificar y mantener HMAC original (fallará)
        mensaje['data'] = base64.b64encode(encrypted_bytes).decode()
        _modificados += 1
        print("[!] Mensaje alterado")
    else:
        print("[=] Mensaje intacto")

    return json.dumps(mensaje)

def get_modificados():
    """
    Retorna la cantidad de mensajes efectivamente modificados.
    """
    return _modificados
