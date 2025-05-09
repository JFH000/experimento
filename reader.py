import pika
import json
from Cyph import decrypt_json
from modificador import modificar_mensaje_cifrado

# Configurar conexión a RabbitMQ
RABBITMQ_HOST = 'RABBITMQ_VM_IP'  # <-- Reemplázalo con la IP de tu VM RabbitMQ
QUEUE_NAME = 'examenes'

# Estadísticas
total = 0
válidos = 0
alterados = 0

def callback(ch, method, properties, body):
    global total, válidos, alterados
    total += 1

    mensaje_original = body.decode()
    mensaje_modificado = modificar_mensaje_cifrado(mensaje_original)

    try:
        mensaje_descifrado = decrypt_json(mensaje_modificado)
        válidos += 1
        print(f"[✔] Mensaje válido: {mensaje_descifrado}")
    except ValueError as e:
        alterados += 1
        print(f"[✘] Mensaje alterado: {e}")

    # Confirmar que el mensaje fue procesado
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Conexión y consumo
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

print("[*] Esperando mensajes. Presiona CTRL+C para salir.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n--- Resumen ---")
    print(f"Total de mensajes: {total}")
    print(f"Válidos: {válidos}")
    print(f"Alterados: {alterados}")
    connection.close()
