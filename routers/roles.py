from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.models import Rol

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


@router.get("/")
def listar_roles(db: Session = Depends(get_db)):
    """
    Devuelve todos los roles
    """
    roles = db.query(Rol).all()
    return roles
