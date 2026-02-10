# 📚 Ejemplos de Prompts para el Sistema RAG Legal

>[!IMPORTANT]
> Estos prompts están hechos para la **opción 3: Modo estructurado con Pydantic AI** (respuestas con fuentes y confianza)

---

## 🎯 PROMPTS TÉCNICOS (Datos Duros)

### 📝 Caso 01: Indemnización Civil

| Campo | Detalle |
|-------|---------|
| **Partes** | María López vs. Constructora Andina S.A. |
| **Materia** | Civil - Indemnización por daños y perjuicios |
| **Notificación** | Lunes 3 de junio de 2024 |
| **Plazo esperado** | 10 días hábiles → 18 de junio de 2024 |

**Prompt:**
```
María López interpuso una demanda civil de indemnización por daños y perjuicios contra la empresa Constructora Andina S.A.
El proceso se tramitó en vía ordinaria civil.
El Juzgado Civil de Lima emitió sentencia de primera instancia, declarando infundada la demanda.
Teniendo en cuenta que la sentencia civil fue notificada el lunes 3 de junio de 2024, ¿hasta qué fecha límite puede la empresa Constructora Andina S.A. interponer recurso de apelación? Justifique el cómputo del plazo.
```

---

### 📝 Caso 02: Despido Arbitrario (Laboral)

| Campo | Detalle |
|-------|---------|
| **Partes** | Juan Pérez vs. Servicios Logísticos del Sur S.A. |
| **Materia** | Laboral - Despido arbitrario |
| **Notificación** | 10 de julio de 2024 |
| **Plazo esperado** | 3 días hábiles → 15 de julio de 2024 |

**Prompt:**
```
Juan Pérez demandó a la empresa Servicios Logísticos del Sur S.A. en un proceso laboral ordinario por despido arbitrario.
El Juzgado de Trabajo emitió sentencia de primera instancia, declarando fundada en parte la demanda.
La empresa desea apelar la sentencia.
¿Hasta qué fecha puede la empresa Servicios Logísticos del Sur S.A. interponer recurso de apelación contra la sentencia laboral notificada el 10 de julio de 2024? Explique el cómputo del plazo.
```

---

### 📝 Caso 03: Indemnización de Perjuicios

| Campo | Detalle |
|-------|---------|
| **Partes** | María López vs. Demandado |
| **Materia** | Civil - Indemnización de perjuicios |
| **Notificación** | 4 de marzo de 2026 (por cédula) |
| **Plazo esperado** | 10 días hábiles |

**Prompt:**
```
El 4 de marzo de 2026, María López fue notificada por cédula de una sentencia definitiva dictada por el Segundo Juzgado Civil de Lima que rechazó su demanda de indemnización de perjuicios.
¿Hasta qué fecha puede interponer válidamente el recurso de apelación y qué normas regulan este plazo?
```

---

### 📝 Caso 04: Condena de Pago + Efectos de Apelación

| Campo | Detalle |
|-------|---------|
| **Partes** | Pedro Ramírez (demandado) |
| **Materia** | Civil - Condena de pago |
| **Notificación** | 10 de abril de 2026 |
| **Consulta adicional** | Efectos de la apelación sobre ejecución |

**Prompt:**
```
Pedro Ramírez fue notificado el 10 de abril de 2026 de una sentencia civil de primera instancia que lo condena al pago de una suma de dinero.
Quiere apelar la sentencia y consulta si la ejecución del fallo se suspende automáticamente con la interposición del recurso.
¿Qué tipo de recurso procede, cuál es su plazo y cuáles son sus efectos?
```

---

### 📝 Caso 05: Apelación + Casación Conjunta

| Campo | Detalle |
|-------|---------|
| **Partes** | Ana Torres |
| **Materia** | Civil - Errores de derecho |
| **Notificación** | 2 de junio de 2026 |
| **Consulta adicional** | Recursos múltiples y forma de presentación |

**Prompt:**
```
En un juicio civil, Ana Torres fue notificada de la sentencia definitiva el 2 de junio de 2026. Su abogado considera que existen errores de derecho en el fallo y además quiere que el tribunal superior revise los hechos.
¿Qué recursos puede interponer, en qué forma pueden presentarse y cuál es el plazo aplicable?
```

---

### 📝 Caso 06: Recurso de Reposición

| Campo | Detalle |
|-------|---------|
| **Partes** | Carlos Medina |
| **Materia** | Civil - Impugnación de auto |
| **Notificación** | 15 de mayo de 2026 |
| **Tipo de resolución** | Auto que rechaza prueba documental |

**Prompt:**
```
El Juzgado Civil dictó un auto que rechaza una prueba documental ofrecida por Carlos Medina dentro del juicio.
Carlos fue notificado el 15 de mayo de 2026 y desea impugnar la resolución.
¿Qué recurso procede, cuál es el plazo y ante qué tribunal debe interponerse?
```

---

### 📝 Caso 07: Notificación Inválida

| Campo | Detalle |
|-------|---------|
| **Partes** | Laura Gómez |
| **Materia** | Civil - Validez de notificación |
| **Situación** | Informada verbalmente, sin notificación formal |

**Prompt:**
```
Laura Gómez fue informada verbalmente del contenido de una sentencia civil, pero nunca recibió notificación por cédula ni por estado diario.
¿Desde cuándo comienza a correr el plazo para apelar y qué norma regula la validez de la notificación?
```

---

## 💬 PROMPTS CONVERSACIONALES (Lenguaje Natural)

> Estos prompts simulan cómo un usuario real podría hacer consultas de forma más informal.

---

### 🗣️ Consulta 01: Plazo básico de apelación

```
Hola, me llegó una notificación del juzgado con una sentencia civil y no tengo claro cuánto tiempo tengo para apelar.
Me notificaron el 4 de marzo de 2026 por cédula.
¿Hasta cuándo puedo presentar la apelación y cómo se cuentan los días?
```

---

### 🗣️ Consulta 02: Efectos de la apelación

```
Buenas, estoy revisando un caso civil y tengo una duda.
La sentencia fue notificada el 10 de abril y queremos apelar, pero no sé si al apelar se suspende automáticamente la ejecución de la sentencia.
¿Me podrías aclarar eso y el plazo que tenemos?
```

---

### 🗣️ Consulta 03: Apelación + Casación

```
Hola, tengo una duda medio urgente.
Me notificaron una sentencia civil hace unos días y quiero apelar, pero no sé bien cómo se cuentan los días ni si se suspende la ejecución.
Además, no sé si puedo presentar apelación junto con casación.
¿Me podrías orientar con eso?
```

---

### 🗣️ Consulta 04: Notificación informal

```
Me enteré de una sentencia porque alguien del juzgado me avisó, pero nunca me llegó ninguna notificación formal.
¿Desde cuándo empieza a correr el plazo para apelar en ese caso?
```

---

### 🗣️ Consulta 05: Múltiples recursos

```
Perdí un juicio civil y mi abogado me dijo que podríamos apelar y también ir a casación si es necesario.
Me notificaron la sentencia el 2 de junio de 2026.
¿Qué recursos puedo presentar y en qué plazos?
```

---

## 📊 Resumen de Plazos Esperados

| Tipo de Proceso | Plazo de Apelación | Base Legal |
|-----------------|-------------------|------------|
| Civil | 10 días hábiles | Art. 189 CPC |
| Laboral | 3 días hábiles | Ley Procesal del Trabajo |
| Penal | 5 días hábiles | Código Procesal Penal |
| Casación | 15 días hábiles | Art. CPC |
| Reposición | 5 días hábiles | CPC |

