"""
Pruebas unitarias — Módulo materias
Sistema de Notas Universitarias
"""

import pytest
from src.materias import Materia, RegistroMaterias


# ─────────────────────────────────────────────
#  Tests: clase Materia
# ─────────────────────────────────────────────

class TestMateria:

    def test_creacion_correcta(self):
        m = Materia("CS101", "Calidad del Software", 3)
        assert m.codigo == "CS101"
        assert m.nombre == "Calidad del Software"
        assert m.creditos == 3

    def test_codigo_se_convierte_a_mayusculas(self):
        m = Materia("cs101", "Materia", 2)
        assert m.codigo == "CS101"

    def test_nombre_se_elimina_espacios(self):
        m = Materia("M1", "  Matemáticas  ", 4)
        assert m.nombre == "Matemáticas"

    def test_creditos_minimo_valido(self):
        m = Materia("M1", "Materia", 1)
        assert m.creditos == 1

    def test_creditos_maximo_valido(self):
        m = Materia("M1", "Materia", 6)
        assert m.creditos == 6

    def test_creditos_cero_lanza_error(self):
        with pytest.raises(ValueError, match="créditos"):
            Materia("M1", "Materia", 0)

    def test_creditos_negativos_lanza_error(self):
        with pytest.raises(ValueError):
            Materia("M1", "Materia", -1)

    def test_creditos_mayor_maximo_lanza_error(self):
        with pytest.raises(ValueError):
            Materia("M1", "Materia", 7)

    def test_creditos_float_lanza_error(self):
        with pytest.raises(ValueError):
            Materia("M1", "Materia", 2.5)

    def test_codigo_vacio_lanza_error(self):
        with pytest.raises(ValueError, match="código"):
            Materia("", "Materia", 3)

    def test_nombre_vacio_lanza_error(self):
        with pytest.raises(ValueError, match="nombre"):
            Materia("M1", "", 3)

    def test_to_dict(self):
        m = Materia("CS101", "Calidad", 3)
        assert m.to_dict() == {"codigo": "CS101", "nombre": "Calidad", "creditos": 3}

    def test_repr(self):
        m = Materia("CS101", "Calidad", 3)
        assert "CS101" in repr(m)
        assert "3" in repr(m)


# ─────────────────────────────────────────────
#  Tests: clase RegistroMaterias
# ─────────────────────────────────────────────

class TestRegistroMaterias:

    def setup_method(self):
        self.registro = RegistroMaterias()
        self.m1 = Materia("CS101", "Calidad del Software", 3)
        self.m2 = Materia("IS201", "Ingeniería de Requerimientos", 3)
        self.m3 = Materia("BD301", "Bases de Datos", 4)

    def test_registrar_materia_nueva(self):
        self.registro.registrar(self.m1)
        assert self.registro.total() == 1

    def test_registrar_codigo_duplicado_lanza_error(self):
        self.registro.registrar(self.m1)
        duplicada = Materia("CS101", "Otra materia", 2)
        with pytest.raises(ValueError, match="(?i)ya existe"):
            self.registro.registrar(duplicada)

    def test_buscar_materia_existente(self):
        self.registro.registrar(self.m1)
        encontrada = self.registro.buscar("CS101")
        assert encontrada.nombre == "Calidad del Software"

    def test_buscar_codigo_minusculas(self):
        self.registro.registrar(self.m1)
        encontrada = self.registro.buscar("cs101")
        assert encontrada.codigo == "CS101"

    def test_buscar_codigo_inexistente_lanza_error(self):
        with pytest.raises(KeyError):
            self.registro.buscar("XX999")

    def test_listar_ordenado_por_nombre(self):
        self.registro.registrar(self.m2)  # Ingeniería
        self.registro.registrar(self.m3)  # Bases
        self.registro.registrar(self.m1)  # Calidad
        lista = self.registro.listar()
        nombres = [m.nombre for m in lista]
        assert nombres == sorted(nombres)

    def test_listar_vacio(self):
        assert self.registro.listar() == []

    def test_eliminar_materia_existente(self):
        self.registro.registrar(self.m1)
        self.registro.eliminar("CS101")
        assert self.registro.total() == 0

    def test_eliminar_materia_inexistente_lanza_error(self):
        with pytest.raises(KeyError):
            self.registro.eliminar("XX999")

    def test_total_creditos_suma_correcta(self):
        self.registro.registrar(self.m1)  # 3
        self.registro.registrar(self.m3)  # 4
        assert self.registro.total_creditos() == 7

    def test_total_creditos_registro_vacio(self):
        assert self.registro.total_creditos() == 0

    def test_total_inicial_es_cero(self):
        assert self.registro.total() == 0
