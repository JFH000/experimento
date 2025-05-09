import json
import base64
import random

def modificar_mensaje_cifrado(mensaje_cifrado_json, probabilidad=0.8):
    """
    Modifica el campo 'data' del mensaje cifrado para invalidar el HMAC.
    """
    mensaje = json.loads(mensaje_cifrado_json)
    data_base64 = mensaje['data']
    hmac_original = mensaje['hmac']

    # Decodificar el contenido cifrado
    encrypted_bytes = bytearray(base64.b64decode(data_base64))

    # Con cierta probabilidad, lo modificamos
    if random.random() < probabilidad:
        num_bytes_a_modificar = random.randint(1, 3)
        for _ in range(num_bytes_a_modificar):
            i = random.randint(0, len(encrypted_bytes) - 1)
            encrypted_bytes[i] ^= random.randint(1, 255)  # Alterar byte

        # Re-codificar a base64
        mensaje['data'] = base64.b64encode(encrypted_bytes).decode()

        # No actualizamos el HMAC, el objetivo es que falle la verificación
        print("[!] Mensaje alterado")

    else:
        print("[=] Mensaje intacto")

    return json.dumps(mensaje)
