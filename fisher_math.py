"""
Funciones numéricas puras (sin Manim) que usan las diapositivas.

Se separan de `fisher_slides.py` para poder probarlas sin renderizar nada:
    python fisher_math.py
"""
import numpy as np

# Proporción observada que se usa en la animación de motivación
P_HAT = 0.3
# Cota inferior del eje y (log-verosimilitud relativa) en esa animación
Y_MIN = -6.0

_GRID = np.linspace(0.001, 0.999, 4000)


def info_bernoulli(p):
    """Información de Fisher de una observación Bernoulli(p): 1 / (p (1 - p))."""
    return 1.0 / (p * (1.0 - p))


def ll_rel(p, n, ph=P_HAT):
    """
    Log-verosimilitud relativa  l(p) - l(p_hat)  para n ensayos Bernoulli con
    proporción observada ph (k = n * ph éxitos):

        n * [ ph * log(p/ph) + (1-ph) * log((1-p)/(1-ph)) ]

    Es <= 0 y vale 0 en p = ph. Su curvatura en ph es  -n / (ph (1-ph)) = -n I(ph).
    """
    p = np.asarray(p, dtype=float)
    return n * (ph * np.log(p / ph) + (1 - ph) * np.log((1 - p) / (1 - ph)))


def rango_visible(n, ph=P_HAT, y_min=Y_MIN):
    """Intervalo de p donde la log-verosimilitud relativa es >= y_min."""
    visible = ll_rel(_GRID, n, ph) >= y_min
    return float(_GRID[visible].min()), float(_GRID[visible].max())


def pdf_normal(x, m, s):
    """Densidad de N(m, s^2)."""
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))


def simular_z(n, p=0.3, reps=20_000, semilla=7):
    """
    Simula `reps` valores de  Z = sqrt(n I(p)) (p_hat - p)  con p_hat = Binomial(n, p)/n.
    Cuando n crece, Z se parece cada vez más a una N(0, 1).
    """
    rng = np.random.default_rng(semilla + n)
    p_hat = rng.binomial(n, p, size=reps) / n
    return (p_hat - p) * np.sqrt(n * info_bernoulli(p))


def densidades_hist(z, bins):
    """Alturas (densidad) de un histograma sobre `bins`."""
    dens, _ = np.histogram(z, bins=bins, density=True)
    return dens


if __name__ == "__main__":
    # --- Pruebas rápidas -----------------------------------------------------
    # 1) Curvatura de la log-verosimilitud en el MLE = n * I(p_hat)
    n, h = 50, 1e-4
    segunda = (ll_rel(P_HAT + h, n) - 2 * ll_rel(P_HAT, n) + ll_rel(P_HAT - h, n)) / h**2
    esperada = -n * info_bernoulli(P_HAT)
    print(f"curvatura numérica = {segunda:9.2f} | -n I(p_hat) = {esperada:9.2f}")
    assert abs(segunda - esperada) / abs(esperada) < 1e-3

    # 2) Información de Fisher = Var(score) por Monte Carlo
    rng = np.random.default_rng(0)
    p = 0.3
    x = rng.binomial(1, p, size=2_000_000)
    score = x / p - (1 - x) / (1 - p)
    print(f"E[score] = {score.mean():+.4f} (teoría 0) | Var(score) = {score.var():.3f} "
          f"| 1/(p(1-p)) = {info_bernoulli(p):.3f}")
    assert abs(score.mean()) < 5e-3 and abs(score.var() - info_bernoulli(p)) < 0.05

    # 3) Cota de Cramér-Rao: Var(MLE) = 1/(n I) y la "mitad de los datos" duplica la varianza
    n = 50
    reps = 400_000
    mle = rng.binomial(n, p, size=reps) / n
    mitad = rng.binomial(n // 2, p, size=reps) / (n // 2)
    cota = 1 / (n * info_bernoulli(p))
    print(f"Var(MLE) = {mle.var():.6f} | cota = {cota:.6f} | Var(mitad) = {mitad.var():.6f} "
          f"| 2*cota = {2 * cota:.6f}")
    assert abs(mle.var() / cota - 1) < 0.02 and abs(mitad.var() / (2 * cota) - 1) < 0.02

    # 4) El rango visible de la curva es razonable y las alturas del histograma caben en el eje
    for n in (10, 50, 200):
        lo, hi = rango_visible(n)
        print(f"n={n:4d}: rango visible de p = [{lo:.3f}, {hi:.3f}]")
        assert 0 < lo < P_HAT < hi < 1
    bins = np.linspace(-4, 4, 33)
    for n in (5, 20, 100, 1000):
        d = densidades_hist(simular_z(n), bins)
        print(f"n={n:4d}: altura máxima del histograma = {d.max():.2f} (eje y llega a 1.6)")
        assert d.max() < 1.6
    print("OK")
