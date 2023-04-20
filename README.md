# Concesiones BDNS
Concesiones BDNS es un proyecto destinado a descargar de manera eficiente todo el conjuntos de datos sobre concesiones de la Base de Datos Nacional de Subvenciones (BDNS). La base de datos pública de subvenciones es conocida por su lentitud, y la plataforma web presenta desafíos para el análisis de datos. Nuestro objetivo es proporcionar una solución para obtener una copia local de la base de datos completa, permitiendo así un análisis más eficiente y rápido.

## Funcionalidades
 - Descarga asíncrona de datos utilizando múltiples procesos
 - Descarga de datos en lotes basados en día o mes
 - Manejo eficiente de la paginación de la API
 - Almacenamiento organizado de los datos descargados en carpetas separadas por año
 - Seguimiento del progreso a través de archivos de registro (logs)
 - Manejo de errores y mecanismos de reintento

## Aviso legal
Este proyecto está diseñado para facilitar el acceso a los datos públicos de subvenciones de la BDNS. Sin embargo, es responsabilidad de cada usuario asegurarse de cumplir con las políticas y términos legales relacionados con el uso y la reutilización de estos datos. Los autores de este proyecto no se hacen responsables de cualquier mal uso de la herramienta ni del uso de los datos descargados. Por favor, asegúrese de revisar y entender los términos y condiciones del uso disponibles en el [Aviso Legal de la BDNS](https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal) antes de utilizar esta herramienta y los datos extraídos.

## Intrucciones
Para empezar, clona este repositorio y sigue las instrucciones a continuación:

1. Configura un entorno virtual (opcional pero recomendado):
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```
2. Instala las dependencias necesarias:
```
pip install -r requirements.txt
```
3. ~~Configura tus ajustes en el archivo settings.py.~~

4. Ejecuta el script principal para iniciar el proceso de descarga:
```
python main.py
```

mas [información sobre el Diseño](Diseño.md)

## Contribuye
Estamos abiertos a colaboradores para ayudar a mejorar y expandir el proyecto Concesiones BDNS. Si deseas contribuir, sigue estos pasos:

1. Haz un fork de este repositorio.
2. Cree una nueva rama para tu funcionalidad o arreglo de bugs.
3. Desarrolla cambios y agrega test si corresponde.
4. Asegúrate de que tu código siga el estilo de código establecido y pase todas los tests.
5. Envía una solicitud de pull request para su revisión.

Agradecemos tu interés en contribuir al proyecto Concesiones BDNS y esperamos trabajar juntos.

### Equipo
Pásate por el [Discord de Antifraude](https://discord.com/channels/1040903830189125713) para discutir el desarrollo de esta y otras herramientas relacionadas

## Licencia
Este proyecto está licenciado bajo la Licencia MIT.