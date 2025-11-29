import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ---------------- Set page layout ----------------
st.set_page_config(
    page_title="Interactive Triangle Fill with Cross",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Available colors and fonts ----------------
available_colors = [
    'blue', 'navy', 'red', 'crimson', 'green', 'lime', 'orange',
    'yellow', 'purple', 'pink', 'brown', 'gray', 'black', 'cyan', 'magenta',
    'gold', 'goldenrod', 'lightgoldenrodyellow'
]

available_fonts = [
    'sans-serif', 'serif', 'cursive', 'fantasy', 'monospace'
]

# ---------------- Function to fill half triangle ----------------
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

# ---------------- Streamlit GUI ----------------
st.title("Interactive Dual Campaign Tracker")

# Centered title
title_text = st.text_input("Centered Title (optional)", "")
title_font = st.selectbox("Title Font", available_fonts, index=0)
title_size = st.slider("Title Font Size", 10, 40, 16)
title_color = st.color_picker("Title Color", "#000000")

# Left/Right configuration in wide columns
col1, col2 = st.columns(2)

with col1:
    label_left = st.text_input("Left Half Label", "Left")
    pct_left = st.slider(f"{label_left} Fill %", 0, 100, 50)
    color_left = st.selectbox(f"{label_left} Color", available_colors, index=available_colors.index("navy"))
    left_font = st.selectbox(f"{label_left} Font", available_fonts, index=0)
    left_size = st.slider(f"{label_left} Font Size", 8, 30, 12)

with col2:
    label_right = st.text_input("Right Half Label", "Right")
    pct_right = st.slider(f"{label_right} Fill %", 0, 100, 50)
    color_right = st.selectbox(f"{label_right} Color", available_colors, index=available_colors.index("crimson"))
    right_font = st.selectbox(f"{label_right} Font", available_fonts, index=0)
    right_size = st.slider(f"{label_right} Font Size", 8, 30, 12)

# ---------------- Optional custom horizontal grid lines ----------------
show_grid = st.checkbox("Show custom horizontal grid lines", value=False)
grid_percentages = []

if show_grid:
    st.markdown("### Set up to 10 horizontal grid lines (0–100%)")
    previous_filled = True
    for i in range(10):
        if previous_filled:
            pct = st.number_input(
                f"Grid line {i+1} (%)",
                min_value=0.0, max_value=100.0, value=0.0, step=1.0, key=f"grid{i}"
            )
            if pct > 0:
                grid_percentages.append(pct)
                previous_filled = True
            else:
                previous_filled = False
        else:
            break

# ---------------- Triangle coordinates ----------------
base_left = (0, 0)
base_right = (1, 0)
top = (0.5, 2)  # 2:1 height-to-base ratio
mid = (0.5, 0)

# ---------------- Create figure ----------------
fig, ax = plt.subplots(figsize=(6, 12), dpi=100)
ax.set_aspect("equal")
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, top[1] + 0.5)  # extra space for cross and title
ax.axis("off")

# Draw left and right fills
fill_half(ax, base_left, mid, top, pct_left, color=color_left)
fill_half(ax, mid, base_right, top, pct_right, color=color_right)

# Draw triangle outline and center line
outline = Polygon([base_left, base_right, top], closed=True, fill=False,
                  edgecolor="black", linewidth=2, zorder=2)
ax.add_patch(outline)
ax.plot([0.5, 0.5], [0, top[1]], color="black", linewidth=2, zorder=2)

# Draw custom horizontal grid lines on top (subtle)
grid_line_width = 2 * 0.75  # 75% of outline thickness
for pct in grid_percentages:
    y = pct / 100 * top[1]
    ax.hlines(
        y, xmin=0, xmax=1,
        colors='gray', linestyles='dashed',
        linewidth=grid_line_width, zorder=5
    )
    ax.text(
        -0.05, y, f"{pct:.0f}%",
        ha="right", va="center",
        fontsize=10, fontweight="bold",
        color="gray", zorder=6
    )

# Draw left/right labels
x_left_center = (base_left[0] + mid[0]) / 2
ax.text(
    x_left_center, -0.05,
    f"{label_left}: {pct_left:.0f}%",
    ha="center", va="top",
    fontsize=left_size, fontfamily=left_font, fontweight="bold", zorder=7
)

x_right_center = (mid[0] + base_right[0]) / 2
ax.text(
    x_right_center, -0.05,
    f"{label_right}: {pct_right:.0f}%",
    ha="center", va="top",
    fontsize=right_size, fontfamily=right_font, fontweight="bold", zorder=7
)

# ---------------- Draw fixed cross ----------------
cross_height = 0.2
cross_width = 0.1
cross_intersection = 0.7
cross_linewidth = 3
cross_color = 'black'
cross_offset = -0.02 # slightly downward from apex

apex_x, apex_y = top

# Vertical line (bottom slightly below apex)
vertical_bottom = apex_y + cross_offset
vertical_top = vertical_bottom + cross_height

ax.plot(
    [apex_x, apex_x],
    [vertical_bottom, vertical_top],
    color=cross_color, linewidth=cross_linewidth, zorder=10
)

# Horizontal line at intersection
horizontal_y = vertical_bottom + cross_height * cross_intersection
ax.plot(
    [apex_x - cross_width / 2, apex_x + cross_width / 2],
    [horizontal_y, horizontal_y],
    color=cross_color, linewidth=cross_linewidth, zorder=10
)

# ---------------- Draw centered title ----------------
title_padding = 0.05
if title_text.strip():
    ax.text(
        0.5, vertical_top + title_padding,
        title_text,
        ha="center", va="bottom",
        fontsize=title_size, fontfamily=title_font, fontweight="bold",
        color=title_color, zorder=8
    )

# ---------------- Centered display of figure ----------------
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.pyplot(fig, use_container_width=False)
