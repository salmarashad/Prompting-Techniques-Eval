import os
import pandas as pd
import time
import json
import ast
import shutil
from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel
from vertexai import init

load_dotenv()
init(project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))
model = GenerativeModel("gemini-2.0-flash-001")

def evaluate_requirements(user_story_data, requirements):
    if isinstance(user_story_data, str):
        try:
            user_story_data = ast.literal_eval(user_story_data)
        except (SyntaxError, ValueError):
            return {k: 3 for k in ["ai-specificity", "ai-measurability", "ai-accuracy", "ai-completeness"]}

    user_story = user_story_data.get('text', '')
    context = user_story_data.get('context', '')

    prompt = f"""
    You are an expert in requirements engineering. You will evaluate a set of requirements based on four criteria.

    USER STORY: {user_story}
    CONTEXT: {context}

    REQUIREMENTS:
    {requirements}

    Please evaluate these requirements on a Likert scale from 1-5 (where 1 is strongly disagree and 5 is strongly agree) for each of the following criteria:

    1. SPECIFICITY: The requirements are specific and unambiguous.
    2. MEASURABILITY: The fulfillment of the requirements can be objectively measured.
    3. ACCURACY: The requirements accurately reflect the information and intent of the source User Story.
    4. COMPLETENESS: The requirements cover all essential functional and non-functional aspects described in the User Story.

    Provide your evaluation as a JSON object with the following format:
    {{
        "specificity": 1-5,
        "measurability": 1-5,
        "accuracy": 1-5,
        "completeness": 1-5
    }}

    Only return the JSON object with no additional text.
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())

        return {
            "ai-specificity": result.get("specificity", 3),
            "ai-measurability": result.get("measurability", 3),
            "ai-accuracy": result.get("accuracy", 3),
            "ai-completeness": result.get("completeness", 3)
        }
    except Exception as e:
        print(f"Error in evaluate_requirements: {e}")
        return {k: 3 for k in ["ai-specificity", "ai-measurability", "ai-accuracy", "ai-completeness"]}


def create_backup(file_path):

    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist, cannot create backup.")
        return

    backup_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    backup_path = os.path.join(backup_dir, f"{os.path.splitext(filename)[0]}_backup.csv")

    try:
        shutil.copy2(file_path, backup_path)
        print(f"Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None


def process_csv(input_file, output_file):
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    columns = ["ai-specificity", "ai-measurability", "ai-accuracy", "ai-completeness"]
    for col in columns:
        if col not in df.columns:
            df[col] = None

    for idx, row in df.iterrows():
        if all(pd.notna(row[col]) for col in columns):
            continue

        try:
            print(f"Processing row {idx + 1}/{len(df)} in {os.path.basename(input_file)}...")
            scores = evaluate_requirements(row["User Story"], row["Output"])
            for col, score in scores.items():
                df.at[idx, col] = score

            if idx % 5 == 0:
                df.to_csv(output_file, index=False)
                print(f"Intermediate save after row {idx + 1}")

            time.sleep(1)
        except Exception as e:
            print(f"Error processing row {idx + 1}: {e}")
            for col in columns:
                df.at[idx, col] = 3

    df.to_csv(output_file, index=False)
    print(f"Completed processing {os.path.basename(input_file)}")


def process_all_rows():
    base_dir = "prompt_engineering_results"

    os.makedirs(base_dir, exist_ok=True)

    for row_num in range(3, 258):
        row_dir = os.path.join(base_dir, f"row_story_{row_num}")
        csv_file = os.path.join(row_dir, "complete_results.csv")

        if not os.path.exists(row_dir):
            print(f"Directory {row_dir} does not exist. Skipping.")
            continue

        if not os.path.exists(csv_file):
            print(f"CSV file {csv_file} does not exist. Skipping.")
            continue

        print(f"\n{'=' * 50}")
        print(f"STARTING PROCESSING: row_story_{row_num}")
        print(f"{'=' * 50}")

        backup = create_backup(csv_file)
        if backup:
            print(f"Created backup before processing row_story_{row_num}")

        process_csv(csv_file, csv_file)

        print(f"{'=' * 50}")
        print(f"COMPLETED: row_story_{row_num}")
        print(f"{'=' * 50}\n")


if __name__ == "__main__":
    process_all_rows()