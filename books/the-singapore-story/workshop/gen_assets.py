#!/usr/bin/env python3
"""Generate flag images and 1940s maps for workshop PDF using cartopy."""

import os, sys, math
sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

OUT = os.path.join(os.path.dirname(__file__), "images")
DPI = 250


# ============================================================
# FLAGS
# ============================================================

def draw_flag_japan():
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.set_xlim(0, 3); ax.set_ylim(0, 2)
    ax.set_aspect("equal")
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 2, fc="white", ec="#999", lw=1))
    ax.add_patch(mpatches.Circle((1.5, 1), 0.6, fc="#BC002D", ec="none"))
    ax.axis("off")
    fig.savefig(f"{OUT}/flag_japan.png", dpi=DPI, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def draw_flag_britain():
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.set_xlim(0, 3); ax.set_ylim(0, 2)
    ax.set_aspect("equal")
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 2, fc="#012169", ec="#999", lw=1))
    for x1, y1, x2, y2 in [(0, 0, 3, 2), (0, 2, 3, 0)]:
        ax.plot([x1, x2], [y1, y2], color="white", lw=8, solid_capstyle="butt")
    for x1, y1, x2, y2 in [(0, 0, 3, 2), (0, 2, 3, 0)]:
        ax.plot([x1, x2], [y1, y2], color="#C8102E", lw=4, solid_capstyle="butt")
    ax.plot([1.5, 1.5], [0, 2], color="white", lw=12, solid_capstyle="butt")
    ax.plot([0, 3], [1, 1], color="white", lw=12, solid_capstyle="butt")
    ax.plot([1.5, 1.5], [0, 2], color="#C8102E", lw=7, solid_capstyle="butt")
    ax.plot([0, 3], [1, 1], color="#C8102E", lw=7, solid_capstyle="butt")
    ax.axis("off")
    fig.savefig(f"{OUT}/flag_britain.png", dpi=DPI, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def draw_flag_singapore():
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.set_xlim(0, 3); ax.set_ylim(0, 2)
    ax.set_aspect("equal")
    ax.add_patch(mpatches.Rectangle((0, 1), 3, 1, fc="#EF3340", ec="none"))
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 1, fc="white", ec="none"))
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 2, fc="none", ec="#999", lw=1))
    ax.add_patch(mpatches.Circle((0.65, 1.5), 0.32, fc="white", ec="none"))
    ax.add_patch(mpatches.Circle((0.75, 1.5), 0.28, fc="#EF3340", ec="none"))
    cx, cy, r = 1.05, 1.5, 0.2
    for i in range(5):
        angle = math.pi / 2 + 2 * math.pi * i / 5
        sx = cx + r * math.cos(angle)
        sy = cy + r * math.sin(angle)
        ax.plot(sx, sy, marker="*", markersize=6, color="white", markeredgewidth=0)
    ax.axis("off")
    fig.savefig(f"{OUT}/flag_singapore.png", dpi=DPI, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def draw_flag_malaysia():
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.set_xlim(0, 3); ax.set_ylim(0, 2)
    ax.set_aspect("equal")
    stripe_h = 2 / 14
    for i in range(14):
        color = "#CC0001" if i % 2 == 0 else "white"
        ax.add_patch(mpatches.Rectangle((0, 2 - (i + 1) * stripe_h), 3, stripe_h, fc=color, ec="none"))
    ax.add_patch(mpatches.Rectangle((0, 1), 1.5, 1, fc="#010066", ec="none"))
    ax.add_patch(mpatches.Circle((0.55, 1.5), 0.3, fc="#FCC200", ec="none"))
    ax.add_patch(mpatches.Circle((0.65, 1.5), 0.25, fc="#010066", ec="none"))
    cx_s, cy_s, r_s = 0.95, 1.5, 0.22
    star_pts = []
    for i in range(28):
        angle = math.pi / 2 + 2 * math.pi * i / 28
        rad = r_s if i % 2 == 0 else r_s * 0.55
        star_pts.append((cx_s + rad * math.cos(angle), cy_s + rad * math.sin(angle)))
    ax.add_patch(mpatches.Polygon(star_pts, closed=True, fc="#FCC200", ec="none"))
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 2, fc="none", ec="#999", lw=1))
    ax.axis("off")
    fig.savefig(f"{OUT}/flag_malaysia.png", dpi=DPI, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# ============================================================
# Shared map helpers
# ============================================================

def _label(ax, lon, lat, text, fontsize=8, color="#2c3e50", bold=False, **kw):
    """Place a text label with white outline for readability."""
    fw = "bold" if bold else "normal"
    txt = ax.text(lon, lat, text, transform=ccrs.PlateCarree(),
                  fontsize=fontsize, color=color, fontweight=fw,
                  fontfamily="Hiragino Sans", ha=kw.get("ha", "center"),
                  va=kw.get("va", "center"), zorder=10)
    txt.set_path_effects([pe.withStroke(linewidth=2.5, foreground="white")])
    return txt


def _base_map(ax):
    """Common styling for all maps."""
    ax.add_feature(cfeature.OCEAN, facecolor="#dae8f5", zorder=0)
    ax.add_feature(cfeature.LAND, facecolor="#f5f0e8", edgecolor="#999", linewidth=0.5, zorder=1)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.4, color="#888", zorder=2)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3, linestyle=":", color="#aaa", zorder=2)
    ax.add_feature(cfeature.LAKES, facecolor="#dae8f5", edgecolor="#999", linewidth=0.3, zorder=2)


