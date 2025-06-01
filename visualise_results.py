import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from process_results import process_results

config_colors = {
    'precise': '#8CB9BD',  # soft teal/aqua
    'default': '#97C1A9',  # sage green
    'creative': '#FCBAD3'  # soft pink
}

def create_visualizations(results_df, output_folder="visualization_results"):
    # create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # set the style for the plots
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (16, 10)
    plt.rcParams['font.size'] = 12

    # get metrics (all columns except Strategy and Config)
    metrics = [col for col in results_df.columns if col not in ['Strategy', 'Config']]

    # process each metric
    for metric in metrics:
        plt.figure(figsize=(16, 10))

        # Create grouped bar chart
        ax = sns.barplot(
            x='Strategy',
            y=metric,
            hue='Config',
            data=results_df,
            palette=config_colors
        )

        # Add values on top of bars
        for i, container in enumerate(ax.containers):
            for j, bar in enumerate(container):
                height = bar.get_height()
                value_format = '{:.2f}' if height < 100 else '{:.1f}' if height < 1000 else '{:.0f}'
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.1,
                    value_format.format(height),
                    ha='center', va='bottom',
                    fontsize=10, rotation=45 if height > 1000 else 0
                )

        # Set title and labels
        plt.title(f'Average {metric} by Strategy and Configuration', fontsize=16)
        plt.xlabel('Strategy', fontsize=14)
        plt.ylabel(metric, fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Configuration', fontsize=12)

        # Adjust layout
        plt.tight_layout()

        # Save figure
        output_file = os.path.join(output_folder, f'{metric.replace(" ", "_")}_comparison.png')
        plt.savefig(output_file, dpi=300)
        print(f"Saved visualization for {metric} to {output_file}")
        plt.close()

    # Create a combined visualization for the most important metrics
    key_metrics = ['FR Count', 'NFR Count', 'Specificity Score', 'Testability Score', 'Measurability Score']
    if all(metric in results_df.columns for metric in key_metrics):
        create_combined_visualization(results_df, key_metrics, output_folder)


def create_combined_visualization(results_df, metrics, output_folder):
    """Create a combined visualization for key metrics"""
    strategies = results_df['Strategy'].unique()
    configs = results_df['Config'].unique()

    # Create subplots
    fig, axes = plt.subplots(len(metrics), 1, figsize=(16, 5 * len(metrics)))

    # Plot each metric
    for i, metric in enumerate(metrics):
        ax = axes[i]
        sns.barplot(
            x='Strategy',
            y=metric,
            hue='Config',
            data=results_df,
            palette=config_colors,
            ax=ax
        )

        # Add values on top of bars
        for container in ax.containers:
            for bar in container:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.05,
                    f'{height:.2f}',
                    ha='center', va='bottom',
                    fontsize=8
                )

        ax.set_title(f'Average {metric}', fontsize=14)
        ax.set_xlabel('') if i < len(metrics) - 1 else ax.set_xlabel('Strategy', fontsize=12)
        ax.set_ylabel(metric, fontsize=12)
        ax.tick_params(axis='x', rotation=45)

        if i == 0:
            ax.legend(title='Configuration', fontsize=10)
        else:
            ax.get_legend().remove()

    plt.tight_layout()
    output_file = os.path.join(output_folder, 'key_metrics_comparison.png')
    plt.savefig(output_file, dpi=300)
    print(f"Saved combined visualization to {output_file}")
    plt.close()


def create_quality_metrics_chart(results_df, output_folder="visualization_results"):
    """
    Create a bar chart showing the average of Measurability, Testability, and Specificity scores
    for each strategy and configuration.

    Args:
        results_df (pandas.DataFrame): DataFrame containing the results
        output_folder (str): Folder to save the visualization
    """
    # Check if all required metrics exist
    required_metrics = ['Measurability Score', 'Testability Score', 'Specificity Score']
    if not all(metric in results_df.columns for metric in required_metrics):
        print("Warning: Not all required metrics found for quality score visualization")
        return

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create a copy of the dataframe
    df = results_df.copy()

    # Calculate the average quality score
    df['Quality Score (Avg)'] = df[required_metrics].mean(axis=1)

    # Set the style for the plot
    sns.set(style="whitegrid")
    plt.figure(figsize=(16, 10))

    # Create bar chart
    ax = sns.barplot(
        x='Strategy',
        y='Quality Score (Avg)',
        hue='Config',
        data=df,
        palette=config_colors
    )

    # Add values on top of bars
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.05,
                f'{height:.2f}',
                ha='center', va='bottom',
                fontsize=10
            )

    # Set title and labels
    plt.title('Average Quality Score (Measurability, Testability, Specificity)', fontsize=16)
    plt.xlabel('Strategy', fontsize=14)
    plt.ylabel('Average Score', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Configuration', fontsize=12)

    # Add horizontal reference lines
    plt.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    plt.axhline(y=2, color='gray', linestyle='--', alpha=0.5)
    plt.axhline(y=3, color='gray', linestyle='--', alpha=0.5)
    plt.axhline(y=4, color='gray', linestyle='--', alpha=0.5)
    plt.axhline(y=5, color='gray', linestyle='--', alpha=0.5)

    # Adjust layout
    plt.tight_layout()

    # Save figure
    output_file = os.path.join(output_folder, 'average_quality_score.png')
    plt.savefig(output_file, dpi=300)
    print(f"Saved average quality score visualization to {output_file}")
    plt.close()

def main():
    # Process results
    print("Processing results...")
    results_df = process_results()

    # Create visualizations
    print("\nCreating visualizations...")
    create_visualizations(results_df)

    # Create quality metrics visualization
    print("\nCreating quality metrics visualization...")
    create_quality_metrics_chart(results_df)

    print("\nVisualization complete!")


if __name__ == "__main__":
    main()