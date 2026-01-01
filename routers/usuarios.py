# routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from db.models import Usuario, Rol

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

# --------------------
# LISTAR USUARIOS
# --------------------
@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


# --------------------
# CREAR USUARIO
# --------------------
@router.post("/")
def crear_usuario(nombre: str, apellido: str, mail: str, cod_rol: int, db: Session = Depends(get_db)):
    # Validar que exista el rol
    rol = db.query(Rol).filter(Rol.id == cod_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Validar que el mail no exista
    existing = db.query(Usuario).filter(Usuario.mail == mail).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    usuario = Usuario(nombre=nombre, apellido=apellido, mail=mail, cod_rol=cod_rol)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


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
# ACTUALIZAR USUARIO
# --------------------
@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, nombre: str = None, apellido: str = None, mail: str = None, cod_rol: int = None, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if cod_rol:
        rol = db.query(Rol).filter(Rol.id == cod_rol).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        usuario.cod_rol = cod_rol
    
    if nombre:
        usuario.nombre = nombre
    if apellido:
        usuario.apellido = apellido
    if mail:
        existing = db.query(Usuario).filter(Usuario.mail == mail, Usuario.id != usuario_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        usuario.mail = mail
    
    db.commit()
    db.refresh(usuario)
    return usuario


# --------------------
# ELIMINAR USUARIO
# --------------------
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"detail": "Usuario eliminado"}
