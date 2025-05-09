import pika
import json
from Cyph import decrypt_json
from modificador import modificar_mensaje_cifrado, get_modificados

# --- Configuración de conexión ---
RABBITMQ_HOST = '10.128.0.7'  # Reemplázalo con tu IP
RABBITMQ_USER = 'monitoring_user'
RABBITMQ_PASSWORD = 'isis2503'
QUEUE_NAME = 'examenes'

# --- Estadísticas ---
total = 0
validos = 0
alterados = 0

def callback(ch, method, properties, body):
    global total, validos, alterados
    total += 1

    mensaje_original = body.decode()
    mensaje_modificado = modificar_mensaje_cifrado(mensaje_original)

    try:
        contenido = decrypt_json(mensaje_modificado)
        validos += 1
        print(f"[✔] Mensaje válido #{total}: {contenido}")
    except ValueError as e:
        alterados += 1
        print(f"[✘] Mensaje alterado #{total}: {e}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

# --- Conexión ---
try:
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, passive=True)
    print(f"[✔] Conectado a RabbitMQ y cola '{QUEUE_NAME}' verificada.")
except pika.exceptions.ChannelClosedByBroker:
    print(f"[✘] La cola '{QUEUE_NAME}' no existe.")
    exit(1)
except Exception as e:
    print(f"[✘] Error de conexión: {e}")
    exit(1)

# --- Consumir ---
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

print("[*] Esperando mensajes. Presiona CTRL+C para detener.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    modificados_reales = get_modificados()
    print("\n--- RESUMEN ---")
    print(f"Total mensajes:   {total}")
    print(f"Válidos:          {validos}")
    print(f"Alterados (HMAC): {alterados}")
    print(f"Modificados real: {modificados_reales}")
    connection.close()
