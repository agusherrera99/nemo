# nemo
CLI Task Manager

## Descripción

**nemo** es una aplicación de línea de comandos para gestionar tareas de manera sencilla y rápida desde la terminal. Permite agregar, listar, actualizar y eliminar tareas, cada una con título, descripción, fecha límite estimada, estado y pin destacado.

## Características principales

- **Agregar tareas** con título, descripción y fecha límite estimada.
- **Listar tareas** mostrando estado, pin y fecha límite.
- **Actualizar tareas** (título, descripción, estado, fecha límite y pin).
- **Eliminar tareas** individuales o todas a la vez.
- **Colores en la terminal** para facilitar la visualización de estados y prioridades.

## Uso básico

```bash
# Listar tareas
nemo list

# Agregar una tarea
nemo add -t "Título" -d "Descripción" --et 5

# Eliminar una tarea por UUID
nemo delete -u "uuid"

# Eliminar todas las tareas
nemo delete --all

# Actualizar el título de una tarea
nemo update -u "uuid" -t "Nuevo título"
```

## Instalación

Clona el repositorio y ejecuta el programa con Python 3:

```bash
git clone https://github.com/tuusuario/nemo.git
cd nemo
python3 src/main.py [comando]
```

## Requisitos

- Python 3.10 o superior

## Licencia

Este proyecto está bajo la licencia MIT.