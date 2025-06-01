import os
import pandas as pd
import numpy as np
from collections import defaultdict

# Define the input directory and create output directory
base_dir = "prompt_engineering_results"


# Define expected strategies and configs for validation
strategies = ["Zero-shot", "Few-shot", "Chain-of-Thought", "Self-Consistency",
              "System Prompt", "Role Prompt", "Contextual", "Tree of Thoughts", "ReAct"]
configs = ["precise", "default", "creative"]

# Use nested defaultdict to make aggregation easier
results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

print(f"Starting to process folders in {base_dir}")

# Track progress
folders_processed = 0
rows_processed = 0

# Loop through all folders
for i in range(1, 258):
    folder_name = f"row_story_{i}"
    folder_path = os.path.join(base_dir, folder_name)

    if not os.path.exists(folder_path):
        print(f"Warning: Folder {folder_path} does not exist")
        continue

    file_path = os.path.join(folder_path, "complete_results.csv")

    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist")
        continue

    try:
        # Read the CSV file - each file might contain multiple rows
        df = pd.read_csv(file_path)

        # Check if file is empty
        if df.empty:
            print(f"Warning: Empty CSV file at {file_path}")
            continue

        # Process each row in the file
        for idx, row in df.iterrows():
            try:
                strategy = row['Strategy']
                config = row['Config']

                # Skip if strategy or config is not valid
                if pd.isna(strategy) or pd.isna(config) or strategy not in strategies or config not in configs:
                    continue

                # Extract metrics
                for metric in ['ai-specificity', 'ai-measurability', 'ai-accuracy', 'ai-completeness']:
                    if metric in row and not pd.isna(row[metric]):
                        try:
                            value = float(row[metric])
                            results[strategy][config][metric].append(value)
                        except (ValueError, TypeError):
                            pass

                rows_processed += 1

            except Exception as e:
                print(f"Error processing row {idx} in {file_path}: {e}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

print(f"\nProcessed {folders_processed} folders with {rows_processed} total rows")

# Calculate averages for each strategy-config combination
avg_results = []

for strategy in strategies:
    for config in configs:
        metrics = results[strategy][config]

        # Only add a row if we have data for this combination
        if any(metrics.values()):
            avg_results.append({
                'Strategy': strategy,
                'Config': config,
                'avg_ai_specificity': round(np.mean(metrics['ai-specificity']), 2) if metrics[
                    'ai-specificity'] else None,
                'avg_ai_measurability': round(np.mean(metrics['ai-measurability']), 2) if metrics[
                    'ai-measurability'] else None,
                'avg_ai_accuracy': round(np.mean(metrics['ai-accuracy']), 2) if metrics['ai-accuracy'] else None,
                'avg_ai_completeness': round(np.mean(metrics['ai-completeness']), 2) if metrics[
                    'ai-completeness'] else None,
            })

# Convert to DataFrame and save to CSV
output_df = pd.DataFrame(avg_results)
output_path = os.path.join("", "strategy_config_averages.csv")
output_df.to_csv(output_path, index=False)

print(f"\nAnalysis complete! Results saved to {output_path}")
print(f"Found {len(avg_results)} strategy-config combinations out of expected 27")