"""
Módulo 3: Gestión de Trabajos y Notas
Sistema de Notas Universitarias — Calidad del Software
"""

from src.estudiantes import Estudiante
from src.materias import Materia


class Trabajo:
    """Representa la nota de un trabajo asignado a un estudiante en una materia."""

    NOTA_MIN = 0.0
    NOTA_MAX = 5.0

    def __init__(
        self,
        estudiante: Estudiante,
        materia: Materia,
        nombre_trabajo: str,
        nota: float,
    ):
        if not nombre_trabajo or not nombre_trabajo.strip():
            raise ValueError("El nombre del trabajo no puede estar vacío.")
        if not isinstance(nota, (int, float)):
            raise ValueError("La nota debe ser un valor numérico.")
        if not (self.NOTA_MIN <= nota <= self.NOTA_MAX):
            raise ValueError(
                f"La nota debe estar entre {self.NOTA_MIN} y {self.NOTA_MAX}."
            )

        self.estudiante = estudiante
        self.materia = materia
        self.nombre_trabajo = nombre_trabajo.strip()
        self.nota = round(float(nota), 2)

    def aprobado(self) -> bool:
        """Un trabajo se considera aprobado con nota >= 3.0."""
        return self.nota >= 3.0

    def __repr__(self):
        return (
            f"Trabajo(estudiante={self.estudiante.codigo!r}, "
            f"materia={self.materia.codigo!r}, "
            f"trabajo={self.nombre_trabajo!r}, nota={self.nota})"
        )

    def to_dict(self) -> dict:
        return {
            "estudiante": self.estudiante.codigo,
            "materia": self.materia.codigo,
            "trabajo": self.nombre_trabajo,
            "nota": self.nota,
            "aprobado": self.aprobado(),
        }


class GestorNotas:
    """Gestiona todos los trabajos y permite consultar promedios y reportes."""

    def __init__(self):
        self._trabajos: list[Trabajo] = []

    def asignar(self, trabajo: Trabajo) -> None:
        """Registra un nuevo trabajo."""
        self._trabajos.append(trabajo)

    def trabajos_de_estudiante(self, codigo_estudiante: str) -> list[Trabajo]:
        """Retorna todos los trabajos de un estudiante."""
        return [t for t in self._trabajos if t.estudiante.codigo == codigo_estudiante.upper()]

    def trabajos_de_materia(self, codigo_materia: str) -> list[Trabajo]:
        """Retorna todos los trabajos de una materia."""
        return [t for t in self._trabajos if t.materia.codigo == codigo_materia.upper()]

    def promedio_estudiante(self, codigo_estudiante: str) -> float:
        """Calcula el promedio general de un estudiante. Retorna 0.0 si no tiene trabajos."""
        trabajos = self.trabajos_de_estudiante(codigo_estudiante)
        if not trabajos:
            return 0.0
        return round(sum(t.nota for t in trabajos) / len(trabajos), 2)

    def promedio_materia(self, codigo_materia: str) -> float:
        """Calcula el promedio de notas en una materia. Retorna 0.0 si no hay trabajos."""
        trabajos = self.trabajos_de_materia(codigo_materia)
        if not trabajos:
            return 0.0
        return round(sum(t.nota for t in trabajos) / len(trabajos), 2)

    def reporte_estudiante(self, codigo_estudiante: str) -> dict:
        """Genera un reporte completo de un estudiante."""
        trabajos = self.trabajos_de_estudiante(codigo_estudiante)
        return {
            "codigo": codigo_estudiante.upper(),
            "total_trabajos": len(trabajos),
            "promedio": self.promedio_estudiante(codigo_estudiante),
            "aprobados": sum(1 for t in trabajos if t.aprobado()),
            "reprobados": sum(1 for t in trabajos if not t.aprobado()),
            "trabajos": [t.to_dict() for t in trabajos],
        }

    def total_trabajos(self) -> int:
        return len(self._trabajos)
