import os
import pandas as pd
import glob


def process_results(base_folder="prompt_engineering_results"):
    # get all CSV files
    pattern = os.path.join(base_folder, "row_story_*", "results_summary.csv")
    csv_files = glob.glob(pattern)

    print(f"Found {len(csv_files)} CSV files to process")

    # initialize a dictionary to store aggregated data
    aggregated_data = {}

    # initialize counters for each strategy-config combination
    counters = {}

    # process each CSV file
    for file_path in csv_files:
        try:
            # read the CSV file
            df = pd.read_csv(file_path)

            # process each row in the CSV
            for _, row in df.iterrows():
                strategy = row['Strategy']
                config = row['Config']
                key = (strategy, config)

                # skip header rows or rows with missing strategy/config
                if pd.isna(strategy) or pd.isna(config):
                    continue

                # initialize data structure if this is the first time seeing this combination
                if key not in aggregated_data:
                    aggregated_data[key] = {col: 0 for col in df.columns if col not in ['Strategy', 'Config']}
                    counters[key] = 0

                # add the values for this row to the aggregated data
                for col in df.columns:
                    if col not in ['Strategy', 'Config']:
                        aggregated_data[key][col] += row[col]

                # increment the counter for this strategy-config combination
                counters[key] += 1

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # calculate averages
    result_rows = []
    for key, data in aggregated_data.items():
        strategy, config = key
        count = counters[key]

        # skip if no valid data was found
        if count == 0:
            continue

        # calculate averages
        avg_data = {col: value / count for col, value in data.items()}

        # create a row for the results
        result_row = {
            'Strategy': strategy,
            'Config': config,
            **avg_data
        }
        result_rows.append(result_row)

    # create a DataFrame from the results
    results_df = pd.DataFrame(result_rows)

    # sort the DataFrame to match the expected order
    strategy_order = [
        "Zero-shot", "Few-shot", "Chain-of-Thought", "Self-Consistency",
        "System Prompt", "Role Prompt", "Contextual", "Tree of Thoughts", "ReAct"
    ]
    config_order = ["precise", "default", "creative"]

    # create a custom sorting key
    def custom_sort(row):
        strategy_idx = strategy_order.index(row['Strategy']) if row['Strategy'] in strategy_order else len(
            strategy_order)
        config_idx = config_order.index(row['Config']) if row['Config'] in config_order else len(config_order)
        return (strategy_idx, config_idx)

    # sort the results
    results_df['sort_key'] = results_df.apply(custom_sort, axis=1)
    results_df = results_df.sort_values('sort_key').drop('sort_key', axis=1)

    return results_df


def main():
    # process the results
    results = process_results()

    # display the results
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    print(results)

    # save the results to a CSV file
    output_file = "prompt_engineering_averages.csv"
    results.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()