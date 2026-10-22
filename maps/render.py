"""Hac Nhat reusable SVG tactical atlas renderer (stdlib only; no game writes).

Only public, already-discovered atlas objects may be rendered. Coordinates 0..100
are schematic positions, not measured meters. No automatic gameplay actions.
"""
from __future__ import annotations

import argparse
import json
import math
from html import escape
from pathlib import Path

WIDTH, HEIGHT = 1100, 700
LEFT, TOP, MAP_W, MAP_H = 46, 100, 720, 520
FACINGS = {"N": 0, "NE": 45, "ENE": 67.5, "E": 90, "SE": 135,
           "S": 180, "SW": 225, "W": 270, "NW": 315}
KINDS = {"landmark", "point", "path", "cover", "hazard-terrain", "terrain",
         "structure", "door", "room", "clue"}


def _xy(x: float, y: float) -> tuple[float, float]:
    for value in (x, y):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError("Map coordinates must be finite numbers within 0..100")
    return LEFT + x * MAP_W / 100, TOP + y * MAP_H / 100


def _attr(value: object) -> str:
    return escape(str(value), quote=True)


def _line(x1: float, y1: float, x2: float, y2: float, **attrs: str) -> str:
    extra = " ".join(f'{key.replace("_", "-")}="{_attr(val)}"' for key, val in attrs.items())
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {extra}/>'


