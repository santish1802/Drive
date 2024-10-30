# Proyecto de Google Drive API

Este proyecto utiliza la API de Google Drive para realizar operaciones específicas. A continuación, se detallan los pasos para configurar y ejecutar el proyecto en Google Colab.

## Requisitos

Asegúrate de que tienes acceso a Google Colab y que has montado tu Google Drive para poder acceder a los archivos.

## Instalación de Dependencias

Para instalar las dependencias necesarias, ejecuta el siguiente comando en una celda de código en Google Colab:

```python
!pip install -q -r /content/Drive/requerimientos.txt

Este comando instalará todas las bibliotecas necesarias listadas en el archivo `requerimientos.txt`. Asegúrate de que este archivo esté presente en la ubicación correcta en tu Google Drive.

## Carga del Archivo de Credenciales

1. **Descargar `credentials.json`:** Si aún no tienes el archivo `credentials.json`, descárgalo desde la consola de desarrolladores de Google. Asegúrate de que las credenciales tengan acceso a la API de Google Drive.

2. **Subir `credentials.json` manualmente:**
   - Ejecuta el siguiente código en una celda de código en Google Colab:

   ```python
   from google.colab import files

   uploaded = files.upload()
   ```

   - Esto abrirá un cuadro de diálogo que te permitirá seleccionar y cargar tu archivo `credentials.json` desde tu computadora.

## Ejecución del Proyecto

Después de haber instalado las dependencias y cargado el archivo de credenciales, puedes ejecutar los scripts de tu proyecto. Ejecuta los siguientes comandos en celdas de código en Google Colab:

```python
!python /content/Drive/Inicio.py
```

```python
!python /content/Drive/tareas.py
```

Asegúrate de que ambos scripts (`Inicio.py` y `tareas.py`) estén ubicados correctamente en tu Google Drive.

## Notas Adicionales

- Asegúrate de que el archivo `requerimientos.txt` contenga todas las bibliotecas necesarias para tu proyecto.
- Si encuentras errores durante la ejecución, revisa los mensajes de error para solucionar problemas específicos.
```
