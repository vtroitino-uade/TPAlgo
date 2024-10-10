# Roguemon

## Requisitos

- Python 3 instalado en tu sistema.
- `virtualenv` instalado. Si no lo tienes, puedes instalarlo ejecutando:

    ```bash
    pip install virtualenv
    ```

## Configuración del entorno virtual

1. Clona este repositorio en tu máquina local:

    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    ```

2. Navega al directorio del proyecto:

    ```bash
    cd tu-repositorio
    ```

3. Crea un entorno virtual con `virtualenv`:

    ```bash
    virtualenv venv
    ```

4. Activa el entorno virtual:

    - En Linux/Mac:

      ```bash
      source venv/bin/activate
      ```

    - En Windows:

      ```bash
      .\venv\Scripts\activate
      ```

5. Instala las dependencias del proyecto usando el archivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

6. ¡Listo! Ya tienes el entorno virtual configurado y las dependencias instaladas.

## Desactivar el entorno virtual

Cuando termines de trabajar, puedes desactivar el entorno virtual ejecutando:

```bash
deactivate
```
