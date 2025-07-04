# Issue de Calidad 1: Complejidad Cognitiva Excesiva en `vista_csv`

## ![alt text](image-1.png)

**Ubicación:** `vigifia_app/views.py`  
**Función:** `vista_csv`  
**Regla:** `python:S3776 - Cognitive Complexity of functions should not be too high`  
**Severidad:** `Crítica`   
**Complejidad actual:** 21  
**Complejidad permitida:** 15  
**Impacto:** Mantenibilidad

---

## Descripción del problema

La función `vista_csv`, encargada de procesar y mostrar contenido de fuentes CSV o API en la vista web, excede el umbral de **complejidad cognitiva permitido por Sonarqube**, lo que hace difícil su comprensión y mantenimiento.

Esto se debe principalmente a:

- Uso excesivo de condicionales anidados (`if`, `elif`, `else`).
- Lógica ramificada con múltiples casos para distintas estructuras de datos.
- Repetición de patrones de renderizado.

---

## Solución aplicada

- Se separaron bloques lógicos en funciones auxiliares (procesar_api_con_imagen, procesar_dict_con_listas, procesar_lista_dicts).
- Se redujo el número de condiciones anidadas.
- Se eliminó la repetición de patrones de renderizado.

---

## Resultado tras corrección

La complejidad cognitiva se redujo y la función vista_csv es ahora más legible y mantenible. En la re-inspección con SonarQube, este quality issue desapareció.




# Issue de calidad 2: Duplicación de Literales

![alt text](image.png)

**Ubicación:** `vigifia_app/views.py`, línea 136  
**Regla:** `python:S1192 - Define a constant instead of duplicating this literal `'vista_csv.html'` 6 times.`   
**Severidad:** `Crítica`  
**Impacto:** Mantenibilidad

---

## Descripción del problema

El literal `'vista_csv.html'` se repite 6 veces en el método `vista_csv`, cada vez que se llama a `render()`. Esta práctica genera dificultades para mantener el código a largo plazo:

- Si se desea cambiar el nombre del template, se deben modificar múltiples líneas manualmente.
- Incrementa el riesgo de inconsistencias y errores tipográficos.
- Viola el principio DRY (*Don’t Repeat Yourself*).

---

## Solución aplicada

- Se definió una constante TEMPLATE_VISTA_CSV = 'vista_csv.html' al inicio del archivo.
- Se reemplazaron todas las instancias del literal por esta constante.

---

## Resultado tras corrección

El código es más limpio y mantenible. En caso de cambiar el nombre del template, solo se modifica una línea. El issue desapareció tras re-inspección con SonarQube.

---

## Re-inspección

<img width="1076" alt="Captura de pantalla 2025-06-23 a la(s) 12 22 20 a m" src="https://github.com/user-attachments/assets/f2a32cbe-9cb0-4b9e-91f2-4641dde3f6f9" />



# Issues restantes:

![alt text](image-2.png)

Los issues 1 y 2 son los que más relevancia tienen con respecto al estado actual del proyecto, por ende serán los que se refactorizarán para una mejor mantenibilidad de la arquitectura. Sin embargo, existen más issues como los expuestos en la imagen 2 que tienen un impacto bajo en la arquitectura, por lo que no se abordarán en el mejoramiento de los quality issues.



---

## Registro de trabajo realizado

| Tarea | Descripción | Tiempo empleado |
|:-----|:-------------|:----------------|
| 1 | Se analizó el informe de SonarQube y se eligió las dos quality issues | 15 min |
| 2 | Se refactorizó vista_csv dividiendo la lógica en funciones auxiliares para reducir la complejidad cognitiva de 21 a menos de 15. | 40 min |
| 3 | Se corrigió el quality issue crítico (S1192) evitando la repetición del literal 'vista_csv.html' mediante una constante. | 10 min |
| 4 | Se realizó la re-inspección con SonarQube y se validó que ambos issues fueron resueltos exitosamente. | 10 min |
| 5 | Se documentaron los cambios en la carpeta /inspections/ y en la Wiki del proyecto según la pauta del hito. | 15 min |

** Tiempo total estimado invertido:** `1 hora y 30 minutos`

---
