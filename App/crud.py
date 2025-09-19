from sqlalchemy.orm import Session
import App.models as models
import App.schemas as schemas
from sqlalchemy.exc import SQLAlchemyError

def create_usuario(db: Session, usuario: schemas.UsuarioBase):
    try:
        db_registro = models.UsuarioModel(
            nome=usuario.nome,
            senha=usuario.senha
        )
        db.add(db_registro)
        db.commit()
        db.refresh(db_registro)
        return db_registro
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_usuario_por_nome(db: Session, nome: str, senha: str):
    return db.query(models.UsuarioModel).filter(models.UsuarioModel.nome == nome, 
                                                models.UsuarioModel.senha == senha).first()