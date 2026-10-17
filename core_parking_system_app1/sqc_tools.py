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
