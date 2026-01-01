from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from db.models import Usuario, Rol

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

# ✅ Listar todos los usuarios
@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

# ✅ Crear un nuevo usuario
@router.post("/")
def crear_usuario(
    nombre: str,
    apellido: str,
    mail: str,
    cod_rol: int,
    db: Session = Depends(get_db)
):
    # Validar que el rol exista
    rol = db.query(Rol).filter(Rol.id == cod_rol).first()
    if not rol:
        raise HTTPException(status_code=400, detail="Rol no existe")
    
    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        mail=mail,
        cod_rol=cod_rol
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
