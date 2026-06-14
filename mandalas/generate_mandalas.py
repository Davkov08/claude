import math

SIZE = 800
CX = CY = SIZE / 2


def petal(cx, cy, length, base_w, bulge, angle_deg, r0=0):
    """A pointed petal shape pointing outward from (cx,cy) along angle_deg.
    r0 = starting radius (base offset from center), length = tip radius."""
    rad = math.radians(angle_deg)
    perp = rad + math.pi / 2
    bx, by = cx + r0 * math.cos(rad), cy + r0 * math.sin(rad)
    tipx, tipy = cx + length * math.cos(rad), cy + length * math.sin(rad)
    p1x, p1y = bx + base_w * math.cos(perp), by + base_w * math.sin(perp)
    p2x, p2y = bx - base_w * math.cos(perp), by - base_w * math.sin(perp)
    mid_r = (r0 + length) / 2
    c1x = cx + mid_r * math.cos(rad) + bulge * math.cos(perp)
    c1y = cy + mid_r * math.sin(rad) + bulge * math.sin(perp)
    c2x = cx + mid_r * math.cos(rad) - bulge * math.cos(perp)
    c2y = cy + mid_r * math.sin(rad) - bulge * math.sin(perp)
    return (f"M {p1x:.2f} {p1y:.2f} "
            f"Q {c1x:.2f} {c1y:.2f} {tipx:.2f} {tipy:.2f} "
            f"Q {c2x:.2f} {c2y:.2f} {p2x:.2f} {p2y:.2f} Z")


def ring_of_petals(cx, cy, n, length, base_w, bulge, r0=0, start=0):
    paths = []
    for i in range(n):
        ang = start + i * 360 / n
        paths.append(f'<path d="{petal(cx, cy, length, base_w, bulge, ang, r0)}" />')
    return "\n".join(paths)


def circle(cx, cy, r):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" />'


def ring_of_circles(cx, cy, n, radius, dot_r, start=0):
    out = []
    for i in range(n):
        ang = math.radians(start + i * 360 / n)
        x, y = cx + radius * math.cos(ang), cy + radius * math.sin(ang)
        out.append(circle(x, y, dot_r))
    return "\n".join(out)


def polygon(cx, cy, n, r, start=0):
    pts = []
    for i in range(n):
        ang = math.radians(start + i * 360 / n)
        pts.append(f"{cx + r * math.cos(ang):.2f},{cy + r * math.sin(ang):.2f}")
    return f'<polygon points="{" ".join(pts)}" />'


def ray_triangle(cx, cy, r0, r1, half_w_deg, angle_deg):
    a = math.radians(angle_deg)
    a1 = math.radians(angle_deg - half_w_deg)
    a2 = math.radians(angle_deg + half_w_deg)
    tip = (cx + r1 * math.cos(a), cy + r1 * math.sin(a))
    b1 = (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))
    b2 = (cx + r0 * math.cos(a2), cy + r0 * math.sin(a2))
    return f'<polygon points="{b1[0]:.2f},{b1[1]:.2f} {tip[0]:.2f},{tip[1]:.2f} {b2[0]:.2f},{b2[1]:.2f}" />'


def ring_of_rays(cx, cy, n, r0, r1, half_w_deg, start=0):
    out = []
    for i in range(n):
        ang = start + i * 360 / n
        out.append(ray_triangle(cx, cy, r0, r1, half_w_deg, ang))
    return "\n".join(out)


def scalloped_circle(cx, cy, R, n, bump_r, outward=True):
    pts = []
    for i in range(n):
        ang = math.radians(i * 360 / n)
        pts.append((cx + R * math.cos(ang), cy + R * math.sin(ang)))
    sweep = 1 if outward else 0
    d = f"M {pts[0][0]:.2f} {pts[0][1]:.2f} "
    for i in range(1, n + 1):
        nx, ny = pts[i % n]
        d += f"A {bump_r:.2f} {bump_r:.2f} 0 0 {sweep} {nx:.2f} {ny:.2f} "
    d += "Z"
    return f'<path d="{d}" />'


