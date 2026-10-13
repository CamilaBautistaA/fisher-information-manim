"""
Información de Fisher: presentación con Manim + manim-slides.

Uso rápido (ver README.md para los detalles):

    manim-slides render fisher_slides.py FisherInformation -ql   # prueba rápida
    manim-slides render fisher_slides.py FisherInformation -qh   # calidad final
    manim-slides present FisherInformation                       # presentar
    manim-slides convert FisherInformation docs/index.html --one-file   # HTML (GitHub Pages)

Las fuentes de cada diapositiva están en BIBLIOGRAFIA.md.
"""
import os
import sys

import numpy as np
from manim import *
from manim_slides import Slide

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fisher_math import (  # noqa: E402
    P_HAT,
    Y_MIN,
    densidades_hist,
    ll_rel,
    pdf_normal,
    rango_visible,
    simular_z,
)

# --------------------------------------------------------------------------- #
#  Personaliza aquí
# --------------------------------------------------------------------------- #
AUTOR = "Tu nombre"
INSTITUCION = "Tu universidad"
CURSO = "Inferencia Estadística"
REPO = "github.com/tu-usuario/fisher-information-slides"

FONDO = "#10131a"
C_DATOS = BLUE_C      # score / log-verosimilitud
C_FISHER = YELLOW     # información de Fisher
C_CR = GREEN_C        # Cramér-Rao / MLE
C_ALT = ORANGE        # estimador alternativo

# Notas del presentador (se ven en `manim-slides present` y en el HTML).
# La clave es la que se pasa a self.pausa(...): las notas describen la diapositiva que SIGUE.
NOTAS = {
    "motivacion": "Pregunta guía: ¿cuánta información trae una muestra sobre el parámetro? "
                  "Ejemplo: n lanzamientos de una moneda con proporción observada 0.3.",
    "motivacion.curva": "Log-verosimilitud relativa con n = 10: muy plana. Muchos valores de p "
                        "explican casi igual de bien los datos.",
    "motivacion.n": "Al crecer n la curva se afila. La curvatura en el máximo es n / (p(1-p)) = n·I(p). "
                    "Esa curvatura es lo que la información de Fisher cuantifica.",
    "score": "Definimos la función score: la derivada de la log-verosimilitud respecto a θ.",
    "score.cero": "Propiedad clave: el score tiene esperanza cero (bajo regularidad). "
                  "Se deriva de que la densidad integra 1.",
    "informacion": "Entonces la información de Fisher es la varianza del score.",
    "informacion.curv": "Forma equivalente: menos la esperanza de la segunda derivada. "
                        "Es la curvatura esperada que vimos en la primera animación.",
    "bernoulli": "Ejemplo completo con Bernoulli(p): log f, score, segunda derivada.",
    "bernoulli.grafica": "I(p) = 1/(p(1-p)). Mínima en p = 1/2 y crece hacia los extremos.",
    "propiedades": "Aditividad: n observaciones iid dan n veces la información de una.",
    "propiedades.2": "Reparametrización: la información cambia con el cuadrado de la derivada del cambio de variable.",
    "propiedades.3": "Ejemplo Normal con σ conocido: más ruido, menos información.",
    "cramer_rao": "Cota de Cramér-Rao: ningún estimador insesgado baja de 1/(n I(θ)).",
    "cramer_rao.curvas": "El MLE de p (media muestral) alcanza la cota.",
    "cramer_rao.mitad": "Un estimador que usa solo la mitad de los datos tiene la mitad de la información "
                        "y el doble de varianza.",
    "normalidad": "El MLE, además, es asintóticamente normal con varianza 1/(n I(θ)).",
    "normalidad.sim": "Simulación: 20 000 muestras Bernoulli(p = 0.3) y el histograma de "
                      "Z = sqrt(n I(p)) (p_hat - p). Con n = 5 es discreto y asimétrico.",
    "normalidad.n20": "n = 20: ya se ve la forma de campana.",
    "normalidad.n100": "n = 100.",
    "normalidad.n1000": "n = 1000: el histograma se pega a la N(0,1). "
                        "La varianza límite es justo la cota de Cramér-Rao.",
    "resumen": "Resumen de las cinco ideas.",
    "referencias": "Fuentes. Todo el material y la bibliografía está en el repositorio.",
}


