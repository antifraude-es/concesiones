# Diseño e Implementación de la Herramienta

Este documento describe las ideas clave y las decisiones tomadas durante la sesión de brainstorming inicial para la creación de la herramienta de descarga de la base de datos de subvenciones.

## Resumen de la Sesión de Brainstorming

- La herramienta está diseñada para descargar la base de datos de subvenciones, que se encuentra detrás de una API lenta con páginas de 200 entradas cada una.
- Se utilizará Python para la implementación.
- Proceso de descarga se ejecutará en un proceso de forma secuencial.
- La descarga se dividirá en lotes basados en días individuales para evitar errores en la API y simplificar el proceso.
- Los datos se organizarán en carpetas separadas para cada año, con hasta 366 archivos JSON en cada carpeta.
- Al iniciar un proceso, se comprobará si ya existe la fecha y, en caso contrario, se creará inmediatamente, evitando así descargas duplicadas.
- Se pueden dividir las descargas en lotes más grandes basados en meses para reducir la probabilidad de conflictos entre otros procesos que intenten descargar los mismos datos.
- Los datos descargados para cada día se mantendrán en memoria y sólo se escribirán en disco una vez que se haya descargado toda la información del día, evitando así la creación de archivos parcialmente descargados y conflictos de escritura.
- Se mostrará el estado del progreso al usuario, ya sea en la salida del terminal de cada proceso o mediante un archivo de estado global.
- Se utilizará un archivo de registro para registrar el progreso y los procesos en curso, facilitando así la gestión del proceso de descarga y garantizando que cada tarea sea realizada por un solo proceso a la vez.

## Consideraciones Adicionales

- Asegúrate de que la máquina en la que se ejecutará el programa tenga suficiente memoria para manejar la cantidad de datos que se descargarán.
- Considera implementar mecanismos de control de errores y reintentos en caso de que alguna de las solicitudes falle.
- Asegúrate de cumplir con las políticas y términos legales para descargar, utilizar y reutilizar los datos extraídos con esta herramienta.

