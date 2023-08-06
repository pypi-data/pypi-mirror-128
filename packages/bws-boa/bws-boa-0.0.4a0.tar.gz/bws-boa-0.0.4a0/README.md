# MS Core

Ms Core


# Instalar / Crear un proyecto

```bash

echo "export PATH=\$PATH:$HOME/.local/bin" >> ~/.bashrc

pip install -U bws-boa


# crear proyecto 

boa init .

```


# Crear un aplicación

```bash
boa add-app <name>

```

# Activar app


Agregar dentro de app.config.INSTALLED_APPS el path del modulo
```python
INSTALLED_APPS = [
    "...",
    "app.nombre_app"
]
```