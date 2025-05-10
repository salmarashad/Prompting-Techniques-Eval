from vertexai.preview.generative_models import GenerativeModel
from vertexai import init
from config import *
from dotenv import load_dotenv
import csv
import time as process_time
from tqdm import tqdm
from evaluation import *
import os

def make_dir(path):
    os.makedirs(path, exist_ok=True)


def autolabel(ax, rects, fmt='{:.0f}', offset=3):
    for rect in rects:
        h = rect.get_height()
        ax.annotate(fmt.format(h), xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, offset), textcoords="offset points", ha='center', va='bottom')


def init_main():
    load_dotenv()

    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")

    init(project=project_id, location=location)
    model = GenerativeModel("gemini-2.0-flash-001")

    # create base results directory
    results_dir = "prompt_engineering_results"
    os.makedirs(results_dir, exist_ok=True)

# generate requirements with different model configurations
def generate_requirements(prompt_text, config_name="default"):
    try:
        config = model_configs[config_name]
        model = GenerativeModel(config["model_name"])

        generation_config = {
            "temperature": config["temperature"],
            "top_p": config["top_p"],
            "top_k": config["top_k"]
        }

        start_time = process_time.time()
        response = model.generate_content(prompt_text, generation_config=generation_config)
        end_time = process_time.time()
        latency = end_time - start_time

        response_text = response.text

        # default token usage (in case metadata is missing)
        token_usage = {
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None
        }

        if hasattr(response, "usage_metadata"):
            token_usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count
            }
        else:
            print("⚠️ No usage metadata found. Cannot calculate actual token usage.")

        return {
            "text": response_text,
            "latency": latency,
            "config": config_name,
            "config_details": config,
            "token_usage": token_usage
        }

    except Exception as e:
        return {
            "text": f"Error generating requirements: {str(e)}",
            "latency": 0,
            "config": config_name,
            "config_details": config,
            "error": str(e),
            "token_usage": None
        }

# helper function to extract requirements counts using regex
def count_requirements(text):
    # pattern for FR-n: style requirements
    fr_pattern = re.compile(r'FR-\d+:', re.IGNORECASE)
    nfr_pattern = re.compile(r'NFR-\d+:', re.IGNORECASE)

    fr_matches = fr_pattern.findall(text)
    nfr_matches = nfr_pattern.findall(text)

    return len(fr_matches), len(nfr_matches)


