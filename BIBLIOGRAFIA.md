# Bibliografía

Todas las fuentes principales están disponibles gratis en línea.

## Fuentes principales

1. **Ly, A., Marsman, M., Verhagen, J., Grasman, R. & Wagenmakers, E.-J. (2017).**
   *A Tutorial on Fisher Information.* Journal of Mathematical Psychology, 80, 40–55.
   - arXiv (acceso abierto): <https://arxiv.org/abs/1705.01064>
   - DOI: <https://doi.org/10.1016/j.jmp.2017.05.006>
   - Tutorial de nivel accesible; cubre la definición, la forma con segunda derivada, y el papel de la información
     de Fisher en estadística frecuentista (tests e intervalos con el MLE), bayesiana (a priori por defecto) y MDL.

2. **MIT OpenCourseWare, 18.443 *Statistics for Applications* (otoño 2006), Lecture 3:**
   *Properties of MLE: consistency, asymptotic normality. Fisher information.*
   - Página: <https://ocw.mit.edu/courses/18-443-statistics-for-applications-fall-2006/resources/lecture3>
   - PDF: <https://ocw.mit.edu/courses/18-443-statistics-for-applications-fall-2006/03b407da8a94b3fe22d987453807ca46_lecture3.pdf>
   - Definición de la información de Fisher, forma alternativa de calcularla y normalidad asintótica del MLE
     (la varianza asintótica es menor cuanto mayor es la información).

3. **Erdely Ruiz, A. & Gutiérrez Peña, E.** *Monografía de Estadística Bayesiana.* UNAM (FES Acatlán / IIMAS).
   - arXiv: <https://arxiv.org/abs/2309.06601>
   - En español. La sección 3.4 (Regla de Jeffreys) enuncia la cota de Cramér–Rao, la información por unidad
     muestral, el lema de la segunda derivada, el ejemplo Binomial/Bernoulli y la invariancia ante
     reparametrizaciones.

4. **Fisher, R. A. (1925).** *Theory of Statistical Estimation.* Mathematical Proceedings of the Cambridge
   Philosophical Society, 22(5), 700–725.
   - DOI: <https://doi.org/10.1017/S0305004100009580>
   - Copia en el archivo digital de la Universidad de Adelaide: <https://hdl.handle.net/2440/15186>
   - Se usa solo como referencia histórica (no se toma de aquí ningún resultado de las diapositivas).

5. *(Opcional, contexto histórico)* **Stigler, S. M. (2007).** *The Epic Story of Maximum Likelihood.*
   Statistical Science. arXiv: <https://arxiv.org/abs/0804.2996>

## Herramientas

- Manim Community: <https://www.manim.community/> · documentación: <https://docs.manim.community/>
- Manim Slides: <https://github.com/jeertmans/manim-slides> · documentación: <https://eertmans.be/manim-slides/>
  · Eertmans, J. (2023). *Manim Slides: A Python package for presenting Manim content anywhere.*
  Journal of Open Source Education, 6. doi:[10.21105/jose.00206](https://doi.org/10.21105/jose.00206)

## ¿De dónde sale cada diapositiva?

| Diapositiva | Qué se afirma | Respaldo |
|---|---|---|
| 2. Motivación | Mayor curvatura de la log-verosimilitud ↔ mayor información ↔ estimación más precisa | MIT 18.443 L3 (interpretación informal de la información de Fisher); Ly et al. (definición y forma con segunda derivada). Las gráficas son ilustraciones propias. |
| 3. Score | Definición del score; E[S] = 0 bajo regularidad | Erdely & Gutiérrez Peña (demostración de E[∂ log p/∂θ] = 0 dentro del Lema 3.6); Ly et al. (§1.2). |
| 4. Información | I(θ) = Var(S) = E[S²] = −E[∂² log f/∂θ²] | Ly et al. (Def. 1.1 y nota al pie con la forma de segunda derivada); Erdely & Gutiérrez Peña (Lema 3.4); MIT 18.443 L3 (lema con la forma alternativa). |
| 5. Bernoulli | I(p) = 1/(p(1−p)) | Erdely & Gutiérrez Peña (Ej. 4, Binomial: m/(θ(1−θ)); Ej. 5, Bernoulli con m = 1). Los pasos intermedios están desarrollados aquí y verificados con `fisher_math.py`. |
| 6. Propiedades | I_n = n·I; I(φ) = I(θ)(dθ/dφ)²; Normal con σ conocido: I(μ) = 1/σ² | Erdely & Gutiérrez Peña (Cor. 3.3 y Lema 3.6). Normal: cálculo directo (score = (x−μ)/σ²). |
| 7. Cramér–Rao | Var(θ̂) ≥ 1/(n·I(θ)) para θ̂ insesgado; no aplica si el soporte depende de θ (p. ej. Uniforme) | Erdely & Gutiérrez Peña (Teo. 3.2, Cor. 3.3 y comentario sobre regularidad); Ly et al. (sección frecuentista). |
| 7. Comparación MLE vs. mitad de los datos | Var(MLE) = 1/(n·I); con n/2 datos la varianza se duplica | **Ejemplo propio** (no proviene de las fuentes). Verificado por simulación en `fisher_math.py`. |
| 8. Normalidad asintótica | √(n·I(θ))(θ̂ₙ − θ) → N(0,1) | MIT 18.443 L3; Ly et al. (uso del MLE en tests e intervalos). Histogramas: simulación propia (`simular_z`). |
| 9. Resumen | — | Las anteriores. |

> **Nota de verificación.** Los números de teorema/lema de Erdely & Gutiérrez Peña salen de leer el texto completo del
> PDF. De Ly et al. y de las notas del MIT revisé extractos, así que conviene que **abras ambos documentos y confirmes
> los números de sección** antes de citarlos en clase.

## Formato para pegar en una lista de referencias (APA 7, abreviado)

- Ly, A., Marsman, M., Verhagen, J., Grasman, R., & Wagenmakers, E.-J. (2017). A tutorial on Fisher information.
  *Journal of Mathematical Psychology, 80*, 40–55. https://doi.org/10.1016/j.jmp.2017.05.006
- Massachusetts Institute of Technology. (2006). *Lecture 3: Properties of MLE: consistency, asymptotic normality.
  Fisher information* [Lecture notes, 18.443 Statistics for Applications]. MIT OpenCourseWare.
  https://ocw.mit.edu/courses/18-443-statistics-for-applications-fall-2006/resources/lecture3
- Erdely Ruiz, A., & Gutiérrez Peña, E. *Monografía de estadística bayesiana*. Universidad Nacional Autónoma de
  México. arXiv:2309.06601. https://arxiv.org/abs/2309.06601
- Fisher, R. A. (1925). Theory of statistical estimation. *Mathematical Proceedings of the Cambridge Philosophical
  Society, 22*(5), 700–725. https://doi.org/10.1017/S0305004100009580
- Eertmans, J. (2023). Manim Slides: A Python package for presenting Manim content anywhere. *Journal of Open Source
  Education, 6*. https://doi.org/10.21105/jose.00206