# --------------------------------------------------------------------------- #
#  Utilidades de dibujo
# --------------------------------------------------------------------------- #
def texto(s, size=34, color=WHITE, **kw):
    return Text(s, font_size=size, color=color, **kw)


def titulo(s):
    t = Text(s, font_size=40, weight="BOLD")
    ajustar(t)
    return t.to_edge(UP, buff=0.5)


def ajustar(m, ancho=12.8):
    """Reduce el objeto si se sale del encuadre."""
    if m.width > ancho:
        m.scale_to_fit_width(ancho)
    return m


def etiquetas_x(ejes, valores, y, fmt="{:.2f}", size=24):
    """Marcas y números del eje x dibujados a la altura `y` (coordenadas del eje)."""
    g = VGroup()
    for v in valores:
        p = ejes.c2p(v, y)
        g.add(Line(p + DOWN * 0.07, p + UP * 0.07, stroke_width=2, color=GREY_B))
        g.add(MathTex(fmt.format(v), font_size=size, color=GREY_B).next_to(p, DOWN, buff=0.15))
    return g


def linea_base(ejes, y, color=GREY_B):
    return Line(ejes.c2p(ejes.x_range[0], y), ejes.c2p(ejes.x_range[1], y),
                stroke_width=2, color=color)


def barras_hist(ejes, datos, bins, color):
    """Histograma (densidad) como grupo de rectángulos; mismo nº de barras para poder hacer Transform."""
    barras = VGroup()
    for h, a, b in zip(densidades_hist(datos, bins), bins[:-1], bins[1:]):
        p0 = ejes.c2p(a, 0)
        p1 = ejes.c2p(b, max(h, 1e-3))
        r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0.8,
                      stroke_color=WHITE, fill_color=color, fill_opacity=0.65)
        r.move_to((p0 + p1) / 2)
        barras.add(r)
    return barras


def entrada_leyenda(color, *lineas):
    muestra = Line(LEFT * 0.35, RIGHT * 0.35, color=color, stroke_width=6)
    cuerpo = VGroup(*lineas).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    return VGroup(muestra, cuerpo).arrange(RIGHT, buff=0.25, aligned_edge=UP)


