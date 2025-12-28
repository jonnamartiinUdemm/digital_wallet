# seed.py
from sqlmodel import Session, select
from database import engine, create_all_tables # Asegurate de tener create_all_tables en database.py o importarlo de main
from models import Categoria, Movimiento
from datetime import datetime, timedelta
import random

def sembrar_datos():
    print("🌱 Iniciando la siembra de datos...")
    
    with Session(engine) as session:
        # 1. Limpieza (Opcional): Borramos datos viejos para empezar limpio
        # Nota: Borramos movimientos primero por la clave foránea
        print("🧹 Limpiando base de datos antigua...")
        session.exec(select(Movimiento)).all()
        # En SQLModel borrar todo requiere iterar o usar sentencias delete directas.
        # Para simplificar este script, asumimos que agregamos datos, no borramos.
        # Si quieres borrar, tendrías que eliminar el archivo .db manualmente antes.

        # 2. Verificar si ya hay categorías
        categorias_existentes = session.exec(select(Categoria)).all()
        
        if not categorias_existentes:
            print("📦 Creando categorías...")
            lista_categorias = [
                Categoria(nombre="Comida", descripcion="Supermercado y restaurantes"),
                Categoria(nombre="Transporte", descripcion="Uber, Taxi, Nafta"),
                Categoria(nombre="Vivienda", descripcion="Alquiler y servicios"),
                Categoria(nombre="Ocio", descripcion="Salidas, cine y juegos"),
                Categoria(nombre="Ingresos", descripcion="Sueldo y Freelo")
            ]
            session.add_all(lista_categorias)
            session.commit()
            
            # Recargamos para obtener los IDs
            for cat in lista_categorias:
                session.refresh(cat)
            categorias_existentes = lista_categorias
        else:
            print("✅ Las categorías ya existían.")

        # 3. Crear Movimientos Aleatorios
        print("💸 Generando 20 movimientos aleatorios...")
        
        conceptos_gastos = ["Compra Super", "Cena afuera", "Uber al centro", "Factura Luz", "Netflix", "Cerveza"]
        conceptos_ingresos = ["Sueldo", "Venta de mueble", "Trabajo Freelance", "Regalo"]

        movimientos = []
        for _ in range(20):
            # Elegir una categoría al azar
            cat_random = random.choice(categorias_existentes)
            
            # Definir tipo y concepto según la categoría
            if cat_random.nombre == "Ingresos":
                tipo = "ingreso"
                concepto = random.choice(conceptos_ingresos)
                monto = random.randint(50000, 200000)
            else:
                tipo = "egreso"
                concepto = random.choice(conceptos_gastos)
                monto = random.randint(1000, 25000)

            # Generar fecha aleatoria en los últimos 60 días
            dias_atras = random.randint(0, 60)
            fecha_random = datetime.now() - timedelta(days=dias_atras)

            # Crear el objeto
            mov = Movimiento(
                monto=float(monto),
                tipo=tipo,
                concepto=concepto,
                date=fecha_random, # Asegúrate que tu campo en models se llame 'date' o 'fecha'
                categoria_id=cat_random.id
            )
            movimientos.append(mov)

        session.add_all(movimientos)
        session.commit()
        print(f"✅ ¡Éxito! Se han creado {len(movimientos)} movimientos nuevos.")

if __name__ == "__main__":
    # Asegurarnos de que las tablas existan antes de insertar
    # (Esto usualmente corre en main.py, pero por seguridad lo invocamos si tienes la función)
    # SQLModel.metadata.create_all(engine) 
    sembrar_datos()