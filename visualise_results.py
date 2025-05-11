import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from process_results import process_results

config_colors = {
    'precise': '#8CB9BD',
    'default': '#97C1A9',
    'creative': '#FCBAD3'
}

def add_bar_labels(ax, rotate_threshold=1000):
    for container in ax.containers:
        for bar in container:
            h = bar.get_height()
            fmt = '{:.2f}' if h < 100 else '{:.1f}' if h < 1000 else '{:.0f}'
            ax.text(
                bar.get_x() + bar.get_width() / 2, h + 0.1,
                fmt.format(h),
                ha='center', va='bottom',
                fontsize=10, rotation=45 if h > rotate_threshold else 0
            )

def plot_metric_bar(results_df, metric, output_folder):
    plt.figure(figsize=(16, 10))
    ax = sns.barplot(x='Strategy', y=metric, hue='Config', data=results_df, palette=config_colors)
    add_bar_labels(ax)
    plt.title(f'Average {metric} by Strategy and Configuration', fontsize=16)
    plt.xlabel('Strategy'); plt.ylabel(metric)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Configuration')
    plt.tight_layout()
    path = os.path.join(output_folder, f'{metric.replace(" ", "_")}_comparison.png')
    plt.savefig(path, dpi=300)
    print(f"Saved visualization for {metric} to {path}")
    plt.close()

def create_visualizations(results_df, output_folder="visualization_results"):
    os.makedirs(output_folder, exist_ok=True)
    sns.set(style="whitegrid")
    plt.rcParams.update({'figure.figsize': (16, 10), 'font.size': 12})

    metrics = [col for col in results_df.columns if col not in ['Strategy', 'Config']]
    for metric in metrics:
        plot_metric_bar(results_df, metric, output_folder)

    key = ['FR Count', 'NFR Count', 'Specificity Score', 'Testability Score', 'Measurability Score']
    if all(m in results_df.columns for m in key):
        create_combined_visualization(results_df, key, output_folder)

def create_combined_visualization(results_df, metrics, output_folder):
    fig, axes = plt.subplots(len(metrics), 1, figsize=(16, 5 * len(metrics)))
    axes = axes if isinstance(axes, np.ndarray) else [axes]

    for i, (ax, metric) in enumerate(zip(axes, metrics)):
        sns.barplot(x='Strategy', y=metric, hue='Config', data=results_df, palette=config_colors, ax=ax)
        for container in ax.containers:
            for bar in container:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05, f'{h:.2f}', ha='center', va='bottom', fontsize=8)

        ax.set_title(f'Average {metric}')
        if i < len(metrics) - 1:
            ax.set_xlabel('')
        else:
            ax.set_xlabel('Strategy')
        ax.set_ylabel(metric)
        ax.tick_params(axis='x', rotation=45)
        if i != 0:
            ax.get_legend().remove()
        else:
            ax.legend(title='Configuration')

    plt.tight_layout()
    path = os.path.join(output_folder, 'key_metrics_comparison.png')
    plt.savefig(path, dpi=300)
    print(f"Saved combined visualization to {path}")
    plt.close()

def create_quality_metrics_chart(results_df, output_folder="visualization_results"):
    metrics = ['Measurability Score', 'Testability Score', 'Specificity Score']
    if not all(m in results_df.columns for m in metrics):
        print("Warning: Not all required metrics found for quality score visualization")
        return

    os.makedirs(output_folder, exist_ok=True)
    df = results_df.copy()
    df['Quality Score (Avg)'] = df[metrics].mean(axis=1)

    sns.set(style="whitegrid")
    plt.figure(figsize=(16, 10))
    ax = sns.barplot(x='Strategy', y='Quality Score (Avg)', hue='Config', data=df, palette=config_colors)

    for container in ax.containers:
        for bar in container:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05, f'{h:.2f}', ha='center', va='bottom', fontsize=10)

    plt.title('Average Quality Score (Measurability, Testability, Specificity)', fontsize=16)
    plt.xlabel('Strategy'); plt.ylabel('Average Score')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Configuration')

    for y in range(1, 6):
        plt.axhline(y=y, color='gray', linestyle='--', alpha=0.5)

    plt.tight_layout()
    path = os.path.join(output_folder, 'average_quality_score.png')
    plt.savefig(path, dpi=300)
    print(f"Saved average quality score visualization to {path}")
    plt.close()

def main():
    print("Processing results...")
    df = process_results()

    print("\nCreating visualizations...")
    create_visualizations(df)

    print("\nCreating quality metrics visualization...")
    create_quality_metrics_chart(df)

    print("\nVisualization complete!")

if __name__ == "__main__":
    main()