def svg_wrap(body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">
<title>{title}</title>
<rect width="{SIZE}" height="{SIZE}" fill="white"/>
<g fill="none" stroke="black" stroke-width="2" stroke-linejoin="round">
{body}
</g>
</svg>'''


# ---------------------------------------------------------------------------
# Mandala 1: Flower mandala (simple, beginner-friendly, 8-fold)
# ---------------------------------------------------------------------------
def mandala1():
    body = []
    body.append(circle(CX, CY, 360))
    body.append(circle(CX, CY, 350))
    body.append(scalloped_circle(CX, CY, 330, 24, 22, outward=True))
    body.append(ring_of_petals(CX, CY, 8, 320, 55, 90, r0=150, start=22.5))
    body.append(ring_of_petals(CX, CY, 8, 230, 45, 60, r0=130, start=0))
    body.append(ring_of_circles(CX, CY, 16, 140, 14, start=11.25))
    body.append(ring_of_petals(CX, CY, 8, 120, 35, 45, r0=20, start=0))
    body.append(circle(CX, CY, 60))
    body.append(circle(CX, CY, 45))
    body.append(ring_of_circles(CX, CY, 8, 30, 8, start=22.5))
    body.append(circle(CX, CY, 12))
    return svg_wrap("\n".join(body), "Mandala 1 - Flower")


# ---------------------------------------------------------------------------
# Mandala 2: Geometric star mandala (12-fold)
# ---------------------------------------------------------------------------
def mandala2():
    body = []
    body.append(circle(CX, CY, 370))
    body.append(circle(CX, CY, 355))
    body.append(ring_of_rays(CX, CY, 12, 290, 350, 9, start=15))
    body.append(circle(CX, CY, 290))
    body.append(polygon(CX, CY, 24, 270, start=0))
    body.append(polygon(CX, CY, 12, 220, start=0))
    body.append(polygon(CX, CY, 12, 220, start=15))
    body.append(circle(CX, CY, 200))
    body.append(ring_of_rays(CX, CY, 12, 120, 195, 12, start=0))
    body.append(circle(CX, CY, 120))
    body.append(ring_of_circles(CX, CY, 12, 95, 12, start=15))
    body.append(polygon(CX, CY, 6, 70, start=0))
    body.append(polygon(CX, CY, 6, 70, start=30))
    body.append(circle(CX, CY, 35))
    body.append(circle(CX, CY, 15))
    return svg_wrap("\n".join(body), "Mandala 2 - Geometric Star")


# ---------------------------------------------------------------------------
# Mandala 3: Lotus mandala (layered petal rings, 12-fold)
# ---------------------------------------------------------------------------
def mandala3():
    body = []
    body.append(circle(CX, CY, 370))
    body.append(scalloped_circle(CX, CY, 350, 36, 18, outward=True))
    body.append(ring_of_petals(CX, CY, 12, 330, 38, 55, r0=240, start=0))
    body.append(ring_of_petals(CX, CY, 12, 250, 42, 60, r0=150, start=15))
    body.append(ring_of_petals(CX, CY, 12, 170, 36, 50, r0=80, start=0))
    body.append(circle(CX, CY, 90))
    body.append(ring_of_petals(CX, CY, 8, 75, 24, 32, r0=15, start=0))
    body.append(circle(CX, CY, 18))
    body.append(ring_of_circles(CX, CY, 12, 300, 9, start=15))
    body.append(ring_of_circles(CX, CY, 12, 200, 8, start=0))
    return svg_wrap("\n".join(body), "Mandala 3 - Lotus")


# ---------------------------------------------------------------------------
# Mandala 4: Sunburst / paisley mandala (6-fold with swirling teardrops)
# ---------------------------------------------------------------------------
def teardrop(cx, cy, r, size, angle_deg):
    """A swirling teardrop (paisley-like) shape."""
    a = math.radians(angle_deg)
    x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
    a2 = math.radians(angle_deg + 70)
    x1, y1 = x0 + size * math.cos(a2), y0 + size * math.sin(a2)
    a3 = math.radians(angle_deg + 140)
    cxp, cyp = x0 + size * 1.4 * math.cos(a3), y0 + size * 1.4 * math.sin(a3)
    return (f"M {x0:.2f} {y0:.2f} "
            f"C {x0 + size*math.cos(a2)*0.6:.2f} {y0 + size*math.sin(a2)*0.6:.2f} "
            f"{x1:.2f} {y1:.2f} {x1:.2f} {y1:.2f} "
            f"C {x1 + size*0.8*math.cos(a3):.2f} {y1 + size*0.8*math.sin(a3):.2f} "
            f"{cxp:.2f} {cyp:.2f} {x0:.2f} {y0:.2f} Z")


def mandala4():
    body = []
    body.append(circle(CX, CY, 375))
    body.append(circle(CX, CY, 360))
    body.append(ring_of_circles(CX, CY, 36, 345, 8, start=0))
    body.append(ring_of_rays(CX, CY, 24, 250, 340, 5, start=7.5))
    body.append(circle(CX, CY, 250))
    for i in range(6):
        ang = i * 60
        body.append(f'<path d="{teardrop(CX, CY, 80, 90, ang)}" />')
    body.append(ring_of_petals(CX, CY, 6, 230, 30, 70, r0=100, start=30))
    body.append(circle(CX, CY, 120))
    body.append(ring_of_circles(CX, CY, 18, 105, 8, start=0))
    body.append(ring_of_petals(CX, CY, 6, 95, 26, 35, r0=20, start=0))
    body.append(circle(CX, CY, 30))
    body.append(circle(CX, CY, 12))
    return svg_wrap("\n".join(body), "Mandala 4 - Sunburst Paisley")


if __name__ == "__main__":
    designs = {
        "mandala1_flower.svg": mandala1(),
        "mandala2_geometric.svg": mandala2(),
        "mandala3_lotus.svg": mandala3(),
        "mandala4_sunburst.svg": mandala4(),
    }
    for name, content in designs.items():
        with open(name, "w") as f:
            f.write(content)
        print("wrote", name)
