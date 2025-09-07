from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config

router = APIRouter()

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/produtos")


def listar_produtos():
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM produtos ORDER BY id")).fetchall()
        return [{"id": row.id, 
                 "nome": row.nome, 
                 "medida": row.medida, 
                 "qtd_disponivel": row.qtd_disponivel,
                 "qtd_minima": row.qtd_minima, 
                 "categoria_id": row.categoria_id,
                 "status": row.status
                 } for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categorias: {str(e)}")
    finally:
        db.close()

