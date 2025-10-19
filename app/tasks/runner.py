# app/tasks/runner.py
import argparse
import pandas as pd
import io
import asyncio
import os
from app.db.session import get_session
from app.db import models
from app.core.logging_config import logger

async def process_excel(file_path: str):
    """
    Procesa el archivo Excel y registra los servicios en la base de datos.
    """
    session_gen = get_session()
    session = await anext(session_gen)

    try:
        if not os.path.exists(file_path):
            logger.error(f"Archivo no encontrado: {file_path}")
            return

        df = pd.read_excel(file_path)
        required_columns = ['name', 'description', 'duration_minutes', 'price']
        missing_columns = [c for c in required_columns if c not in df.columns]
        if missing_columns:
            logger.error(f"Faltan columnas requeridas: {', '.join(missing_columns)}")
            return

        services_created = []
        errors = []

        for index, row in df.iterrows():
            try:
                if pd.isna(row['name']) or pd.isna(row['duration_minutes']) or pd.isna(row['price']):
                    errors.append({
                        "fila": index + 2,
                        "error": "Campos obligatorios vacíos (name, duration_minutes, price)"
                    })
                    continue

                new_service = models.Service(
                    name=str(row['name']).strip(),
                    description=str(row['description']).strip() if not pd.isna(row['description']) else "",
                    duration_minutes=int(row['duration_minutes']),
                    price=float(row['price']),
                    state=True
                )
                session.add(new_service)
                services_created.append(new_service.name)
            except Exception as e:
                errors.append({"fila": index + 2, "error": str(e)})

        await session.commit()
        logger.info(f"{len(services_created)} servicios creados.")
        if errors:
            logger.warning(f"⚠️ {len(errors)} filas con errores.")
        os.remove(file_path)

    except Exception as e:
        await session.rollback()
        logger.error(f"Error procesando Excel: {str(e)}")
    finally:
        await session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa un archivo Excel de servicios.")
    parser.add_argument("--file", required=True, help="Ruta al archivo Excel a procesar")
    args = parser.parse_args()

    asyncio.run(process_excel(args.file))
