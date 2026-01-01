# routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from db.session import get_db
from db.models import Usuario, Rol

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

# --------------------
# Pydantic Models
# --------------------
class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    mail: str
    cod_rol: int

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    mail: Optional[str] = None
    cod_rol: Optional[int] = None

# --------------------
# LISTAR USUARIOS
# --------------------
@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

# --------------------
# CREAR USUARIO (recibe JSON)
# --------------------
@router.post("/")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Validar que exista el rol
    rol = db.query(Rol).filter(Rol.id == usuario.cod_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    # Validar que el mail no exista
    existing = db.query(Usuario).filter(Usuario.mail == usuario.mail).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# --------------------
# OBTENER USUARIO POR ID
# --------------------
@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# --------------------
# ACTUALIZAR USUARIO (recibe JSON)
# --------------------
@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    u = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.cod_rol:
        rol = db.query(Rol).filter(Rol.id == usuario.cod_rol).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        u.cod_rol = usuario.cod_rol

    if usuario.nombre:
        u.nombre = usuario.nombre
    if usuario.apellido:
        u.apellido = usuario.apellido
    if usuario.mail:
        existing = db.query(Usuario).filter(Usuario.mail == usuario.mail, Usuario.id != usuario_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        u.mail = usuario.mail

    db.commit()
    db.refresh(u)
    return u

# --------------------
# ELIMINAR USUARIO
# --------------------
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    u = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(u)
    db.commit()
    return {"detail": "Usuario eliminado"}
