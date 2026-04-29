# Paquete principal — Sistema de Notas Universitarias
from src.estudiantes import Estudiante, RegistroEstudiantes
from src.materias import Materia, RegistroMaterias
from src.notas import Trabajo, GestorNotas

__all__ = [
    "Estudiante", "RegistroEstudiantes",
    "Materia", "RegistroMaterias",
    "Trabajo", "GestorNotas",
]
