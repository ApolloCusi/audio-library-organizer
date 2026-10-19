import argparse

import shutil

from mutagen import File as AudioFile

from pathlib import Path

def escanear_carpeta(ruta):
    """Recibe la ruta de una carpeta y devuelve una lista de archivos de audio encontrados."""
    extensiones_audio = {".mp3", ".wav", ".aiff", ".flac"}
    carpeta = Path(ruta)

    if not carpeta.exists():
        print(f"Error: la carpeta '{ruta}' no existe")
        return []

    archivos_audio = [archivo for archivo in carpeta.iterdir() if archivo.suffix.lower() in extensiones_audio]
    return archivos_audio

def obtener_info_audio(ruta_archivo):
    """Extrae duración y formato de un archivo de audio."""
    try:
        audio = AudioFile(ruta_archivo)
        if audio is None:
            return None
        return {
            "duracion_segundos": round(audio.info.length, 2),
            "formato": ruta_archivo.suffix
        }

    except Exception as error:
        print(f"No se pudo leer '{ruta_archivo.name}': {error}")
        return None

def crear_carpetas_destino(carpeta_base):
    (carpeta_base / "Cortos").mkdir(exist_ok=True)
    (carpeta_base / "Largos").mkdir(exist_ok=True)


def organizar_por_duracion(archivo, info, carpeta_base, umbral_segundos=120):
    try:
        if info["duracion_segundos"] < umbral_segundos:
            destino = carpeta_base / "Cortos" / archivo.name
        else:
            destino = carpeta_base / "Largos" / archivo.name

        shutil.move(str(archivo), str(destino))
        print(f"Movido: '{archivo.name} → {destino.parent.name}/")
    except FileExistsError:
        print(f"Ya existe '{archivo.name}' en el destino, se omite")
    except Exception as error:
        print(f"Error moviendo {archivo.name}: {error}")



def main():
    parser = argparse.ArgumentParser(description="Organizador de biblioteca de audio")
    parser.add_argument("--carpeta", required=True, help="Ruta de la carpeta a organizar")
    parser.add_argument("--umbral", type=int, default=120, help="Segundos para considerar un audio 'corto'")
    args = parser.parse_args()

    carpeta = Path(args.carpeta)
    archivos = escanear_carpeta(args.carpeta)
    crear_carpetas_destino(carpeta)

    for archivo in archivos:
        info = obtener_info_audio(archivo)
        if info:
            organizar_por_duracion(archivo, info, carpeta, args.umbral)

if __name__ == "__main__":
    main()