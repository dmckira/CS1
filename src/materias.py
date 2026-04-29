"""
Módulo 2: Gestión de Materias
Sistema de Notas Universitarias — Calidad del Software
"""


class Materia:
    """Representa una materia del plan de estudios."""

    CREDITOS_MIN = 1
    CREDITOS_MAX = 6

    def __init__(self, codigo: str, nombre: str, creditos: int):
        if not codigo or not codigo.strip():
            raise ValueError("El código de la materia no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la materia no puede estar vacío.")
        if not isinstance(creditos, int) or not (self.CREDITOS_MIN <= creditos <= self.CREDITOS_MAX):
            raise ValueError(
                f"Los créditos deben ser un entero entre "
                f"{self.CREDITOS_MIN} y {self.CREDITOS_MAX}."
            )

        self.codigo = codigo.strip().upper()
        self.nombre = nombre.strip()
        self.creditos = creditos

    def __repr__(self):
        return f"Materia(codigo={self.codigo!r}, nombre={self.nombre!r}, creditos={self.creditos})"

    def to_dict(self) -> dict:
        return {"codigo": self.codigo, "nombre": self.nombre, "creditos": self.creditos}


class RegistroMaterias:
    """Repositorio en memoria para gestionar materias."""

    def __init__(self):
        self._materias: dict[str, Materia] = {}

    def registrar(self, materia: Materia) -> None:
        """Registra una materia. Lanza ValueError si el código ya existe."""
        if materia.codigo in self._materias:
            raise ValueError(f"Ya existe una materia con código {materia.codigo!r}.")
        self._materias[materia.codigo] = materia

    def buscar(self, codigo: str) -> Materia:
        """Retorna la materia por código. Lanza KeyError si no existe."""
        codigo = codigo.strip().upper()
        if codigo not in self._materias:
            raise KeyError(f"No se encontró la materia con código {codigo!r}.")
        return self._materias[codigo]

    def listar(self) -> list[Materia]:
        """Retorna todas las materias ordenadas por nombre."""
        return sorted(self._materias.values(), key=lambda m: m.nombre)

    def eliminar(self, codigo: str) -> None:
        """Elimina una materia por código."""
        codigo = codigo.strip().upper()
        if codigo not in self._materias:
            raise KeyError(f"No se encontró la materia con código {codigo!r}.")
        del self._materias[codigo]

    def total_creditos(self) -> int:
        """Suma de créditos de todas las materias registradas."""
        return sum(m.creditos for m in self._materias.values())

    def total(self) -> int:
        return len(self._materias)
