# Instalacion
Crear un environment con conda
```
conda create dashboard
```
Activarlo y usar pip para instalar las dependencias. Con suerte, todo ira bien:
```
python3 pip install requirements.txt
```

# Ejecutar
Hay que instalar en el sistema el programa `streamlit` ya que pip no lo instala. Introducir las claves de las APIs en el archivo **config.cfg** y lanzar el comand siguiente:
```
streamlit run src.mydashboard.py
```
Gozar.
