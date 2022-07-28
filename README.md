# Analytics_Alkemy

## Instrucciones para la ejecución:

1. Clonar repositorio:
```
git clone https://github.com/andresg0896/Analytics_Alkemy
```

2. Crear entorno virtual:

    -Para Windows:
      ```
    python3 -m venv alkemy
    alkemy\\Scripts\\activate.bat
      ```

    -Para Unix\MacOS:
      ```
    python3 -m venv alkemy
    source alkemy/bin/activate
      ```
3. Instalar dependencias a usar:
```
pip install numpy
pip install pandas
pip install requests
pip install sqlalchemy
pip install psicopg2
```
4. Configurar datos de conexión a base de datos y cambiar URLs de ser necesario en ```DB_URL.py```

5. Ejecutar:
```
python3 union.py
```
6. Revisar logs de ser necesario en:
```
comentarios.log
```

