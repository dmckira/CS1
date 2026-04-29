"""
Módulo 1: Gestión de Estudiantes
Sistema de Notas Universitarias — Calidad del Software
"""


class Estudiante:
    """Representa un estudiante registrado en el sistema."""

    def __init__(self, codigo: str, nombre: str, email: str):
        if not codigo or not codigo.strip():
            raise ValueError("El código del estudiante no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del estudiante no puede estar vacío.")
        if "@" not in email:
            raise ValueError("El email debe contener '@'.")

        self.codigo = codigo.strip().upper()
        self.nombre = nombre.strip()
        self.email = email.strip().lower()

    def __repr__(self):
        return f"Estudiante(codigo={self.codigo!r}, nombre={self.nombre!r})"

    def to_dict(self) -> dict:
        return {"codigo": self.codigo, "nombre": self.nombre, "email": self.email}


class RegistroEstudiantes:
    """Repositorio en memoria para gestionar estudiantes."""

    def __init__(self):
        self._estudiantes: dict[str, Estudiante] = {}

    def registrar(self, estudiante: Estudiante) -> None:
        """Registra un nuevo estudiante. Lanza ValueError si el código ya existe."""
        if estudiante.codigo in self._estudiantes:
            raise ValueError(f"Ya existe un estudiante con código {estudiante.codigo!r}.")
        self._estudiantes[estudiante.codigo] = estudiante

    def buscar(self, codigo: str) -> Estudiante:
        """Retorna el estudiante por código. Lanza KeyError si no existe."""
        codigo = codigo.strip().upper()
        if codigo not in self._estudiantes:
            raise KeyError(f"No se encontró el estudiante con código {codigo!r}.")
        return self._estudiantes[codigo]

    def listar(self) -> list[Estudiante]:
        """Retorna todos los estudiantes ordenados por nombre."""
        return sorted(self._estudiantes.values(), key=lambda e: e.nombre)

    def eliminar(self, codigo: str) -> None:
        """Elimina un estudiante por código."""
        codigo = codigo.strip().upper()
        if codigo not in self._estudiantes:
            raise KeyError(f"No se encontró el estudiante con código {codigo!r}.")
        del self._estudiantes[codigo]

    def total(self) -> int:
        return len(self._estudiantes)
