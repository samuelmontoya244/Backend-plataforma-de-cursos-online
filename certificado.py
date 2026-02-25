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
        self._estudiante_id = estudiante_id.strip()
        self._estudiante_nombre = estudiante_nombre.strip()
        self._curso_codigo = curso_codigo.strip()
        self._curso_nombre = curso_nombre.strip()
        self._fecha_emision = fecha_emision if fecha_emision else date.today()

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def estudiante_id(self) -> str:
        return self._estudiante_id

    @property
    def estudiante_nombre(self) -> str:
        return self._estudiante_nombre

    @property
    def curso_codigo(self) -> str:
        return self._curso_codigo

    @property
    def curso_nombre(self) -> str:
        return self._curso_nombre

    @property
    def fecha_emision(self) -> date:
        return self._fecha_emision

    def __str__(self) -> str:
        return (
            f"Certificado {self._codigo}\n"
            f"Estudiante: {self._estudiante_nombre} ({self._estudiante_id})\n"
            f"Curso: {self._curso_nombre} ({self._curso_codigo})\n"
            f"Fecha de emisión: {self._fecha_emision.isoformat()}"
        )
