from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import json
import os
import datetime
import mimetypes

class DriveUploader:
    def __init__(self):
        self.token_file = 'token.json'
        self.scopes = ['https://www.googleapis.com/auth/drive.file']
        self.service = None

    def dict_to_credentials(self, credentials_dict):
        """
        Convierte un diccionario a objeto Credentials
        """
        if credentials_dict.get('expiry'):
            credentials_dict['expiry'] = datetime.datetime.fromisoformat(credentials_dict['expiry'])
        return Credentials(**credentials_dict)

    def load_credentials(self):
        """
        Cargar credenciales desde el archivo token.json
        """
        if not os.path.exists(self.token_file):
            raise FileNotFoundError(
                "No se encontró el archivo token.json. Por favor, ejecuta primero el script de autenticación."
            )

        try:
            with open(self.token_file, 'r') as token:
                creds_dict = json.load(token)
                return self.dict_to_credentials(creds_dict)
        except Exception as e:
            raise Exception(f"Error al cargar las credenciales: {e}")

    def get_mime_type(self, file_path):
        """
        Obtiene el tipo MIME del archivo
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            return 'application/octet-stream'
        return mime_type

    def create_folder(self, folder_name, parent_id=None):
        """
        Crea una carpeta en Google Drive
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
            
        try:
            file = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            print(f'Carpeta creada con ID: {file.get("id")}')
            return file.get('id')
        except HttpError as error:
            print(f'Error al crear la carpeta: {error}')
            return None

    def upload_file(self, file_path, parent_folder_id=None):
        """
        Sube un archivo a Google Drive
        """
        if not os.path.exists(file_path):
            print(f"El archivo {file_path} no existe.")
            return None

        try:
            file_name = os.path.basename(file_path)
            mime_type = self.get_mime_type(file_path)
            
            file_metadata = {'name': file_name}
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]

            media = MediaFileUpload(
                file_path,
                mimetype=mime_type,
                resumable=True
            )

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, webViewLink'
            ).execute()

            print(f'Archivo subido exitosamente:')
            print(f'Nombre: {file.get("name")}')
            print(f'ID: {file.get("id")}')
            print(f'Tipo MIME: {file.get("mimeType")}')
            print(f'Link: {file.get("webViewLink")}')
            
            return file

        except HttpError as error:
            print(f'Error al subir el archivo: {error}')
            return None

    def initialize_service(self):
        """
        Inicializa el servicio de Google Drive
        """
        try:
            creds = self.load_credentials()
            self.service = build('drive', 'v3', credentials=creds)
            print("Servicio de Google Drive inicializado correctamente")
        except Exception as e:
            raise Exception(f"Error al inicializar el servicio: {e}")

def main():
    """
    Función principal para subir archivos
    """
    uploader = DriveUploader()
    
    try:
        uploader.initialize_service()
        
        while True:
            print("\n=== Menú de Subida de Archivos a Google Drive ===")
            print("1. Subir archivo")
            print("2. Crear carpeta")
            print("3. Subir archivo a una carpeta específica")
            print("4. Salir")
            
            opcion = input("\nSeleccione una opción (1-4): ")
            
            if opcion == '1':
                ruta = input("Ingrese la ruta completa del archivo a subir: ")
                uploader.upload_file(ruta)
                
            elif opcion == '2':
                nombre = input("Ingrese el nombre de la carpeta a crear: ")
                uploader.create_folder(nombre)
                
            elif opcion == '3':
                ruta = input("Ingrese la ruta completa del archivo a subir: ")
                folder_id = input("Ingrese el ID de la carpeta de destino: ")
                uploader.upload_file(ruta, folder_id)
                
            elif opcion == '4':
                print("¡Hasta luego!")
                break
                
            else:
                print("Opción no válida. Por favor, intente nuevamente.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()