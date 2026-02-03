import serial
import sys
import os
import time
from pathlib import Path

def encontrar_puerto_arduino():
    """Encuentra automáticamente el puerto del Arduino"""
    import serial.tools.list_ports
    
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'Arduino' in port.description or 'USB' in port.description or '':
            return port.device
    return None

def enviar_jpg(archivo_jpg, puerto=None, baudrate=115200):
    """Envía un JPG al Arduino por Serial"""
    
    # Verificar archivo
    archivo = Path(archivo_jpg)
    if not archivo.exists():
        print(f"❌ ERROR: Archivo '{archivo_jpg}' no existe")
        return False
    
    # Obtener tamaño
    tamano = archivo.stat().st_size
    print(f"📁 Archivo: {archivo.name}")
    print(f"📊 Tamaño: {tamano:,} bytes ({tamano/1024:.1f} KB)")
    
    # Encontrar puerto automáticamente si no se especifica
    if not puerto:
        puerto = encontrar_puerto_arduino()
        if not puerto:
            print("❌ No se encontró Arduino conectado")
            print("   Conecta el Arduino y verifica:")
            print("   - Cable USB")
            print("   - Driver instalado")
            return False
    
    print(f"🔌 Puerto: {puerto}")
    
    try:
        # Conectar al Arduino
        print("🔄 Conectando...")
        ser = serial.Serial(puerto, baudrate, timeout=5)
        time.sleep(2)  # Esperar que Arduino se inicialice
        
        # Leer mensaje inicial del Arduino
        print("📡 Esperando Arduino...")
        time.sleep(1)
        while ser.in_waiting:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea:
                print(f"   ARDUINO: {linea}")
        
        # Enviar comando para comenzar
        print("\n▶️  Iniciando transmisión...")
        ser.write(b'S')  # Comando para comenzar
        
        # Esperar confirmación
        time.sleep(1)
        
        # Enviar tamaño del archivo (4 bytes big-endian)
        print("📤 Enviando tamaño del archivo...")
        ser.write(tamano.to_bytes(4, 'big'))
        time.sleep(0.1)
        
        # Leer y enviar el archivo en bloques
        print("🚀 Transmitiendo datos...")
        bytes_enviados = 0
        bloque_size = 512  # 512 bytes por bloque
        
        with open(archivo, 'rb') as f:
            while True:
                bloque = f.read(bloque_size)
                if not bloque:
                    break
                
                # Enviar bloque
                ser.write(bloque)
                bytes_enviados += len(bloque)
                
                # Mostrar progreso
                porcentaje = (bytes_enviados / tamano) * 100
                barra = '█' * int(porcentaje / 2) + '░' * (50 - int(porcentaje / 2))
                print(f"\r   [{barra}] {porcentaje:.1f}% ({bytes_enviados:,}/{tamano:,} bytes)", end='')
        
        print(f"\n✅ Archivo enviado: {bytes_enviados:,} bytes")
        
        # Esperar resultados del Arduino
        print("\n⏳ Esperando resultados de transmisión...")
        time.sleep(2)
        
        # Leer toda la respuesta del Arduino
        inicio = time.time()
        while time.time() - inicio < 10:  # 10 segundos máx
            if ser.in_waiting:
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    print(f"   📊 {linea}")
                    if "RESULTADOS" in linea or "Listo" in linea:
                        break
        
        ser.close()
        print("\n🎉 Transmisión completada exitosamente!")
        return True
        
    except serial.SerialException as e:
        print(f"❌ Error Serial: {e}")
        print("   Verifica:")
        print("   1. Arduino conectado")
        print("   2. Monitor Serial del IDE cerrado")
        print("   3. Puerto correcto")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

def main():
    print("=" * 50)
    print("📤 TRANSMISOR JPG -> ARDUINO -> LoRa")
    print("=" * 50)
    
    if len(sys.argv) != 2:
        print("Uso: python enviar_jpg_vscode.py <archivo.jpg>")
        print("Ejemplo: python enviar_jpg_vscode.py foto.jpg")
        
        # Mostrar archivos JPG en directorio actual
        print("\nArchivos JPG disponibles:")
        jpg_files = list(Path('.').glob('*.jpg')) + list(Path('.').glob('*.jpeg'))
        for i, archivo in enumerate(jpg_files, 1):
            tamano = archivo.stat().st_size
            print(f"  {i}. {archivo.name} ({tamano/1024:.1f} KB)")
        
        if jpg_files:
            seleccion = input("\nSelecciona número o ingresa nombre: ").strip()
            if seleccion.isdigit():
                archivo = jpg_files[int(seleccion)-1]
            else:
                archivo = Path(seleccion)
        else:
            return
        
    else:
        archivo = Path(sys.argv[1])
    
    # Ejecutar
    enviar_jpg(archivo)

if __name__ == "__main__":
    main()