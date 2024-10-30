from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.colab import files
import json
import os
import datetime

class DriveAuthenticator:
    def __init__(self):
        self.token_file = 'token.json'
        self.credentials_file = 'credentials.json'
        self.scopes = ['https://www.googleapis.com/auth/drive']

    def create_and_upload_credentials(self):
        """Instrucciones para crear y subir el archivo de credenciales."""
        print("Para obtener el archivo credentials.json:")
        print("1. Ve a https://console.cloud.google.com")
        print("2. Crea un nuevo proyecto o selecciona uno existente")
        print("3. Habilita la API de Google Drive")
        print("4. En 'Credenciales', crea credenciales OAuth 2.0")
        print("5. Descarga el archivo JSON de credenciales")
        print("\nAhora, sube tu archivo credentials.json:")
        uploaded = files.upload()
        return next(iter(uploaded))

    def load_credentials(self):
        """Cargar credenciales guardadas si existen."""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as token:
                creds_dict = json.load(token)
                creds_dict['expiry'] = datetime.datetime.fromisoformat(creds_dict['expiry'])
                return Credentials(**creds_dict)
        return None

    def save_credentials(self, creds):
        """Guardar credenciales para uso futuro."""
        creds_dict = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes,
            'expiry': creds.expiry.isoformat() if creds.expiry else None
        }
        with open(self.token_file, 'w') as token:
            json.dump(creds_dict, token, indent=2)
        print("\nCredenciales guardadas exitosamente!")

    def authenticate_drive(self):
        """Autenticar y crear servicio de Drive."""
        creds = self.load_credentials()
        if creds and creds.valid:
            print("Usando credenciales guardadas previamente.")
            return build('drive', 'v3', credentials=creds)

        # Si no hay credenciales guardadas, pedir que suban el archivo
        if not os.path.exists(self.credentials_file):
            self.create_and_upload_credentials()

        # Crear el flujo de OAuth
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.scopes,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        )

        # Generar URL de autorización
        auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
        print("\n1. Abre este link en una nueva pestaña y selecciona la cuenta de Google Drive que deseas usar:")
        print(auth_url)
        print("\n2. Después de autorizar, copia el código que te muestra Google y pégalo aquí:")
        
        auth_code = input('Ingresa el código de autorización: ')
        flow.fetch_token(code=auth_code)
        self.save_credentials(flow.credentials)
        
        return build('drive', 'v3', credentials=flow.credentials)

def main():
    """Función principal para autenticar y crear el token."""
    print("=== Acceso a Google Drive con Autenticación Persistente ===")
    authenticator = DriveAuthenticator()
    service = authenticator.authenticate_drive()
    print("Autenticación completada con éxito. Servicio de Google Drive está disponible.")

if __name__ == '__main__':
    main()