def run_evaluation(user_story, row_number):
    results_dir = "prompt_engineering_results"
    run_dir = os.path.join(results_dir, f"row_{row_number}")

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    os.makedirs(run_dir)

    # For storing all results
    all_results = {
        "user_story": user_story,
        "results": {}
    }

    # For storing aggregate metrics
    aggregated_metrics = {
        "by_strategy": {},
        "by_config": {},
        "overall": {
            "fr_count": [],
            "nfr_count": [],
            "specificity_score": [],
            "testability_score": [],
            "measurability_score": [],
            "latency": [],
            "prompt_tokens": [],
            "completion_tokens": [],
            "total_tokens": [],
            "output_length": []
        }
    }

    # CSV for quick comparison
    csv_file = os.path.join(run_dir, "results_summary.csv")
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Strategy", "Config", "Prompt Length", "Response Length",
            "FR Count", "NFR Count", "Specificity Score", "Testability Score",
            "Measurability Score", "Latency (seconds)",
            "Prompt Tokens ", "Completion Tokens ", "Total Tokens "
        ])


    # Loop through all prompt strategies and model configurations
    total_runs = len(prompt_strategies) * len(model_configs)
    progress = tqdm(total=total_runs, desc="Generating requirements")

    # Token tracking summaries
    total_tokens = 0
    token_usage_by_strategy = {}
    token_usage_by_config = {}

    for strategy_name, strategy_func in prompt_strategies.items():
        all_results["results"][strategy_name] = {}
        token_usage_by_strategy[strategy_name] = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }

        # Initialize strategy-level metrics aggregation
        if strategy_name not in aggregated_metrics["by_strategy"]:
            aggregated_metrics["by_strategy"][strategy_name] = {
                "fr_count": [],
                "nfr_count": [],
                "specificity_score": [],
                "testability_score": [],
                "measurability_score": [],
                "latency": [],
                "prompt_tokens": [],
                "completion_tokens": [],
                "total_tokens": [],
                "output_length": []
            }

        # Generate the prompt (same for all configs)
        prompt = strategy_func(user_story)

        for config_name in model_configs:
            if config_name not in token_usage_by_config:
                token_usage_by_config[config_name] = {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }

            # Initialize config-level metrics aggregation
            if config_name not in aggregated_metrics["by_config"]:
                aggregated_metrics["by_config"][config_name] = {
                    "fr_count": [],
                    "nfr_count": [],
                    "specificity_score": [],
                    "testability_score": [],
                    "measurability_score": [],
                    "latency": [],
                    "prompt_tokens": [],
                    "completion_tokens": [],
                    "total_tokens": [],
                    "output_length": []
                }

            # Generate requirements with this config
            result = generate_requirements(prompt, config_name)
            output = result["text"]
            latency = result["latency"]
            token_usage = result.get("token_usage", {})

            # Update token tracking
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_run_tokens = token_usage.get("total_tokens", 0)

            # Update token totals
            total_tokens += total_run_tokens
            token_usage_by_strategy[strategy_name]["prompt_tokens"] += prompt_tokens
            token_usage_by_strategy[strategy_name]["completion_tokens"] += completion_tokens
            token_usage_by_strategy[strategy_name]["total_tokens"] += total_run_tokens

            token_usage_by_config[config_name]["prompt_tokens"] += prompt_tokens
            token_usage_by_config[config_name]["completion_tokens"] += completion_tokens
            token_usage_by_config[config_name]["total_tokens"] += total_run_tokens

            # Extract metrics
            fr_count, nfr_count = count_requirements(output)
            quality_metrics = evaluate_requirements_quality(output)

            # Add metrics to aggregated data
            metrics_to_track = {
                "fr_count": fr_count,
                "nfr_count": nfr_count,
                "specificity_score": quality_metrics["specificity_score"],
                "testability_score": quality_metrics["testability_score"],
                "measurability_score": quality_metrics["measurability_score"],
                "latency": latency,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_run_tokens,
                "output_length": len(output)
            }

            # Update all aggregation levels
            for metric, value in metrics_to_track.items():
                aggregated_metrics["overall"][metric].append(value)
                aggregated_metrics["by_strategy"][strategy_name][metric].append(value)
                aggregated_metrics["by_config"][config_name][metric].append(value)

            # Add to results dictionary
            all_results["results"][strategy_name][config_name] = {
                "prompt": prompt,
                "output": output,
                "prompt_length": len(prompt),
                "output_length": len(output),
                "fr_count": fr_count,
                "nfr_count": nfr_count,
                "latency": latency,
                "quality_metrics": quality_metrics,
                "config_details": model_configs[config_name],
                "token_usage": token_usage
            }

            # Write to CSV
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    strategy_name,
                    config_name,
                    len(prompt),
                    len(output),
                    fr_count,
                    nfr_count,
                    quality_metrics["specificity_score"],
                    quality_metrics["testability_score"],
                    quality_metrics["measurability_score"],
                    f"{latency:.2f}",
                    prompt_tokens,
                    completion_tokens,
                    total_run_tokens
                ])

            progress.update(1)

    progress.close()

    # Save complete results as CSV
    complete_csv_file = os.path.join(run_dir, "complete_results.csv")
    with open(complete_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header row
        writer.writerow([
            "User Story", "Strategy", "Config",
            "Prompt", "Output", "Prompt Length", "Output Length",
            "FR Count", "NFR Count", "Specificity Score", "Testability Score",
            "Measurability Score", "Latency (seconds)", "Prompt Tokens ",
            "Completion Tokens ", "Total Tokens ", "Config Details"
        ])

        # Write data rows
        for strategy_name, strategy_data in all_results["results"].items():
            for config_name, config_data in strategy_data.items():
                writer.writerow([
                    all_results["user_story"],
                    strategy_name,
                    config_name,
                    config_data["prompt"],
                    config_data["output"],
                    config_data["prompt_length"],
                    config_data["output_length"],
                    config_data["fr_count"],
                    config_data["nfr_count"],
                    config_data["quality_metrics"]["specificity_score"],
                    config_data["quality_metrics"]["testability_score"],
                    config_data["quality_metrics"]["measurability_score"],
                    f"{config_data['latency']:.2f}",
                    config_data["token_usage"].get("prompt_tokens", 0),
                    config_data["token_usage"].get("completion_tokens", 0),
                    config_data["token_usage"].get("total_tokens", 0),
                    str(config_data["config_details"])
                ])


    token_summary = {
        "total_tokens": total_tokens,
        "by_strategy": token_usage_by_strategy,
        "by_config": token_usage_by_config
    }

    # # Generate human evaluation template
    # eval_template = os.path.join(run_dir, "human_evaluation_template.csv")
    # with open(eval_template, 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([
    #         "Strategy", "Config", "Completeness (1-5)", "Clarity (1-5)",
    #         "Specificity (1-5)", "Testability (1-5)", "Usefulness (1-5)",
    #         "Overall (1-5)", "Notes"
    #     ])
    #
    #     for strategy_name in all_results["results"]:
    #         for config_name in all_results["results"][strategy_name]:
    #             writer.writerow([
    #                 strategy_name,
    #                 config_name,
    #                 "", "", "", "", "", "", ""
    #             ])


    return all_results, run_dir, token_summary


def load_user_stories_from_csv(filepath):
    stories = {}
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            story_id = f"story_{idx + 1}"
            stories[story_id] = {
                'text': row.get('User Story', ''),
                'context': row.get('Context', '')
            }
    return stories


# main execution function
if __name__ == "__main__":

    print("Starting requirements generation evaluation...")
    init_main()
    stories = load_user_stories_from_csv("user_stories.csv")

    for i, (story_id, story_data) in enumerate(stories.items()):
        # if i != 159:
        #     continue

        print(f"\nProcessing story {story_id}...")
        results, output_dir, token_summary = run_evaluation(story_data, story_id)

        print(f"Evaluation complete for story {story_id}.")
        print(f"- Results saved to {output_dir}")

    print("\nEvaluation complete.")