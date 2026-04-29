"""
Pruebas unitarias — Módulo notas
Sistema de Notas Universitarias
"""

import pytest
from src.estudiantes import Estudiante
from src.materias import Materia
from src.notas import Trabajo, GestorNotas


# ─────────────────────────────────────────────
#  Fixtures compartidos
# ─────────────────────────────────────────────

@pytest.fixture
def estudiante():
    return Estudiante("E001", "Ana García", "ana@test.com")

@pytest.fixture
def estudiante2():
    return Estudiante("E002", "Carlos Mejía", "carlos@test.com")

@pytest.fixture
def materia():
    return Materia("CS101", "Calidad del Software", 3)

@pytest.fixture
def materia2():
    return Materia("IS201", "Ingeniería de Requerimientos", 3)

@pytest.fixture
def gestor():
    return GestorNotas()


# ─────────────────────────────────────────────
#  Tests: clase Trabajo
# ─────────────────────────────────────────────

class TestTrabajo:

    def test_creacion_correcta(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Taller 1", 4.2)
        assert t.nombre_trabajo == "Taller 1"
        assert t.nota == 4.2
        assert t.estudiante is estudiante
        assert t.materia is materia

    def test_nota_se_redondea_dos_decimales(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Parcial", 3.14159)
        assert t.nota == 3.14

    def test_nota_cero_es_valida(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Quiz", 0.0)
        assert t.nota == 0.0

    def test_nota_maxima_valida(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Final", 5.0)
        assert t.nota == 5.0

    def test_nota_negativa_lanza_error(self, estudiante, materia):
        with pytest.raises(ValueError, match="nota"):
            Trabajo(estudiante, materia, "Parcial", -0.1)

    def test_nota_mayor_a_cinco_lanza_error(self, estudiante, materia):
        with pytest.raises(ValueError):
            Trabajo(estudiante, materia, "Parcial", 5.1)

    def test_nota_no_numerica_lanza_error(self, estudiante, materia):
        with pytest.raises(ValueError):
            Trabajo(estudiante, materia, "Parcial", "cuatro")

    def test_nombre_trabajo_vacio_lanza_error(self, estudiante, materia):
        with pytest.raises(ValueError, match="trabajo"):
            Trabajo(estudiante, materia, "", 3.5)

    def test_aprobado_con_nota_igual_a_tres(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Parcial", 3.0)
        assert t.aprobado() is True

    def test_aprobado_con_nota_mayor_a_tres(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Parcial", 4.5)
        assert t.aprobado() is True

    def test_reprobado_con_nota_menor_a_tres(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Parcial", 2.9)
        assert t.aprobado() is False

    def test_to_dict(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Taller", 4.0)
        d = t.to_dict()
        assert d["estudiante"] == "E001"
        assert d["materia"] == "CS101"
        assert d["nota"] == 4.0
        assert d["aprobado"] is True

    def test_nota_entero_es_valida(self, estudiante, materia):
        t = Trabajo(estudiante, materia, "Quiz", 3)
        assert t.nota == 3.0


# ─────────────────────────────────────────────
#  Tests: clase GestorNotas
# ─────────────────────────────────────────────

class TestGestorNotas:

    def test_asignar_trabajo_incrementa_total(self, gestor, estudiante, materia):
        t = Trabajo(estudiante, materia, "Parcial", 4.0)
        gestor.asignar(t)
        assert gestor.total_trabajos() == 1

    def test_trabajos_de_estudiante_retorna_correctos(
        self, gestor, estudiante, estudiante2, materia
    ):
        t1 = Trabajo(estudiante, materia, "Parcial", 4.0)
        t2 = Trabajo(estudiante2, materia, "Parcial", 3.5)
        t3 = Trabajo(estudiante, materia, "Final", 3.8)
        gestor.asignar(t1)
        gestor.asignar(t2)
        gestor.asignar(t3)
        trabajos_ana = gestor.trabajos_de_estudiante("E001")
        assert len(trabajos_ana) == 2

    def test_trabajos_de_materia_retorna_correctos(
        self, gestor, estudiante, materia, materia2
    ):
        t1 = Trabajo(estudiante, materia, "Parcial", 4.0)
        t2 = Trabajo(estudiante, materia2, "Parcial", 3.0)
        gestor.asignar(t1)
        gestor.asignar(t2)
        trabajos_cs101 = gestor.trabajos_de_materia("CS101")
        assert len(trabajos_cs101) == 1

    def test_promedio_estudiante_calculo_correcto(
        self, gestor, estudiante, materia, materia2
    ):
        gestor.asignar(Trabajo(estudiante, materia, "P1", 4.0))
        gestor.asignar(Trabajo(estudiante, materia2, "P2", 3.0))
        assert gestor.promedio_estudiante("E001") == 3.5

    def test_promedio_estudiante_sin_trabajos_es_cero(self, gestor):
        assert gestor.promedio_estudiante("E999") == 0.0

    def test_promedio_materia_calculo_correcto(
        self, gestor, estudiante, estudiante2, materia
    ):
        gestor.asignar(Trabajo(estudiante, materia, "P1", 4.0))
        gestor.asignar(Trabajo(estudiante2, materia, "P1", 3.0))
        assert gestor.promedio_materia("CS101") == 3.5

    def test_promedio_materia_sin_trabajos_es_cero(self, gestor):
        assert gestor.promedio_materia("XX999") == 0.0

    def test_reporte_estudiante_estructura(
        self, gestor, estudiante, materia, materia2
    ):
        gestor.asignar(Trabajo(estudiante, materia, "Parcial", 4.0))
        gestor.asignar(Trabajo(estudiante, materia2, "Quiz", 2.5))
        reporte = gestor.reporte_estudiante("E001")
        assert reporte["total_trabajos"] == 2
        assert reporte["aprobados"] == 1
        assert reporte["reprobados"] == 1
        assert reporte["promedio"] == 3.25

    def test_reporte_estudiante_sin_trabajos(self, gestor):
        reporte = gestor.reporte_estudiante("E999")
        assert reporte["total_trabajos"] == 0
        assert reporte["promedio"] == 0.0

    def test_total_trabajos_inicial_es_cero(self, gestor):
        assert gestor.total_trabajos() == 0

    def test_multiples_trabajos_mismo_estudiante_materia(
        self, gestor, estudiante, materia
    ):
        for i, nota in enumerate([3.5, 4.0, 4.5], 1):
            gestor.asignar(Trabajo(estudiante, materia, f"Taller {i}", nota))
        assert gestor.total_trabajos() == 3
        assert gestor.promedio_estudiante("E001") == round((3.5 + 4.0 + 4.5) / 3, 2)
