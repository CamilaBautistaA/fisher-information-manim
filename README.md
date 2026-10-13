# Información de Fisher — presentación con Manim Slides

Exposición corta (≈ 12 min) para un curso de **Inferencia Estadística**, hecha con
[Manim](https://www.manim.community/) y [Manim Slides](https://github.com/jeertmans/manim-slides).
Las fuentes de cada diapositiva están en [`BIBLIOGRAFIA.md`](BIBLIOGRAFIA.md).

## Contenido

| # | Diapositiva | Animación | Tiempo sugerido |
|---|-------------|-----------|-----------------|
| 1 | Portada | — | 0:30 |
| 2 | ¿Cuánta información trae la muestra? | log-verosimilitud que se afila al crecer *n*; curvatura = *n·I(p̂)* | 2:00 |
| 3 | Función score | demostración de E[S] = 0 | 1:30 |
| 4 | Información de Fisher | Var(S) = −E[∂² log f] | 1:30 |
| 5 | Ejemplo Bernoulli(p) | derivación y gráfica de I(p) = 1/(p(1−p)) | 1:30 |
| 6 | Propiedades | aditividad, reparametrización, Normal | 1:00 |
| 7 | Cota de Cramér–Rao | MLE vs. estimador con la mitad de los datos | 1:30 |
| 8 | Normalidad asintótica del MLE | histograma de simulaciones que converge a N(0,1) | 1:30 |
| 9 | Resumen | — | 0:45 |
| 10 | Referencias | — | 0:15 |

Cada diapositiva tiene varios "clics" (≈ 23 en total) y **notas del presentador** en español
(diccionario `NOTAS` al inicio de `fisher_slides.py`).

## Requisitos

- Python reciente (3.10 o superior).
- Una distribución de **LaTeX** (TeX Live, MacTeX o MiKTeX): Manim la usa para `MathTex`.
- **FFmpeg** y las librerías Cairo/Pango (ver la guía de instalación de Manim:
  <https://docs.manim.community/en/stable/installation.html>).
- Detalles de Manim Slides: <https://eertmans.be/manim-slides/latest/installation.html>.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
manim-slides checkhealth           # comprueba que todo está instalado
```

## Uso

```bash
# 1. Renderizar (prueba rápida en baja calidad; usa -qh para la versión final)
manim-slides render fisher_slides.py FisherInformation -ql

# 2. Presentar en vivo (ventana nativa)
manim-slides present FisherInformation

# 3. Exportar a HTML (RevealJS) para abrir en cualquier navegador
mkdir -p docs
manim-slides convert FisherInformation docs/index.html --one-file --offline
```

Tip: mientras editas, comenta secciones en la lista `secciones` de `construct()` para renderizar solo la que estás
ajustando. Manim guarda en caché lo ya renderizado.

## Personalizar

Al inicio de `fisher_slides.py`: `AUTOR`, `INSTITUCION`, `CURSO`, `REPO`, colores y el diccionario `NOTAS`.

## Verificar las matemáticas

```bash
python fisher_math.py
```

Comprueba numéricamente (Monte Carlo) que E[score] = 0, Var(score) = 1/(p(1−p)), que la curvatura de la
log-verosimilitud en el MLE es *n·I(p̂)*, que Var(MLE) alcanza la cota de Cramér–Rao y que usar la mitad de los datos
duplica la varianza.

## Publicar en GitHub

```bash
git init
git add .
git commit -m "Presentación: Información de Fisher"
git branch -M main
git remote add origin https://github.com/<usuario>/<repo>.git
git push -u origin main
```

Para tener la presentación en línea: **Settings → Pages → Deploy from a branch → `main` / `/docs`**.
Quedará en `https://<usuario>.github.io/<repo>/`.

- GitHub rechaza archivos de más de 100 MB. Con `--one-file` el HTML incrusta los videos; si pesa demasiado,
  renderiza con `-qm` en lugar de `-qh`.
- Si exportas **sin** `--one-file`, sube también la carpeta de recursos que se genera junto al HTML.
- `media/` y `slides/` (videos intermedios) están en `.gitignore`.

## Si algo falla

- *Error de LaTeX / "latex not found"*: instala una distribución de LaTeX y reinicia la terminal.
- *Renderiza muy lento*: usa `-ql` mientras editas.
- *`TypeError` con `notes`*: actualiza con `pip install -U manim-slides` (el código ya lo tolera, pero sin notas).
- *Algo se ve desalineado en tu pantalla*: ajusta las posiciones (`move_to(...)`) de esa sección; las medidas están
  pensadas para el encuadre 16:9 por defecto de Manim.

## Estructura

```
fisher_slides.py   # la presentación (clase FisherInformation)
fisher_math.py     # funciones numéricas puras + pruebas (python fisher_math.py)
BIBLIOGRAFIA.md    # fuentes y qué diapositiva respalda cada una
requirements.txt
.gitignore
```

## Cómo citar las herramientas

Manim Slides pide citarlo o enlazar su repositorio al final de la presentación (ya está en la diapositiva de
referencias): Eertmans, J. (2023), *Manim Slides: A Python package for presenting Manim content anywhere*,
Journal of Open Source Education, doi:[10.21105/jose.00206](https://doi.org/10.21105/jose.00206).
