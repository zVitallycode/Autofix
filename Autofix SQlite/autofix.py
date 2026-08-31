from peewee import *

# Conexión a SQLite
db = SqliteDatabase('autofix.db')

# Clase base para configurar la conexión a la base de datos
class BaseModel(Model):
    class Meta:
        database = db

# Tabla 1: Clientes
class Cliente(BaseModel):
    nombre = CharField(unique=True)
    telefono = CharField()

# Tabla 2: Vehiculos
class Vehiculos(BaseModel):
    placa = CharField()
    marca = CharField()
    modelo = CharField()
    cliente = ForeignKeyField(Cliente, backref='vehiculos')


def iniciar_base_datos():
    db.connect()
    db.create_tables([Cliente, Vehiculos], safe=True)


def registrar_cliente():
    print("\n--- REGISTRAR CLIENTE ---")
    nombre = input("Nombre del cliente: ").strip()

    if not nombre:
        print("❌ El nombre no puede estar vacío.")
        return

    telefono = input("Teléfono del cliente: ").strip()

    if not telefono:
        print("❌ El teléfono no puede estar vacío.")
        return

    try:
        Cliente.create(nombre=nombre, telefono=telefono)
        print(f"✅ Cliente '{nombre}' guardado con éxito.")
    except IntegrityError:
        print(f"❌ El cliente '{nombre}' ya existe.")


def registrar_vehiculo():
    print("\n--- NUEVO VEHICULO ---")

    # Obtenemos los clientes creados
    clientes = Cliente.select()
    if not clientes.exists():
        print("❌ Primero debes agregar al menos un cliente.")
        return

    print("Clientes registrados")
    for cli in clientes:
        print(f"  [{cli.id}] {cli.nombre} - Tel: {cli.telefono}")

    try:
        cli_id = int(input("Ingresa el ID del cliente: "))
        cliente = Cliente.get_by_id(cli_id)

        placa = input("Placa del vehiculo: ").strip()
        modelo = input("Modelo del vehiculo: ").strip()
        marca = input("Marca del vehiculo: ").strip()

        Vehiculos.create(modelo=modelo, marca=marca, placa=placa, cliente=cliente)
        print(f"✅ Vehiculo '{placa}' agregado correctamente.")
    except (ValueError, Cliente.DoesNotExist):
        print("❌ Datos inválidos o cliente no encontrado.")


def ver_vehiculos():
    print("\n--- LISTA DE VEHICULOS ---")
    vehiculos = Vehiculos.select()

    if not vehiculos.exists():
        print("📭 No hay vehiculos registrados.")
        return

    for v in vehiculos:
        print(f"Matricula: {v.placa} | Modelo: {v.modelo} | Marca: {v.marca} | Cliente: {v.cliente.nombre}")


def buscar_vehiculo():
    placa = input("Placa del vehiculo: ").strip()
    try:
        vehiculo = Vehiculos.get(Vehiculos.placa == placa)
        print(f"📭 Vehiculo encontrado: {vehiculo.placa} - {vehiculo.marca} {vehiculo.modelo} (Cliente: {vehiculo.cliente.nombre})")
    except Vehiculos.DoesNotExist:
        print("📭 Vehiculo no encontrado.")


def eliminar_vehiculo():
    placa = input("Placa del vehiculo a eliminar: ").strip()
    try:
        vehiculo = Vehiculos.get(Vehiculos.placa == placa)
        vehiculo.delete_instance()
        print(f"✅ Vehiculo '{placa}' eliminado correctamente.")
    except Vehiculos.DoesNotExist:
        print("📭 Vehiculo no encontrado.")


def menu_principal():
    iniciar_base_datos()

    while True:
        print("\n==============================")
        print("  🛒 MENÚ DE AUTOFIX 🛒")
        print("==============================")
        print("1. Registrar Cliente")
        print("2. Registrar Vehiculo")
        print("3. Ver Lista de Vehiculos")
        print("4. Buscar un Vehiculo")
        print("5. Eliminar un Vehiculo")
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
