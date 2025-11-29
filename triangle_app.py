import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ---------------- Available colors ----------------
available_colors = [
    'blue', 'navy', 'red', 'crimson', 'green', 'lime', 'orange',
    'yellow', 'purple', 'pink', 'brown', 'gray', 'black', 'cyan', 'magenta',
    'gold', 'goldenrod', 'lightgoldenrodyellow'
]

# ---------------- Available fonts ----------------
available_fonts = [
    'sans-serif', 'serif', 'cursive', 'fantasy', 'monospace'
]

# ---------------- Fill function ----------------
def fill_half(ax, base_left, base_right, top, pct, color="navy"):
    pct = max(0, min(100, pct)) / 100
    max_height = top[1]
    fill_y = pct * max_height

    if fill_y == 0:
        return

    def interpolate(p1, p2, y):
        (x1, y1), (x2, y2) = p1, p2
        t = (y - y1) / (y2 - y1)
        return (x1 + t * (x2 - x1), y)

    pA = interpolate(base_left, top, fill_y)
    pB = interpolate(base_right, top, fill_y)

    fill_poly = [base_left, base_right, pB, pA]
    patch = Polygon(fill_poly, closed=True, facecolor=color, edgecolor=None, zorder=1)
    ax.add_patch(patch)
    return patch

# ---------------- Streamlit UI ----------------
st.title("Interactive Dual Triangle Generator")

# Centered title input
title_text = st.text_input("Centered Title (optional)", "")
title_font = st.selectbox("Title Font", available_fonts, index=0)
title_size = st.slider("Title Font Size", 10, 40, 16)

# Two columns for left/right settings
col1, col2 = st.columns(2)

with col1:
    label_left = st.text_input("Left Half Label", "Left")
    pct_left   = st.slider(f"Fill % for {label_left}", 0, 100, 50)
    color_left = st.selectbox(f"Color for {label_left}", available_colors, index=available_colors.index("navy"))
    left_font = st.selectbox(f"{label_left} Font", available_fonts, index=0)
    left_size = st.slider(f"{label_left} Font Size", 8, 30, 12)

with col2:
    label_right = st.text_input("Right Half Label", "Right")
    pct_right   = st.slider(f"Fill % for {label_right}", 0, 100, 50)
    color_right = st.selectbox(f"Color for {label_right}", available_colors, index=available_colors.index("crimson"))
    right_font = st.selectbox(f"{label_right} Font", available_fonts, index=0)
    right_size = st.slider(f"{label_right} Font Size", 8, 30, 12)

# ---------------- Triangle coordinates ----------------
base_left  = (0, 0)
base_right = (1, 0)
top        = (0.5, 0.866)
mid        = (0.5, 0)

# ---------------- Create figure ----------------
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect("equal")
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1)
ax.axis("off")

# Draw fills
fill_half(ax, base_left, mid, top, pct_left, color=color_left)
fill_half(ax, mid, base_right, top, pct_right, color=color_right)

# Draw outline and center line
outline = Polygon([base_left, base_right, top], closed=True, fill=False,
                  edgecolor="black", linewidth=2, zorder=10)
ax.add_patch(outline)
ax.plot([0.5, 0.5], [0, 0.866], color="black", linewidth=2, zorder=11)

# Draw left label
x_left_center = (base_left[0] + mid[0]) / 2
ax.text(
    x_left_center, -0.05,
    f"{label_left}: {pct_left:.0f}%",
    ha="center", va="top",
    fontsize=left_size, fontfamily=left_font, fontweight="bold"
)

# Draw right label
x_right_center = (mid[0] + base_right[0]) / 2
ax.text(
    x_right_center, -0.05,
    f"{label_right}: {pct_right:.0f}%",
    ha="center", va="top",
    fontsize=right_size, fontfamily=right_font, fontweight="bold"
)

# Draw centered title if provided
if title_text.strip():
    ax.text(
        0.5, 1.05,
        title_text,
        ha="center", va="bottom",
        fontsize=title_size, fontfamily=title_font, fontweight="bold"
    )

# ---------------- Show figure ----------------
st.pyplot(fig)