# --------------------------------------------------------------------------- #
#  La presentación
# --------------------------------------------------------------------------- #
class FisherInformation(Slide):
    def construct(self):
        self.camera.background_color = FONDO
        secciones = [
            ("portada", self.s_portada),
            ("motivacion", self.s_motivacion),
            ("score", self.s_score),
            ("informacion", self.s_informacion),
            ("bernoulli", self.s_bernoulli),
            ("propiedades", self.s_propiedades),
            ("cramer_rao", self.s_cramer_rao),
            ("normalidad", self.s_normalidad),
            ("resumen", self.s_resumen),
            ("referencias", self.s_referencias),
        ]
        for i, (clave, seccion) in enumerate(secciones):
            if i > 0:
                self.pausa(clave)   # nueva diapositiva (con sus notas)
                self.limpiar()      # el FadeOut ocurre al inicio de la nueva diapositiva
            seccion()

    # ----------------------------------------------------------------- utilidades de flujo
    def pausa(self, clave=""):
        notas = NOTAS.get(clave, "")
        try:
            self.next_slide(notes=notas)
        except TypeError:  # versiones antiguas de manim-slides sin el argumento `notes`
            self.next_slide()

    def limpiar(self):
        vivos = [m for m in self.mobjects if not isinstance(m, ValueTracker)]
        for m in vivos:
            m.clear_updaters()
        if vivos:
            self.play(*[FadeOut(m) for m in vivos], run_time=0.6)

    # ----------------------------------------------------------------- 1. Portada
    def s_portada(self):
        t = Text("Información de Fisher", font_size=68, weight="BOLD", color=C_FISHER)
        sub = texto(CURSO, 32, GREY_B)
        VGroup(t, sub).arrange(DOWN, buff=0.35).move_to(UP * 1.9)
        formula = MathTex(
            r"I(\theta)=\operatorname{Var}_\theta\!\left(\frac{\partial}{\partial\theta}\log f(X;\theta)\right)",
            font_size=46,
        ).move_to(DOWN * 0.6)
        autor = texto(f"{AUTOR} · {INSTITUCION}", 26, GREY_B).to_edge(DOWN, buff=0.7)

        self.play(Write(t), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.play(Write(formula), run_time=2)
        self.play(FadeIn(autor))

    # ----------------------------------------------------------------- 2. Motivación
    def s_motivacion(self):
        tit = titulo("¿Cuánta información trae la muestra sobre θ?")
        idea = VGroup(
            texto("Lanzamos una moneda n veces y observamos una proporción de éxitos", 30),
            MathTex(r"\hat p = k/n = 0.3", font_size=44),
            MathTex(r"\ell(p)=k\log p+(n-k)\log(1-p)", font_size=44, color=C_DATOS),
        ).arrange(DOWN, buff=0.5).move_to(DOWN * 0.3)
        ajustar(idea)
        self.play(Write(tit))
        self.play(FadeIn(idea, lag_ratio=0.4), run_time=2)

        # --- Gráfica de la log-verosimilitud relativa -----------------------------
        self.pausa("motivacion.curva")
        self.play(FadeOut(idea))

        ejes = Axes(x_range=[0, 1, 0.25], y_range=[Y_MIN, 1, 2], x_length=7.5, y_length=4.0, tips=False)
        ejes.x_axis.set_opacity(0)            # usamos nuestra propia base abajo
        ejes.to_edge(LEFT, buff=1.0).shift(DOWN * 0.6)
        base = VGroup(linea_base(ejes, Y_MIN), etiquetas_x(ejes, [0, 0.25, 0.5, 0.75, 1], Y_MIN))
        x_lab = MathTex("p", font_size=32).next_to(ejes.c2p(1, Y_MIN), RIGHT, buff=0.3)
        y_lab = MathTex(r"\ell(p)-\ell(\hat p)", font_size=30).next_to(ejes.y_axis, UP, buff=0.2)
        punto = Dot(ejes.c2p(P_HAT, 0), color=C_FISHER)
        guia = DashedLine(ejes.c2p(P_HAT, Y_MIN), ejes.c2p(P_HAT, 0), color=C_FISHER, stroke_width=2)
        p_lab = MathTex(r"\hat p=0.3", font_size=28, color=C_FISHER).next_to(punto, UP, buff=0.12)

        def curva_para(nv):
            lo, hi = rango_visible(nv)
            return ejes.plot(lambda p: float(ll_rel(p, nv)), x_range=[lo, hi, (hi - lo) / 250],
                             color=C_DATOS, stroke_width=5, use_smoothing=False)

        n = ValueTracker(10)
        et_n = MathTex("n=", font_size=44).move_to(RIGHT * 3.6 + UP * 1.5)
        val_n = DecimalNumber(10, num_decimal_places=0, font_size=44).next_to(et_n, RIGHT, buff=0.15)
        et_c = MathTex(r"-\ell''(\hat p)=", font_size=40).move_to(RIGHT * 3.4 + UP * 0.2)
        val_c = DecimalNumber(10 / (P_HAT * (1 - P_HAT)), num_decimal_places=0, font_size=40,
                              color=C_FISHER).next_to(et_c, RIGHT, buff=0.15)
        igual = MathTex(r"=\;n\,I(\hat p)", font_size=40, color=C_FISHER).next_to(et_c, DOWN, buff=0.35)
        igual.align_to(et_c, LEFT)

        c0 = curva_para(10)
        self.play(Create(ejes), FadeIn(base), FadeIn(x_lab), FadeIn(y_lab))
        self.play(Create(c0), FadeIn(punto), Create(guia), FadeIn(p_lab))
        self.play(FadeIn(VGroup(et_n, val_n, et_c, val_c, igual)))

        # --- n crece: la curva se afila y la curvatura aumenta --------------------
        self.pausa("motivacion.n")
        dinamica = always_redraw(lambda: curva_para(n.get_value()))
        self.remove(c0)
        self.add(dinamica)
        val_n.add_updater(lambda m: m.set_value(n.get_value()).next_to(et_n, RIGHT, buff=0.15))
        val_c.add_updater(lambda m: m.set_value(n.get_value() / (P_HAT * (1 - P_HAT)))
                          .next_to(et_c, RIGHT, buff=0.15))
        self.play(n.animate.set_value(200), run_time=6, rate_func=smooth)

        msg = texto("Más curvatura → el parámetro queda mejor determinado → más información",
                    28, C_FISHER)
        ajustar(msg).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(msg))

    # ----------------------------------------------------------------- 3. Score
    def s_score(self):
        tit = titulo("Función score")
        modelo = MathTex(r"X\sim f(x;\theta),\qquad \theta\in\mathbb{R}", font_size=42).move_to(UP * 2.0)
        s_def = MathTex(r"S(\theta)=\frac{\partial}{\partial\theta}\log f(X;\theta)",
                        font_size=54, color=C_DATOS).move_to(UP * 0.3)
        nota = texto("Mide qué tan sensible es la log-verosimilitud a un cambio en θ",
                     28, GREY_B).move_to(DOWN * 1.2)
        self.play(Write(tit))
        self.play(FadeIn(modelo))
        self.play(Write(s_def))
        self.play(FadeIn(nota))

        self.pausa("score.cero")
        cero = MathTex(r"\mathbb{E}_\theta\big[S(\theta)\big]=0", font_size=52, color=C_FISHER).move_to(UP * 0.4)
        prueba = MathTex(
            r"\mathbb{E}[S]=\int\frac{\partial_\theta f}{f}\,f\,dx"
            r"=\frac{d}{d\theta}\int f\,dx=\frac{d}{d\theta}\,1=0",
            font_size=34,
        ).move_to(DOWN * 1.1)
        ajustar(prueba)
        reg = texto("Condiciones de regularidad: el soporte de f no depende de θ y se puede derivar "
                    "bajo la integral.", 22, GREY_B)
        ajustar(reg).move_to(DOWN * 3.1)
        self.play(FadeOut(modelo), FadeOut(nota), s_def.animate.move_to(UP * 1.9))
        self.play(Write(cero))
        self.play(Write(prueba), run_time=3)
        self.play(FadeIn(reg))

    # ----------------------------------------------------------------- 4. Información de Fisher
    def s_informacion(self):
        tit = titulo("Información de Fisher")
        d1 = MathTex(
            r"I(\theta)=\operatorname{Var}_\theta\big(S(\theta)\big)="
            r"\mathbb{E}_\theta\!\left[\left(\frac{\partial}{\partial\theta}\log f(X;\theta)\right)^{2}\right]",
            font_size=44,
        )
        ajustar(d1).move_to(UP * 1.7)
        c1 = texto("Varianza del score", 28, C_DATOS).next_to(d1, DOWN, buff=0.3)
        d2 = MathTex(
            r"I(\theta)=-\,\mathbb{E}_\theta\!\left[\frac{\partial^{2}}{\partial\theta^{2}}\log f(X;\theta)\right]",
            font_size=50, color=C_FISHER,
        ).move_to(DOWN * 0.8)
        c2 = texto("Curvatura esperada de la log-verosimilitud", 28, C_FISHER).next_to(d2, DOWN, buff=0.3)
        caja = SurroundingRectangle(d2, color=C_FISHER, buff=0.25)
        nota = texto("(segunda forma: si se puede derivar dos veces bajo la integral)", 22, GREY_B)
        nota.to_edge(DOWN, buff=0.5)

        self.play(Write(tit))
        self.play(Write(d1), run_time=2.5)
        self.play(FadeIn(c1))

        self.pausa("informacion.curv")
        self.play(Write(d2), run_time=2)
        self.play(FadeIn(c2), Create(caja))
        self.play(FadeIn(nota))

    # ----------------------------------------------------------------- 5. Ejemplo Bernoulli
    def s_bernoulli(self):
        tit = titulo("Ejemplo: Bernoulli(p)")
        l1 = MathTex(r"\log f(x;p)=x\log p+(1-x)\log(1-p)", font_size=42)
        l2 = MathTex(r"S(p)=\frac{x}{p}-\frac{1-x}{1-p}", font_size=42, color=C_DATOS)
        l3 = MathTex(r"\frac{\partial^{2}}{\partial p^{2}}\log f(x;p)=-\frac{x}{p^{2}}-\frac{1-x}{(1-p)^{2}}",
                     font_size=42)
        l4 = MathTex(r"I(p)=-\mathbb{E}\big[\,\cdot\,\big]=\frac{p}{p^{2}}+\frac{1-p}{(1-p)^{2}}"
                     r"=\frac{1}{p(1-p)}", font_size=42, color=C_FISHER)
        lineas = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.45)
        ajustar(lineas, 12.5).next_to(tit, DOWN, buff=0.6)

        self.play(Write(tit))
        for l in lineas:
            self.play(Write(l), run_time=1.6)

        # --- Gráfica de I(p) --------------------------------------------------------
        self.pausa("bernoulli.grafica")
        final = MathTex(r"I(p)=\frac{1}{p(1-p)}", font_size=56, color=C_FISHER)
        final.next_to(tit, DOWN, buff=0.35)
        ejes = Axes(x_range=[0, 1, 0.25], y_range=[0, 30, 10], x_length=8, y_length=3.4, tips=False)
        ejes.move_to(DOWN * 1.15)
        marcas = etiquetas_x(ejes, [0, 0.25, 0.5, 0.75, 1], 0)
        x_lab = MathTex("p", font_size=32).next_to(ejes.c2p(1, 0), RIGHT, buff=0.3)
        curva = ejes.plot(lambda p: 1 / (p * (1 - p)), x_range=[0.036, 0.964, 0.004],
                          color=C_FISHER, stroke_width=5, use_smoothing=False)
        minimo = Dot(ejes.c2p(0.5, 4), color=WHITE)
        et_min = MathTex(r"p=\tfrac{1}{2}:\ I=4", font_size=32).next_to(minimo, UP, buff=0.5)
        interp = texto("Cerca de 0 o 1, I(p) es grande: la varianza del MLE, p(1-p)/n, es pequeña", 24, GREY_B)
        ajustar(interp).to_edge(DOWN, buff=0.2)

        self.play(FadeOut(VGroup(l1, l2, l3)), ReplacementTransform(l4, final))
        self.play(Create(ejes), FadeIn(marcas), FadeIn(x_lab))
        self.play(Create(curva), run_time=2)
        self.play(FadeIn(minimo), FadeIn(et_min))
        self.play(FadeIn(interp))

    # ----------------------------------------------------------------- 6. Propiedades
    def s_propiedades(self):
        tit = titulo("Propiedades")
        filas = [
            ("Aditividad (muestra i.i.d.)",
             r"S_n=\sum_{i=1}^{n}S_i\ \Longrightarrow\ I_n(\theta)=\operatorname{Var}(S_n)=n\,I(\theta)"),
            ("Reparametrización",
             r"I(\varphi)=I(\theta)\left(\frac{d\theta}{d\varphi}\right)^{2}"),
            ("Ejemplo: Normal con σ conocido",
             r"X\sim N(\mu,\sigma^{2}):\qquad I(\mu)=\frac{1}{\sigma^{2}}"),
        ]
        grupos = VGroup(*[
            VGroup(texto(et, 30, C_DATOS), MathTex(f, font_size=40)).arrange(DOWN, buff=0.2)
            for et, f in filas
        ]).arrange(DOWN, buff=0.55).move_to(DOWN * 0.45)
        ajustar(grupos, 12.5)

        self.play(Write(tit))
        self.play(FadeIn(grupos[0], shift=UP * 0.2))
        self.pausa("propiedades.2")
        self.play(FadeIn(grupos[1], shift=UP * 0.2))
        self.pausa("propiedades.3")
        self.play(FadeIn(grupos[2], shift=UP * 0.2))

    # ----------------------------------------------------------------- 7. Cramér-Rao
    def s_cramer_rao(self):
        tit = titulo("Cota de Cramér–Rao")
        teorema = MathTex(
            r"\hat\theta\ \text{insesgado}\ \Longrightarrow\ "
            r"\operatorname{Var}_\theta(\hat\theta)\ \ge\ \frac{1}{n\,I(\theta)}",
            font_size=52,
        ).move_to(UP * 1.5)
        nota = texto("Ningún estimador insesgado puede tener varianza menor (bajo regularidad)",
                     28, GREY_B)
        ajustar(nota).move_to(DOWN * 0.3)
        self.play(Write(tit))
        self.play(Write(teorema), run_time=2.5)
        self.play(FadeIn(nota))

        # --- Comparación de dos estimadores de p ------------------------------------
        self.pausa("cramer_rao.curvas")
        p0, n0 = 0.3, 50
        sd1 = np.sqrt(p0 * (1 - p0) / n0)
        sd2 = sd1 * np.sqrt(2)

        ejes = Axes(x_range=[0.05, 0.55, 0.1], y_range=[0, 7, 1], x_length=8, y_length=3.3, tips=False)
        ejes.move_to(LEFT * 2.0 + DOWN * 0.95)
        marcas = etiquetas_x(ejes, [0.1, 0.2, 0.3, 0.4, 0.5], 0, fmt="{:.1f}")
        c1 = ejes.plot(lambda x: float(pdf_normal(x, p0, sd1)), x_range=[0.05, 0.55, 0.004],
                       color=C_CR, stroke_width=5, use_smoothing=False)
        c2 = ejes.plot(lambda x: float(pdf_normal(x, p0, sd2)), x_range=[0.05, 0.55, 0.004],
                       color=C_ALT, stroke_width=5, use_smoothing=False)
        verdadero = DashedLine(ejes.c2p(p0, 0), ejes.c2p(p0, 7), color=GREY_B, stroke_width=2)
        pie = texto("Aproximación normal, n = 50, p = 0.3", 22, GREY_B).to_edge(DOWN, buff=0.25)

        e1 = entrada_leyenda(
            C_CR,
            MathTex(r"\hat p=\bar X_n\ \ (\mathrm{MLE})", font_size=34),
            MathTex(r"\operatorname{Var}=\frac{p(1-p)}{n}=\frac{1}{n\,I(p)}", font_size=34),
        )
        e2 = entrada_leyenda(
            C_ALT,
            MathTex(r"\tilde p=\frac{2}{n}\sum_{i\le n/2}X_i", font_size=34),
            texto("usa solo la mitad de los datos", 22, GREY_B),
            MathTex(r"\operatorname{Var}=\frac{2\,p(1-p)}{n}=\frac{2}{n\,I(p)}", font_size=34),
        )
        leyenda = VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        ajustar(leyenda, 4.6).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.1)

        self.play(
            teorema.animate.scale(0.75).move_to(UP * 2.1),
            FadeOut(nota),
        )
        self.play(Create(ejes), FadeIn(marcas), FadeIn(verdadero), FadeIn(pie))
        self.play(Create(c1), run_time=1.5)
        self.play(FadeIn(e1))

        self.pausa("cramer_rao.mitad")
        self.play(Create(c2), run_time=1.5)
        self.play(FadeIn(e2))

    # ----------------------------------------------------------------- 8. Normalidad asintótica
    def s_normalidad(self):
        tit = titulo("Normalidad asintótica del MLE")
        enunciado = MathTex(
            r"\sqrt{n\,I(\theta)}\,\big(\hat\theta_n-\theta\big)\ \xrightarrow{\ d\ }\ N(0,1)",
            font_size=50, color=C_FISHER,
        ).move_to(UP * 2.3)
        equiv = MathTex(r"\hat\theta_n\ \approx\ N\!\left(\theta,\ \frac{1}{n\,I(\theta)}\right)",
                        font_size=38).move_to(RIGHT * 4.7 + UP * 1.2)
        self.play(Write(tit))
        self.play(Write(enunciado), run_time=2)
        self.play(FadeIn(equiv))

        # --- Simulación: Z = sqrt(n I(p)) (p_hat - p) con p = 0.3 --------------------
        self.pausa("normalidad.sim")
        ejes = Axes(x_range=[-4, 4, 1], y_range=[0, 1.6, 0.4], x_length=8, y_length=3.4, tips=False)
        ejes.y_axis.set_opacity(0)
        ejes.move_to(LEFT * 1.8 + DOWN * 0.9)
        marcas = etiquetas_x(ejes, [-3, -2, -1, 0, 1, 2, 3], 0, fmt="{:.0f}")
        z_lab = MathTex("Z", font_size=32).next_to(ejes.c2p(4, 0), RIGHT, buff=0.3)
        normal = ejes.plot(lambda z: float(pdf_normal(z, 0, 1)), x_range=[-4, 4, 0.02],
                           color=C_FISHER, stroke_width=4, use_smoothing=False)
        nota_n01 = MathTex(r"\text{curva: }N(0,1)", font_size=32, color=C_FISHER).move_to(RIGHT * 4.7 + UP * 0.2)
        sim = texto("Histograma de 20 000 estimaciones\nBernoulli(p = 0.3)", 22, GREY_B)
        sim.move_to(RIGHT * 4.7 + DOWN * 2.3)

        bins = np.linspace(-4, 4, 33)
        ns = [5, 20, 100, 1000]
        barras = barras_hist(ejes, simular_z(ns[0]), bins, C_DATOS)
        etiqueta = MathTex(f"n={ns[0]}", font_size=46).move_to(RIGHT * 4.7 + DOWN * 0.9)

        self.play(Create(ejes), FadeIn(marcas), FadeIn(z_lab))
        self.play(Create(normal), FadeIn(nota_n01), FadeIn(sim))
        self.play(FadeIn(barras), FadeIn(etiqueta))

        for n_i, clave in zip(ns[1:], ["normalidad.n20", "normalidad.n100", "normalidad.n1000"]):
            self.pausa(clave)
            nuevas = barras_hist(ejes, simular_z(n_i), bins, C_DATOS)
            nueva_et = MathTex(f"n={n_i}", font_size=46).move_to(etiqueta)
            self.play(Transform(barras, nuevas), Transform(etiqueta, nueva_et), run_time=1.5)

        cierre = texto("La varianza límite 1/(n·I(θ)) es la cota de Cramér–Rao:\n"
                       "el MLE es asintóticamente eficiente", 24, C_CR)
        ajustar(cierre).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(cierre))

    # ----------------------------------------------------------------- 9. Resumen
    def s_resumen(self):
        tit = titulo("Resumen")
        filas = [
            ("Score", r"S(\theta)=\partial_\theta\log f(X;\theta),\quad \mathbb{E}[S]=0"),
            ("Información", r"I(\theta)=\operatorname{Var}(S)=-\mathbb{E}\big[\partial^{2}_\theta\log f\big]"),
            ("Muestra i.i.d.", r"I_n(\theta)=n\,I(\theta)"),
            ("Cramér–Rao", r"\operatorname{Var}(\hat\theta)\ \ge\ \frac{1}{n\,I(\theta)}"),
            ("MLE", r"\hat\theta_n\ \approx\ N\!\left(\theta,\ \frac{1}{n\,I(\theta)}\right)"),
        ]
        etiquetas = VGroup(*[texto(a, 28, C_FISHER) for a, _ in filas]).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        formulas = VGroup(*[MathTex(b, font_size=36) for _, b in filas])
        x_f = etiquetas.get_right()[0] + 0.8
        for f, e in zip(formulas, etiquetas):
            f.move_to([x_f + f.width / 2, e.get_center()[1], 0])
        cuerpo = VGroup(etiquetas, formulas)
        ajustar(cuerpo, 12.5).move_to(DOWN * 0.15)
        mas = texto("Más allá: intervalos de confianza (Wald) · a priori de Jeffreys · "
                    "complejidad de modelos (MDL)", 24, GREY_B)
        ajustar(mas).to_edge(DOWN, buff=0.35)

        self.play(Write(tit))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(e, shift=RIGHT * 0.2), Write(f))
                                for e, f in zip(etiquetas, formulas)], lag_ratio=0.5), run_time=6)
        self.play(FadeIn(mas))

    # ----------------------------------------------------------------- 10. Referencias
    def s_referencias(self):
        tit = titulo("Referencias")
        refs = [
            ("Ly, Marsman, Verhagen, Grasman & Wagenmakers (2017). A Tutorial on Fisher Information.",
             "Journal of Mathematical Psychology 80, 40–55 · arXiv:1705.01064"),
            ("MIT OpenCourseWare 18.443, Statistics for Applications (otoño 2006), Lecture 3.",
             "Propiedades del MLE: consistencia, normalidad asintótica e información de Fisher · ocw.mit.edu"),
            ("Erdely Ruiz & Gutiérrez Peña. Monografía de Estadística Bayesiana (UNAM), sección 3.4.",
             "Cota de Cramér–Rao, forma con la segunda derivada y regla de Jeffreys · arXiv:2309.06601"),
            ("Fisher, R. A. (1925). Theory of Statistical Estimation.",
             "Proc. Cambridge Philosophical Society 22(5), 700–725 · doi:10.1017/S0305004100009580"),
            ("Eertmans, J. (2023). Manim Slides: A Python package for presenting Manim content anywhere.",
             "Journal of Open Source Education 6 · doi:10.21105/jose.00206"),
        ]
        bloques = VGroup(*[
            VGroup(texto(a, 22), texto(b, 20, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            for a, b in refs
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        ajustar(bloques, 12.5).move_to(UP * 0.1)
        repo = texto(f"Código, animaciones y bibliografía completa: {REPO}", 22, C_DATOS)
        ajustar(repo).to_edge(DOWN, buff=0.4)

        self.play(Write(tit))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bloques], lag_ratio=0.4), run_time=4)
        self.play(FadeIn(repo))
