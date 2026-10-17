import io
import base64
import matplotlib
matplotlib.use('Agg')  # Headless backend for web server
import matplotlib.pyplot as plt
from .models import Defect

def get_pareto_chart():
    """Generates an 80/20 Pareto Chart from defect logs encoded as Base64."""
    defects = Defect.objects.all().order_by('-frequency')
    if not defects.exists():
        return None

    categories = [d.defect_type for d in defects]
    frequencies = [d.frequency for d in defects]
    total = sum(frequencies)

    # Compute cumulative percentages
    cumulative = []
    running_sum = 0
    for f in frequencies:
        running_sum += f
        cumulative.append((running_sum / total) * 100)

    fig, ax1 = plt.subplots(figsize=(8, 4.5))

    # Bar chart for defect frequencies
    bars = ax1.bar(categories, frequencies, color='#2b5c8f', width=0.55)
    ax1.set_ylabel('Defect Occurrence Count', color='#2b5c8f', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#2b5c8f')
    ax1.set_xticklabels(categories, rotation=25, ha='right')

    # Line chart for cumulative percentage
    ax2 = ax1.twinx()
    ax2.plot(categories, cumulative, color='#d9534f', marker='o', linewidth=2, markersize=6)
    ax2.set_ylabel('Cumulative Percentage (%)', color='#d9534f', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#d9534f')
    ax2.set_ylim(0, 105)

    # 80% Pareto threshold line
    ax2.axhline(80, color='gray', linestyle='--', linewidth=1, label='80% Cutoff')

    plt.title('Pareto Analysis (80/20 Rule) - Parking Operational Bottlenecks', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=120)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    return f"data:image/png;base64,{image_base64}"

# function to get the ishikawa fishbone diagram :

def get_fishbone_diagram():
    """Generates an Ishikawa (Fishbone) Root-Cause Diagram encoded as Base64."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Central spine
    ax.annotate('', xy=(8.2, 5), xytext=(1, 5),
                arrowprops=dict(arrowstyle="->", lw=3.5, color='#1f2d3d'))

    # Problem statement (Head of the fish)
    ax.text(8.3, 5, "Long Entry\nQueues & Delays", 
            bbox=dict(boxstyle="square,pad=0.5", facecolor="#d9534f", edgecolor="black", alpha=0.9),
            color='white', weight='bold', fontsize=10, va='center')

    # Categories & Causes
    causes = {
        'People': {
            'pos': (2.5, 7.5), 'dir': 1,
            'items': ['Untrained gate staff', 'Slow cash handling']
        },
        'Process': {
            'pos': (5.5, 7.5), 'dir': 1,
            'items': ['Manual receipt checks', 'Lack of lane signage']
        },
        'Software Code': {
            'pos': (2.5, 2.5), 'dir': -1,
            'items': ['Slow checkout queries', 'Unoptimized search']
        },
        'Infrastructure': {
            'pos': (5.5, 2.5), 'dir': -1,
            'items': ['Barrier gate motor jam', 'Inductive loop failure']
        }
    }

    # Draw branch ribs and sub-causes
    for cat, info in causes.items():
        x_base = info['pos'][0] + 1.2
        y_dir = info['dir']
        # Rib line
        ax.plot([x_base, info['pos'][0]], [5, 5 + (2.5 * y_dir)], color='#2b5c8f', lw=2)
        # Category label
        ax.text(info['pos'][0], 5 + (2.8 * y_dir), cat, 
                weight='bold', fontsize=10, color='#2b5c8f',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#e6f2ff", edgecolor="#2b5c8f"))
        # Causes text
        offset = 0.5
        for item in info['items']:
            ax.text(info['pos'][0] + 0.3, 5 + ((1.2 + offset) * y_dir), f"- {item}", 
                    fontsize=8.5, color='#333', va='center')
            offset += 0.8

    plt.title('Ishikawa (Fishbone) Diagram - Root Cause Analysis for TQM', fontsize=12, fontweight='bold', pad=20)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=120)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    return f"data:image/png;base64,{image_base64}"
