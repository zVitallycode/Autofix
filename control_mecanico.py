
from peewee import *

# 1. Configuración de Base de Datos PostgreSQL (Neon)
db = PostgresqlDatabase(
    'neondb',
    user='neondb_owner',
    password='npg_bjF2oZy7shcW',
    host='ep-falling-art-ay2v242e-pooler.c-5.us-east-2.aws.neon.tech',
    port=5432,
    sslmode='require'
)

# 2. Definición de Modelos
class BaseModel(Model):
    class Meta:
        database = db

class Cliente(BaseModel):
    nombre = CharField()
    telefono = CharField()

class Vehiculo(BaseModel):
    placa = CharField(unique=True)
    marca = CharField()
    modelo = CharField()
    cliente = ForeignKeyField(Cliente, backref='vehiculos')

def iniciar_base_datos():
    db.connect()
    db.create_tables([Cliente, Vehiculo], safe=True)

# 3. Funciones del Sistema
def registrar_cliente():
    print("\n--- REGISTRAR CLIENTE ---")
    nombre = input("Nombre del cliente: ").strip()
    telefono = input("Teléfono del cliente: ").strip()
    
    if not nombre or not telefono:
        print("❌ Todos los campos son obligatorios.")
        return

    try:
        Cliente.create(nombre=nombre, telefono=telefono)
        print(f"✅ Cliente '{nombre}' registrado con éxito.")
    except Exception as e:
        print(f"❌ Ocurrió un error al registrar el cliente: {e}")

def registrar_vehiculo():
    print("\n--- REGISTRAR VEHÍCULO ---")
    clientes = Cliente.select()
    if not clientes.exists():
        print("❌ Primero debes registrar al menos un cliente.")
        return

    print("Clientes disponibles:")
    for c in clientes:
        print(f"  [{c.id}] {c.nombre} - Tel: {c.telefono}")

    try:
        cliente_id = int(input("Ingresa el ID del cliente propietario: "))
        cliente = Cliente.get_by_id(cliente_id)
        
        placa = input("Placa del vehículo: ").strip().upper()
        marca = input("Marca: ").strip()
        modelo = input("Modelo: ").strip()

        if not placa or not marca or not modelo:
            print("❌ Todos los campos del vehículo son obligatorios.")
            return

        Vehiculo.create(placa=placa, marca=marca, modelo=modelo, cliente=cliente)
        print(f"✅ Vehículo con placa '{placa}' registrado correctamente.")
    except (ValueError, DoesNotExist):
        print("❌ Datos inválidos o cliente no encontrado.")
    except IntegrityError:
        print(f"❌ La placa '{placa}' ya se encuentra registrada.")

def ver_vehiculos():
    print("\n--- LISTA DE VEHÍCULOS ---")
    vehiculos = Vehiculo.select()

    if not vehiculos.exists():
        print("📭 No hay vehículos registrados.")
        return

    for v in vehiculos:
        print(f"Placa: {v.placa} | Marca: {v.marca} ({v.modelo}) | Propietario: {v.cliente.nombre}")

def buscar_vehiculo():
    print("\n--- BUSCAR VEHÍCULO POR PLACA ---")
    placa_buscada = input("Ingresa el número de placa a buscar: ").strip().upper()
    
    try:
        vehiculo = Vehiculo.get(Vehiculo.placa == placa_buscada)
        print(f"\n🚗 Vehículo Encontrado:")
        print(f"Placa: {vehiculo.placa} | Marca: {vehiculo.marca} | Modelo: {vehiculo.modelo} | Propietario: {vehiculo.cliente.nombre} (Tel: {vehiculo.cliente.telefono})")
    except DoesNotExist:
        print(f"❌ No se encontró ningún vehículo con la placa '{placa_buscada}'.")

def eliminar_vehiculo():
    print("\n--- ELIMINAR VEHÍCULO ---")
    ver_vehiculos()
    
    placa_eliminar = input("\nIngresa la placa del vehículo a eliminar: ").strip().upper()
    
    try:
        vehiculo = Vehiculo.get(Vehiculo.placa == placa_eliminar)
        vehiculo.delete_instance()
        print(f"🗑️ Vehículo con placa '{placa_eliminar}' eliminado correctamente.")
    except DoesNotExist:
        print("❌ El vehículo con esa placa no existe.")

# 4. Menú Principal y Ejecución
def menu_principal():
    iniciar_base_datos()

    while True:
        print("\n==============================")
        print("  🚗 MENÚ TALLER AUTOFIX 🚗")
        print("==============================")
        print("1. Registrar Cliente")
        print("2. Registrar Vehículo")
        print("3. Ver todos los Vehículos")
        print("4. Buscar Vehículo por número de Placa")
        print("5. Eliminar Vehículo")
        print("6. Salir")
        print("==============================")

        opcion = input("Elige una opción (1-6): ").strip()

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            registrar_vehiculo()
        elif opcion == "3":
            ver_vehiculos()
        elif opcion == "4":
            buscar_vehiculo()
        elif opcion == "5":
            eliminar_vehiculo()
        elif opcion == "6":
            print("\n👋 ¡Hasta luego! Cerrando la aplicación...")
            db.close()
            break
        else:
            print("❌ Opción no válida. Digita un número entre 1 y 6.")

if __name__ == "__main__":
    menu_principal()