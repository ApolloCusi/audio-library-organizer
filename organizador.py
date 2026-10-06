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

if __name__ == "__main__":
    archivos = escanear_carpeta("test audio")

    print(f"Se encontraron {len(archivos)} archivos de audio: ")
    for archivo in archivos:
        print(f" - {archivo.name}")