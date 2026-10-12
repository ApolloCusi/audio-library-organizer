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


if __name__ == "__main__":
    archivos = escanear_carpeta("test_audio")

    for archivo in archivos:
        info = obtener_info_audio(archivo)
        if info:
            print(f"{archivo.name}: {info['duracion_segundos']}s ({info['formato']})")