def _dot(ax, lon, lat, color="#c0392b", size=5):
    ax.plot(lon, lat, "o", color=color, markersize=size, transform=ccrs.PlateCarree(), zorder=8)


# ============================================================
# MAPS
# ============================================================

def draw_map_japan():
    """Japan's empire and southern advance route."""
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([92, 148, -10, 45], crs=ccrs.PlateCarree())
    _base_map(ax)

    # Highlight Japanese territories (approximate shading)
    # Japan home islands emphasis
    from matplotlib.patches import FancyArrowPatch
    import matplotlib.patches as mp

    # Empire overlay — rough polygons for visual effect
    # Japan
    _label(ax, 137, 37, "日本", fontsize=11, color="#b71c1c", bold=True)
    # Korea
    _label(ax, 127.5, 37, "朝鮮", fontsize=7, color="#c62828")
    # Taiwan
    _label(ax, 121, 23.5, "台湾", fontsize=7, color="#c62828")
    # Manchuria
    _label(ax, 125, 44, "満州国", fontsize=7, color="#c62828")

    # Targets
    _label(ax, 101, 4, "マラヤ", fontsize=7.5, color="#1565c0")
    _dot(ax, 103.85, 1.35, "#e65100", 6)
    _label(ax, 103.85, -0.5, "シンガポール", fontsize=7, color="#e65100", bold=True)
    _label(ax, 112, 2, "ボルネオ", fontsize=7, color="#1565c0")
    _label(ax, 121, 12, "フィリピン", fontsize=7, color="#1565c0")
    _label(ax, 107, -5, "蘭領東インド\n（石油）", fontsize=7.5, color="#0d47a1", bold=True)

    _label(ax, 110, 30, "中国", fontsize=9, color="#7d6608")

    # Southern advance arrows
    trans = ccrs.PlateCarree()._as_mpl_transform(ax)
    arrow_base = dict(arrowstyle="->,head_width=5,head_length=4", color="#c62828", lw=2.5)
    ax.annotate("", xy=(103.5, 2), xytext=(132, 32),
                arrowprops=dict(**arrow_base, connectionstyle="arc3,rad=0.2"),
                xycoords=trans, textcoords=trans)
    ax.annotate("", xy=(121, 8), xytext=(130, 28),
                arrowprops=dict(**arrow_base, connectionstyle="arc3,rad=-0.15"),
                xycoords=trans, textcoords=trans)
    ax.annotate("", xy=(108, -3), xytext=(128, 25),
                arrowprops=dict(**arrow_base, connectionstyle="arc3,rad=0.3"),
                xycoords=trans, textcoords=trans)

    # Oil box
    _label(ax, 108, -8, "石油", fontsize=10, color="#c62828", bold=True)
    ax.add_patch(mpatches.FancyBboxPatch(
        (103, -9.5), 10, 3, boxstyle="round,pad=0.5",
        facecolor="#fadbd8", edgecolor="#c62828", linewidth=1.5, alpha=0.7,
        transform=ccrs.PlateCarree(), zorder=5))

    # Title
    ax.set_title("1940年  大日本帝国と南進ルート", fontsize=12,
                 fontweight="bold", fontfamily="Hiragino Sans", color="#2c3e50", pad=10)

    fig.savefig(f"{OUT}/map_japan.png", dpi=DPI, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


def draw_map_singapore():
    """Singapore — tiny island at the tip of Malaya."""
    fig = plt.figure(figsize=(5.5, 4))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([99, 106, -1.5, 7.5], crs=ccrs.PlateCarree())
    _base_map(ax)

    # Labels
    _label(ax, 101.5, 4.5, "マラヤ\n（イギリス植民地）", fontsize=10, color="#1565c0", bold=True)
    _label(ax, 97, 2.5, "スマトラ\n（オランダ領）", fontsize=7.5, color="#7f8c8d")

    # Cities
    for lon, lat, name in [(101.7, 3.15, "クアラルンプール"), (100.35, 5.4, "ペナン"), (100.5, 6.6, "コタバル")]:
        _dot(ax, lon, lat, "#1565c0", 4)
        _label(ax, lon + 0.4, lat, name, fontsize=6.5, color="#1565c0", ha="left")

    # Singapore
    _dot(ax, 103.85, 1.35, "#e65100", 8)

    # SG callout
    ax.annotate("シンガポール\n（イギリス直轄植民地）\n人口約80万人",
                xy=(103.85, 1.35), xytext=(105, -0.3),
                xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                textcoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                fontsize=8, fontfamily="Hiragino Sans", color="#bf360c",
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#bf360c", lw=1.5),
                bbox=dict(boxstyle="round,pad=0.4", fc="#fbe9e7", ec="#bf360c"),
                zorder=10)

    # Causeway
    ax.plot([103.76, 103.76], [1.38, 1.48], color="#2c3e50", lw=2, ls="--",
            transform=ccrs.PlateCarree(), zorder=5)
    _label(ax, 104.2, 1.55, "コーズウェイ", fontsize=6, color="#2c3e50")

    # Malacca Strait
    _label(ax, 100.5, 0.5, "マラッカ海峡", fontsize=7, color="#5d6d7e")

    ax.set_title("1940年  シンガポールの位置", fontsize=12,
                 fontweight="bold", fontfamily="Hiragino Sans", color="#2c3e50", pad=10)

    fig.savefig(f"{OUT}/map_singapore.png", dpi=DPI, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


def draw_map_malaysia():
    """Malaya's resources and ethnic division."""
    fig = plt.figure(figsize=(5.5, 4))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([99, 106, -1.5, 8], crs=ccrs.PlateCarree())
    _base_map(ax)

    _label(ax, 101.5, 7, "マラヤ（9州 + 海峡植民地）", fontsize=9, color="#2e7d32", bold=True)

    # Resource labels with boxes
    ax.text(100.5, 5.5, "錫 (Tin)\n世界最大", transform=ccrs.PlateCarree(),
            fontsize=8, ha="center", color="#4a148c", fontweight="bold",
            fontfamily="Hiragino Sans", zorder=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="#e1bee7", ec="#4a148c", alpha=0.85))

    ax.text(102.5, 3, "ゴム (Rubber)\n世界の40%", transform=ccrs.PlateCarree(),
            fontsize=8, ha="center", color="#1b5e20", fontweight="bold",
            fontfamily="Hiragino Sans", zorder=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="#c8e6c9", ec="#1b5e20", alpha=0.85))

    # Ethnic groups
    _label(ax, 100.2, 4, "マレー人\n（農業・漁業）", fontsize=6.5, color="#2e7d32")
    _label(ax, 102, 2, "中華系\n（鉱山・商業）", fontsize=6.5, color="#c62828")
    _label(ax, 103.5, 5.5, "インド系\n（ゴム農園）", fontsize=6.5, color="#0d47a1")

    # Singapore
    _dot(ax, 103.85, 1.35, "#e65100", 6)
    _label(ax, 104.5, 1.1, "SG", fontsize=7, color="#e65100", bold=True)

    # Sumatra
    _label(ax, 97, 2.5, "スマトラ\n（オランダ領）", fontsize=7, color="#7f8c8d")

    # Divide and Rule box
    ax.text(99.5, -0.8, "Divide and Rule（分割統治）\n3民族を分断して支配", transform=ccrs.PlateCarree(),
            fontsize=7.5, ha="left", color="#5d4037", fontfamily="Hiragino Sans",
            bbox=dict(boxstyle="round,pad=0.3", fc="#efebe9", ec="#5d4037", alpha=0.9), zorder=10)

    ax.set_title("1940年  マラヤの資源と民族構成", fontsize=12,
                 fontweight="bold", fontfamily="Hiragino Sans", color="#2c3e50", pad=10)

    fig.savefig(f"{OUT}/map_malaysia.png", dpi=DPI, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


def draw_map_britain():
    """British Empire's Southeast Asian territories."""
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([92, 120, -10, 12], crs=ccrs.PlateCarree())
    _base_map(ax)

    # British territories
    _label(ax, 101, 4.5, "マラヤ", fontsize=9, color="#0d47a1", bold=True)
    _label(ax, 96.5, 7, "ビルマ", fontsize=8, color="#0d47a1")
    _label(ax, 113, 4, "北ボルネオ\n（英領）", fontsize=7, color="#0d47a1")

    # Dutch territories
    _label(ax, 97, 1, "スマトラ\n（蘭領）", fontsize=7, color="#7f8c8d")
    _label(ax, 110, -6.5, "ジャワ（蘭領）", fontsize=7, color="#7f8c8d")
    _label(ax, 113, -1, "ボルネオ南部\n（蘭領）", fontsize=6.5, color="#7f8c8d")

    # French
    _label(ax, 106, 8, "仏領\nインドシナ", fontsize=7, color="#7f8c8d")

    # Singapore naval base callout
    _dot(ax, 103.85, 1.35, "#c62828", 8)
    ax.annotate("シンガポール海軍基地\n「東洋のジブラルタル」\n建設費5億ポンド以上",
                xy=(103.85, 1.35), xytext=(109, 0.5),
                xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                textcoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                fontsize=7.5, fontfamily="Hiragino Sans", color="#c62828",
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#c62828", lw=1.5),
                bbox=dict(boxstyle="round,pad=0.4", fc="#ffebee", ec="#c62828", alpha=0.9),
                zorder=10)

    # Trade route
    ax.plot([93, 103.5], [5, 1.5], color="#1565c0", lw=1.5, ls="--",
            transform=ccrs.PlateCarree(), zorder=5, alpha=0.7)
    ax.plot([104, 118], [1.5, -5], color="#1565c0", lw=1.5, ls="--",
            transform=ccrs.PlateCarree(), zorder=5, alpha=0.7)
    _label(ax, 98, 3, "貿易路", fontsize=6.5, color="#1565c0")

    # Legend
    legend_y = -8.5
    ax.add_patch(mpatches.Rectangle((93, legend_y), 1.5, 1,
                 facecolor="#bbdefb", edgecolor="#0d47a1", lw=1,
                 transform=ccrs.PlateCarree(), zorder=10))
    ax.text(95, legend_y + 0.5, "イギリス領", transform=ccrs.PlateCarree(),
            fontsize=7, color="#0d47a1", fontfamily="Hiragino Sans",
            va="center", zorder=10)
    ax.add_patch(mpatches.Rectangle((100, legend_y), 1.5, 1,
                 facecolor="#e0e0e0", edgecolor="#7f8c8d", lw=1,
                 transform=ccrs.PlateCarree(), zorder=10))
    ax.text(102, legend_y + 0.5, "オランダ/フランス領", transform=ccrs.PlateCarree(),
            fontsize=7, color="#7f8c8d", fontfamily="Hiragino Sans",
            va="center", zorder=10)

    ax.set_title("1940年  東南アジアにおけるイギリスの勢力圏", fontsize=12,
                 fontweight="bold", fontfamily="Hiragino Sans", color="#2c3e50", pad=10)

    fig.savefig(f"{OUT}/map_britain.png", dpi=DPI, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


if __name__ == "__main__":
    draw_flag_japan()
    draw_flag_britain()
    draw_flag_singapore()
    draw_flag_malaysia()
    print("Flags generated.")

    draw_map_japan()
    print("  map_japan OK")
    draw_map_singapore()
    print("  map_singapore OK")
    draw_map_malaysia()
    print("  map_malaysia OK")
    draw_map_britain()
    print("  map_britain OK")
    print(f"All assets saved to: {OUT}/")
