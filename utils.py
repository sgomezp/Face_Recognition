import os
import time

def rename_files(directory_path):
    try:
        # Obtiene el nombre del directorio
        directory_name = os.path.basename(directory_path)

        # Recorre cada archivo en el directorio
        for index, filename in enumerate(os.listdir(directory_path)):
            if filename.endswith('.jpg'):
                # Construye el nuevo nombre del archivo con un sufijo único
                timestamp = int(time.time())
                new_filename = f"{directory_name}_{timestamp}_{index + 1}.jpg"

                # Ruta completa de los archivos antiguos y nuevos
                old_filepath = os.path.join(directory_path, filename)
                new_filepath = os.path.join(directory_path, new_filename)

                # Renombra el archivo
                os.rename(old_filepath, new_filepath)

                print(f"Renombrado: {old_filepath} -> {new_filepath}")

    except Exception as e:
        print(f"Error al renombrar archivos: {str(e)}")

# Directorio base
root_directory = "data"

# Ruta del directorio que deseas procesar
directory_to_rename = os.path.join(root_directory, "sandra")

# Llama a la función para renombrar todos los archivos en el directorio
rename_files(directory_to_rename)