def render_map(atlas: dict, scene: dict | None, map_id: str) -> str:
    """Render one stable SVG. Does not mutate atlas, scene, game state or files."""
    if atlas.get("schema") != "HN-MAP-ATLAS-V1":
        raise ValueError("Unsupported atlas schema")
    matches = [m for m in atlas.get("maps", []) if m.get("id") == map_id]
    if len(matches) != 1:
        raise ValueError("Map ID missing or ambiguous")
    area = matches[0]
    if scene is not None:
        if scene.get("schema") != "HN-MAP-SCENE-V1" or scene.get("map_id") != map_id:
            raise ValueError("Scene must match this map (never relocate a token implicitly)")
        if type(scene.get("last_completed_turn")) is not int:
            raise ValueError("Missing completed turn")
    objects = area.get("objects", [])
    if len(objects) > 14:
        raise ValueError("Map has more than 14 markers; split into overview/local maps")
    identifiers = [obj.get("id") for obj in objects]
    if not all(identifiers) or len(identifiers) != len(set(identifiers)):
        raise ValueError("Static map object IDs must be unique")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{_attr(area["name"])}">',
        '<defs><marker id="routeArrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6Z" fill="#77b8d0"/></marker>',
        '<marker id="facingArrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6Z" fill="#c6ebfc"/></marker></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#152027"/>',
        f'<text x="46" y="51" font-family="sans-serif" font-size="28" font-weight="bold" fill="#f0e6d4">{escape(area["name"])}</text>',
        f'<text x="48" y="80" font-family="sans-serif" font-size="15" fill="#b7c6cc">HẮC NHẬT · SƠ ĐỒ TƯƠNG ĐỐI · KHÔNG DÙNG ĐO MÉT · revision {int(area.get("revision", 1))}</text>',
        f'<rect x="{LEFT}" y="{TOP}" width="{MAP_W}" height="{MAP_H}" rx="10" fill="#202d32" stroke="#687c82" stroke-width="2"/>',
    ]
    for n in range(1, 10):
        px = LEFT + MAP_W * n / 10
        py = TOP + MAP_H * n / 10
        parts.append(_line(px, TOP, px, TOP + MAP_H, stroke="#35454b", stroke_dasharray="3 7", stroke_width="1"))
        parts.append(_line(LEFT, py, LEFT + MAP_W, py, stroke="#35454b", stroke_dasharray="3 7", stroke_width="1"))

    if not objects and area.get("evidence_level") == "PLACEHOLDER":
        parts.append('<text x="410" y="362" font-family="sans-serif" font-size="20" text-anchor="middle" fill="#f0cc93">CHƯA CÓ BỐ CỤC ĐƯỢC XÁC MINH</text>')
    if area.get("evidence_level"):
        parts.append(f'<text x="824" y="94" font-family="sans-serif" font-size="13" fill="#b4c9d0">{escape(str(area["evidence_level"]))}</text>')

    # The static layer is defined by persistent object IDs. No inferred scenery.
    legend_rows = []
    for index, obj in enumerate(objects, 1):
        kind = obj.get("type")
        if kind not in KINDS:
            raise ValueError("Unsupported object type: " + str(kind))
        object_id = _attr(obj["id"])
        label = escape(str(obj.get("label", "")))
        if kind == "path":
            pts = obj.get("points", [])
            if len(pts) < 2:
                raise ValueError("Path must have two points")
            points = " ".join(f"{_xy(*p)[0]:.1f},{_xy(*p)[1]:.1f}" for p in pts)
            parts.append(f'<polyline data-object-id="{object_id}" points="{points}" fill="none" stroke="#b99862" stroke-width="4" stroke-dasharray="11 6" stroke-linejoin="round"/>')
            parts.append(f'<text x="70" y="{620 - 20 * index}" font-size="11" fill="#d9bd85" font-family="sans-serif">{label}</text>')
        else:
            cx, cy = _xy(obj["x"], obj["y"])
            if kind in {"structure", "room"}:
                w = float(obj.get("w", 14)) * MAP_W / 100
                h = float(obj.get("h", 12)) * MAP_H / 100
                parts.append(f'<rect data-object-id="{object_id}" x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="#38484b" stroke="#b7aa8a" stroke-width="3"/>')
            elif kind in {"cover", "hazard-terrain", "terrain"}:
                color = {"cover": "#80715d", "hazard-terrain": "#956b50", "terrain": "#476057"}[kind]
                parts.append(f'<rect data-object-id="{object_id}" x="{cx-24:.1f}" y="{cy-16:.1f}" width="48" height="32" rx="6" fill="{color}" stroke="#dfcaa3" stroke-width="1.5"/>')
            else:
                color = "#d0b077" if kind == "clue" else "#93b7b8"
                parts.append(f'<circle data-object-id="{object_id}" cx="{cx:.1f}" cy="{cy:.1f}" r="15" fill="#26353b" stroke="{color}" stroke-width="2.5"/>')
            # Numbered map pins and distinct side index avoid occluding close clues.
            parts.append(f'<text x="{cx:.1f}" y="{cy+5:.1f}" text-anchor="middle" fill="#fff5df" font-size="14" font-family="sans-serif" font-weight="bold">{index}</text>')
        legend_rows.append((index, label, kind))

    # Movement layer: pale-blue dashed line, distinct from solid facing arrow.
    if scene:
        current = scene.get("current", {})
        for move in current.get("movement", []):
            x1, y1 = _xy(*move["from"])
            x2, y2 = _xy(*move["to"])
            parts.append(_line(x1, y1, x2, y2, stroke="#77b8d0", stroke_width="3", stroke_dasharray="8 5", marker_end="url(#routeArrow)", **{"data-entity-id": move.get("entity_id", "")}))
        for token in current.get("tokens", []):
            if token.get("status") in {"DEAD", "HIDDEN"}:
                continue
            x, y = _xy(token["x"], token["y"])
            direction = token.get("facing")
            if direction not in FACINGS:
                raise ValueError("Invalid facing for token: " + str(direction))
            radians = math.radians(FACINGS[direction])
            fx = x + math.sin(radians) * 48
            fy = y - math.cos(radians) * 48
            color = "#518fb4" if token.get("category") == "player" else "#b95c52"
            parts.append(_line(x, y, fx, fy, stroke="#c6ebfc", stroke_width="4", marker_end="url(#facingArrow)"))
            parts.append(f'<circle data-token-id="{_attr(token["id"])}" cx="{x:.1f}" cy="{y:.1f}" r="18" fill="{color}" stroke="#d9f0ff" stroke-width="2.5"/>')
            parts.append(f'<text x="{x:.1f}" y="{y+6:.1f}" text-anchor="middle" font-size="18" font-family="sans-serif" fill="white" font-weight="bold">{escape(str(token.get("label", "?")))}</text>')
            parts.append(f'<text x="{x+21:.1f}" y="{y+23:.1f}" font-family="sans-serif" font-size="12" fill="#bde4f7">{escape(str(direction))}</text>')

    parts.append('<text x="824" y="117" font-family="sans-serif" font-weight="bold" font-size="18" fill="#f0e6d4">ĐỊA HÌNH ĐÃ BIẾT</text>')
    for idx, label, kind in legend_rows:
        y = 145 + 29 * (idx - 1)
        parts.append(f'<text x="822" y="{y}" font-family="sans-serif" font-size="14" fill="#f1cf92">{idx:02d}</text>')
        # Keep full text in title; abbreviate visible names before side-panel clipping.
        plain = str(objects[idx-1].get("label", ""))
        short = escape(plain if len(plain) <= 25 else plain[:22] + "…")
        parts.append(f'<text x="858" y="{y}" font-family="sans-serif" font-size="14" fill="#e5e9e8"><title>{label}</title>{short}</text>')
    # Known names with unknown bearings: sidebar text only, never map pins.
    unplaced = area.get("unplaced_known_names", [])
    if unplaced:
        heading_y = 145 + 29 * len(objects) + 15
        if heading_y + 23 * len(unplaced) > 540:
            raise ValueError("Too many unplaced names for sidebar; split into region/area maps")
        parts.append(f'<text x="824" y="{heading_y}" font-family="sans-serif" font-weight="bold" font-size="15" fill="#d6b784">CHƯA ĐỊNH VỊ</text>')
        for i, name in enumerate(unplaced):
            full = escape(str(name))
            short = escape(str(name)[:28] + "…" if len(str(name)) > 29 else str(name))
            parts.append(f'<text data-unplaced-name="{i}" x="824" y="{heading_y + 23 * (i + 1)}" font-family="sans-serif" font-size="13" fill="#b4c4c9"><title>{full}</title>{short}</text>')
    parts.extend([
        '<text x="824" y="566" font-family="sans-serif" font-size="15" fill="#acd5e7">Hướng mặt: đường liền</text>',
        '<text x="824" y="593" font-family="sans-serif" font-size="15" fill="#84b5c9">Di chuyển: nét đứt</text>',
        '<text x="824" y="620" font-family="sans-serif" font-size="13" fill="#bdc9cd">BẮC: phía trên · tọa độ 0–100</text>',
        f'<text x="46" y="658" font-family="sans-serif" font-size="14" fill="#adbac1">Map ID: {escape(map_id)}</text>',
    ])
    if scene:
        parts.append(f'<text x="760" y="658" font-family="sans-serif" font-size="14" fill="#e9c68b">Cuối T{scene["last_completed_turn"]} · T{scene["next_turn"]} chưa diễn ra</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render persistent Hắc Nhật atlas and optional current scene to an editable SVG")
    parser.add_argument("--atlas", type=Path, default=Path(__file__).with_name("atlas-v1.json"))
    parser.add_argument("--scene", type=Path, default=Path(__file__).with_name("active-scene.json"))
    parser.add_argument("--map", dest="map_id", help="Map id; default current scene map")
    parser.add_argument("--base-only", action="store_true", help="Render fixed terrain without live tokens")
    parser.add_argument("--output", type=Path, help="SVG file output; otherwise stdout")
    args = parser.parse_args(argv)
    atlas = json.loads(args.atlas.read_text(encoding="utf-8"))
    scene = None if args.base_only else json.loads(args.scene.read_text(encoding="utf-8"))
    map_id = args.map_id or (scene["map_id"] if scene is not None else None)
    if not map_id:
        parser.error("--map is required with --base-only")
    svg = render_map(atlas, scene, map_id)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")
    else:
        print(svg, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
