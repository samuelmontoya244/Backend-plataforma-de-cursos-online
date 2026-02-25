from datetime import date


class Certificado:
    def __init__(
        self,
        codigo: str,
        estudiante_id: str,
        estudiante_nombre: str,
        curso_codigo: str,
        curso_nombre: str,
        fecha_emision: date | None = None,
    ) -> None:
        self._codigo = codigo.strip()
        self._estudiante = (estudiante_id.strip(), estudiante_nombre.strip())
        self._curso = (curso_codigo.strip(), curso_nombre.strip())
        self._fecha = fecha_emision or date.today()

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def estudiante(self) -> tuple[str, str]:
        return self._estudiante

    @property
    def curso(self) -> tuple[str, str]:
        return self._curso

    @property
    def fecha_emision(self) -> date:
        return self._fecha

    def __str__(self) -> str:
        return (
            f"Certificado {self._codigo} | "
            f"Estudiante: {self._estudiante[1]} ({self._estudiante[0]}) | "
            f"Curso: {self._curso[1]} ({self._curso[0]}) | "
            f"Fecha: {self._fecha.isoformat()}"
        )
