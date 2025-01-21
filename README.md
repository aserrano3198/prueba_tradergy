# Deployment

Para ejecutar la aplicación hay que usar el siguiente comando:

`streamlit run app.py`

Además, se han añadido dos scripts de python que usan el API REST de Esios para descargar datos:

- **get_indicators.py**: usa el endpoint /indicators para traerse todos los indicadores y los presenta como una lista. Con este script he sacado los indicadores que tenía que usar para el segundo script
- **download_data.py**: usa el endpoint /indicators/{indicator} para traerse los datos de cada uno de los indicadores pedidos y los guarda en el archivo precios_spot.csv después de eliminar columnas innecesarias y ordenarlos 

# Predicción futura del precio de la electricidad
A continuación voy a dar respuestas para la cuestión de como atacaría un problema de predicción del precio diario de la electricidad
## **1. Variables Relevantes**

- **Precios Históricos**: Los precios previos en el mercado eléctrico, ya que suelen ser indicadores importantes para los precios futuros. También el precio histórico medio del día de la semana y mes en el que nos encontramos.
- **Demanda Eléctrica**: La cantidad de energía consumida por los usuarios en los últimos días nos puede ayudar a hacer una predicción de la demanda eléctrica futura.
- **Condiciones Meteorológicas**: Factores como la temperatura, la velocidad del viento y la radiación solar que influyen directamente en la demanda y en la oferta (especialmente las energías renovables).
- **Noticias de la red eléctrica**: Noticias sobre paros o cualquier evento inesperado que pueda alterar la producción o demanda de energía.

## **2. Proceso de Adquisición, Limpieza y Almacenamiento de Datos**

Posibles fuentes de datos:

- **Precios Históricos**: Accesibles a través de APIs como ESIOS.
- **Datos Meteorológicos**: Se pueden obtener a través de la API de AEMET o investigar otras APIs más especificas que den más informacion de las zonas de interés.
- **Demanda y Oferta**: Datos de OMIE y de REE.
- **Web Scraping de Noticias**: Buscando datos clave y filtrando por noticias del sector energía.

Para limpiar estos datos hay que normalizarlos antes de añadirlos a las BBDD. Para ello se pueden añadir valores faltantes o eliminar valores erroneos y hacer que haya uniformidad en los formatos de las columnas. 

También seria conveniente buscar posibles excesos o falta de datos de algún tipo y corregirlos para que al procesarlos no haya errores de sesgo.

Una vez tratados los datos pueden ser alamacenados en una BBDD en servidores alamcenados en la nube como AWS S3

## **3. Modelo de Predicción**

Una vez que tenemos los datos almacenados, pongamos que en una BBDD de AWS S3, podríamos usar una de las siguientes opciones: 

- **Amazon SageMaker**: Herramienta que facilita el entrenamiento y la implementación de foundational models. Podemos usar SageMaker para crear nuestro propio modelo predictivo y mejorarlo con el tiempo.
- **Amazon Forecast**: Este servicio está especializado en la predicción de series temporales. Puede darnos mejores resultados a corto plazo, pero a largo plazo siempre será mejor entrenar nuestro propio modelo.


## **4. Evaluación de Resultados**

Evaluaría los resultados con los propios datos que tenemos extraidos de fuentes reales.

Usaría un 80% de los datos extraidos para entrenar al modelo y el 20% restante los guardaría para hacer testing automático del modelo y poder evaluar su precisión generando nuevos datos.

## **5. Almacenamiento y Despliegue de Predicciones**

Una vez que el modelo fuese fiable automatizaría las predicciones y las almacenaría en una base de datos. 

Para acceder a las predicciones se podría crear una API REST, como la que se usa para extraer los datos reales de precios históricos.

Por último, para ayudar a la visualización de dichas predicciones se podría usar un entorno web amigable como el que da Streamlit.
