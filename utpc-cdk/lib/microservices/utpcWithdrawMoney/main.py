import json, os
import mysql.connector

# Obtener variables de entorno para la conexión a la base de datos

ENV_HOST_MYSQL = os.getenv("ENV_HOST_MYSQL")
ENV_USER_MYSQL = os.getenv("ENV_USER_MYSQL")
ENV_PASSWORD_MYSQL = os.getenv("ENV_PASSWORD_MYSQL")
ENV_DATABASE_MYSQL = os.getenv("ENV_DATABASE_MYSQL")
ENV_PORT_MYSQL = os.getenv("ENV_PORT_MYSQL")

# Encabezados de respuesta para CORS
headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
    }
# Función para realizar un retiro de dinero
def withdrawMoney( idTarjetNumber, tipoDesposito, monto):
  try:
    conn = mysql.connector.connect(
      host=ENV_HOST_MYSQL,
      user=ENV_USER_MYSQL,
      password=ENV_PASSWORD_MYSQL,
      database=ENV_DATABASE_MYSQL,
      port=ENV_PORT_MYSQL
    )  
    cursor = conn.cursor()
 
 # Insertar registro de transacción
 
    cursor.execute(f"""
      INSERT INTO Transaccion (tipo, monto, idCuenta)
      VALUES ('{tipoDesposito}', {monto}, {idTarjetNumber});     
    """)
 # Actualizar saldo de la cuenta bancaria
    cursor.execute(f"""
      UPDATE CuentaBancaria
      SET saldo = saldo - {monto}
      WHERE id = '{idTarjetNumber}';
    """)

    conn.commit()
    print(f"Key updated successfully for idTarjetNumber: {idTarjetNumber}")

  except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

  finally:
    if 'conn' in locals() and conn.is_connected():
      cursor.close()
      conn.close()
      print("MySQL connection is closed")

# Función Lambda principal
def lambda_handler(event, context):
  try:
    print(f"Event: {event} ")
    print(f"Context: {context}")
    body = event['body']
    body_dict = json.loads(body)
    print(f"body_dict: {body_dict}  [lambda_handler]")

    idTarjetNumber = body_dict['idTarjetNumber']
    tipoDesposito = body_dict['tipoDesposito']
    monto = body_dict['monto']

    if tipoDesposito == 'Retiro':
      withdrawMoney(idTarjetNumber, tipoDesposito, monto)

      return {
          "statusCode": 200,
          "headers": headers,
          "body": json.dumps({"message": "Success"})
      }

    else:
      return {
          "statusCode": 200,
          "headers": headers,
          "body": json.dumps({"message": "No es un retiro de dinero"})
      }
  except Exception as e:
    print(f"Error [lambda_handler]: {e}")
    return {
        "statusCode": 500,
        "headers": headers,
        "body": json.dumps({"message": "Error"})
    }