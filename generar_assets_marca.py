# Genera los recursos graficos de marca a partir de marca/logotipo fondo azul.png
# - img/logo-blanco.png: logo con fondo transparente (para fondos oscuros)
# - img/logo-azul.png:   logo con fondo transparente (para fondos claros)
# - icon-192.png / icon-512.png: icono de la app con el isotipo "T"
from PIL import Image, ImageDraw

NAVY = (22, 34, 87)
CYAN = (0, 170, 224)
WHITE = (255, 255, 255)
BG_LOGO = (20, 34, 87)
CYAN_LOGO = (1, 170, 224)
AR_START_X = 790  # donde empieza el "AR" en cian dentro del PNG original


def extraer_logo():
    src = Image.open('marca/logotipo fondo azul.png').convert('RGB')
    w, h = src.size
    px = src.load()
    claro = Image.new('RGBA', (w, h))
    oscuro = Image.new('RGBA', (w, h))
    pc, po = claro.load(), oscuro.load()
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            es_ar = x >= AR_START_X and y < 330
            fg = CYAN_LOGO if es_ar else WHITE
            d = [fg[i] - BG_LOGO[i] for i in range(3)]
            v = [p[i] - BG_LOGO[i] for i in range(3)]
            a = sum(d[i] * v[i] for i in range(3)) / sum(di * di for di in d)
            a = max(0.0, min(1.0, a))
            alpha = round(a * 255)
            pc[x, y] = (*(CYAN if es_ar else WHITE), alpha)
            po[x, y] = (*(CYAN if es_ar else NAVY), alpha)
    caja = claro.getbbox()
    margen = 6
    caja = (caja[0] - margen, caja[1] - margen, caja[2] + margen, caja[3] + margen)
    claro.crop(caja).save('img/logo-blanco.png', optimize=True)
    oscuro.crop(caja).save('img/logo-azul.png', optimize=True)


def dibujar_isotipo(draw, s, ox, oy, color_borde, color_lineas):
    # Isotipo en grilla de 100x100: una T formada por los bordes de dos calles
    # que se cruzan, con lineas punteadas de carril.
    def r(x0, y0, x1, y1, c):
        draw.rectangle([ox + x0 * s, oy + y0 * s, ox + x1 * s, oy + y1 * s], fill=c)
    b = 9  # grosor del borde
    r(0, 0, 100, b, color_borde)                  # borde superior de la calle horizontal
    r(0, 30 - b, 32 + b, 30, color_borde)         # borde inferior izquierdo
    r(68 - b, 30 - b, 100, 30, color_borde)       # borde inferior derecho
    r(32, 30 - b, 32 + b, 100, color_borde)       # borde izquierdo de la calle vertical
    r(68 - b, 30 - b, 68, 100, color_borde)       # borde derecho de la calle vertical
    for x0 in (2, 17, 73, 88):                    # carril horizontal
        r(x0, 12.5, x0 + 10, 17.5, color_lineas)
    for y0 in (8, 26, 44, 62, 80):                # carril vertical
        r(47.5, y0, 52.5, y0 + 10, color_lineas)


def generar_icono(size):
    ss = 4
    S = size * ss
    img = Image.new('RGBA', (S, S), NAVY + (255,))
    d = ImageDraw.Draw(img)
    lado = S * 0.6  # deja margen para iconos "maskable" de Android
    escala = lado / 100
    origen = (S - lado) / 2
    dibujar_isotipo(d, escala, origen, origen, WHITE, CYAN)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(f'icon-{size}.png', optimize=True)


if __name__ == '__main__':
    extraer_logo()
    for tam in (192, 512):
        generar_icono(tam)
    print('Listo: img/logo-blanco.png, img/logo-azul.png, icon-192.png, icon-512.png')
