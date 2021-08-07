# Compilar codigo fuente sass
npm run build && \

# Compilar traducciones
pybabel compile -d app/translations && \

# Iniciar flask server 
python3 run.py
