import pika
import random
from Cyph import encrypt_json  # Usamos tu módulo

# Configuración de RabbitMQ
RABBITMQ_HOST = 'RABBITMQ_VM_IP'  # <-- Reemplázalo con la IP de tu VM RabbitMQ
QUEUE_NAME = 'examenes'

# Conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Crear la cola si no existe
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Generar datos ficticios
def generar_examen(i):
    return {
        "paciente_id": f"pac_{random.randint(1000, 9999)}",
        "doctor_id": f"doc_{random.randint(100, 999)}",
        "url_examen": f"https://examensalud.com/resultados/{i}.pdf"
    }

# Enviar mensajes cifrados
for i in range(100):
    examen = generar_examen(i)
    mensaje_cifrado = encrypt_json(examen)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=mensaje_cifrado.encode(),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[x] Enviado mensaje cifrado #{i+1}")

connection.close()
