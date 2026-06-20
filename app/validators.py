import re
from datetime import datetime

# ISBN: exactamente 13 dígitos numéricos (el enunciado lo pide así, sin guiones).
_ISBN_RE = re.compile(r"^\d{13}$")
# Email: algo@algo.ext (sin espacios, con al menos un punto en el dominio).
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_isbn(value: str) -> str:
    if not _ISBN_RE.fullmatch(value):
        raise ValueError("El ISBN debe contener exactamente 13 dígitos numéricos")
    return value


def validar_email(value: str) -> str:
    if not _EMAIL_RE.fullmatch(value):
        raise ValueError("El email no tiene un formato válido (usuario@dominio.ext)")
    return value


def validar_anio(value: int) -> int:
    # TRAMPA #4: el enunciado fija el CHECK en 2026, pero la validación dice
    # "hasta el año actual". Acá usamos el año actual dinámico; el CHECK de la
    # base queda como segunda barrera.
    actual = datetime.now().year
    if value < 1000 or value > actual:
        raise ValueError(f"El año de publicación debe estar entre 1000 y {actual}")
    return value
