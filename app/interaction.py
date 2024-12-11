import requests
from .data import ModelResponse
import re
from datetime import datetime
from fuzzywuzzy import process
import time

INTENT_ACTION_MAP = {
    "ask_graduation_data": "action_show_graduation_data",
    "ask_research_data": "action_show_research_data",
    "ask_activity_data": "action_show_activity_data",
    "ask_ipk_data": "action_show_ipk_data",
    "ask_lecturer_data": "action_show_lecturer_data",
}

faculty_patterns = [
    "Fakultas Bisnis dan Manajemen",
    "Fakultas Ilmu Pendidikan",
    "Fakultas Ilmu Komputer",
    "Fakultas Teknik Sipil dan Perencanaan",
    "Fakultas Hukum",
]
major_patterns = [
    "Manajemen",
    "Akuntansi",
    "Pariwisata",
    "Pendidikan Bahasa Inggris",
    "Teknik Sipil",
    "Arsitektur",
    "Ilmu Hukum",
    "Sistem Informasi",
    "Teknologi Informasi",
]

publication_type_patterns = ["Nasional non-sinta", "Scopus", "Sinta", "international"]

activity_level_patterns = ["internasional", "lokal", "nasional"]

def convert_range_to_year_range(entities: dict) -> dict:
    if "range" in entities:
        year = entities.get("year")
        
        if year:
            start_year = int(year)  
            end_year = datetime.now().year
            entities["year_range"] = f"{start_year} - {end_year}"
            del entities["year"]
    
    return entities


def calculate_period_range(period: str) -> str:
    current_year = datetime.now().year

    match = re.search(r"(\d+)\s*(tahun terakhir|terakhir)", period)
    if match:
        num_years = int(match.group(1))
        start_year = current_year - num_years
        end_year = current_year
        return f"{start_year} - {end_year}"

    if "tahun terakhir" in period:
        num_years = int(period.split()[0])
        start_year = current_year - num_years
        end_year = current_year
        return f"{start_year} - {end_year}"

    if "dari tahun lalu" in period:
        start_year = current_year - 1
        end_year = current_year
        return f"{start_year} - {end_year}"

    return None


def word_match(input_text: str, patterns: list, threshold: int = 85) -> str:
    result = process.extractOne(input_text, patterns)
    if result and result[1] >= threshold:
        return result[0]
    return input_text


def extract_and_match_entities(entities: dict) -> dict:
    if "faculty" in entities:
        entities["faculty"] = word_match(entities["faculty"], faculty_patterns)

    if "major" in entities:
        entities["major"] = word_match(entities["major"], major_patterns)

    return entities


def extract_number_from_text(text: str) -> int:
    if not text or not isinstance(text, str):
        return None

    match = re.search(r"\d+", text)
    if match:
        return int(match.group(0))
    return None


def execute_action(action_name: str, tracker_data: dict, ttl_hash=None) -> dict:
    action_url = "http://localhost:5055/webhook"
    headers = {"Content-Type": "application/json"}

    payload = {"next_action": action_name, "tracker": tracker_data}
    response = requests.post(action_url, headers=headers, json=payload)
    return response.json()


def request_model(q: str, ttl_hash=None):
    res = requests.post(
        "http://localhost:5005/model/parse",
        headers={"Content-Type": "application/json"},
        json={"text": q},
    )

    return res.json()


def query_model(q: str) -> ModelResponse:
    # cache 5 minutes
    data = request_model(q, ttl_hash=round(time.time() / 300))

    intent = data["intent"]["name"]
    entities = {entity["entity"]: entity["value"] for entity in data["entities"]}
    entities = extract_and_match_entities(entities)

    period = entities.get("period")
    if period:
        year_range = calculate_period_range(period)
        if year_range:
            entities["year_range"] = year_range
            del entities["period"]
    if "range" in entities:
        entities = convert_range_to_year_range(entities)
        del entities["range"]

    for key in ["year","cohort", "start", "end"]:
        if key in entities:
            entities[key] = extract_number_from_text(entities[key])

    if "start" in entities and "end" in entities:
        entities["year_range"] = f"{entities['start']} - {entities['end']}"
    elif "start" in entities:
        entities["year_range"] = f"{entities['start']} - {entities['start']}"
    elif "end" in entities:
        entities["year_range"] = f"{entities['end']} - {entities['end']}"
    if 'cohort' in entities and 'year' in entities:
        entities['cohort'] = entities['year']
        del entities['year']  
    if intent == "ask_activity_data":
        if "activity_level" in entities:
            entities["activity_level"] = word_match(
                entities["activity_level"], activity_level_patterns
            )
        if "publication_type" in entities:
            entities["activity_level"] = entities["publication_type"]
            del entities["publication_type"]

    elif intent == "ask_research_data":
        if "publication_type" in entities:
            entities["publication_type"] = word_match(
                entities["publication_type"], publication_type_patterns
            )
        if "activity_level" in entities:
            entities["publication_type"] = entities["activity_level"]
            del entities["activity_level"]

    tracker_data = {
        "sender_id": "user",
        "slots": entities,
        "latest_message": {"intent": {"name": intent}, "entities": entities, "text": q},
    }

    action_name = INTENT_ACTION_MAP.get(intent)
    # cache for 1 hour
    action_result = execute_action(
        action_name, tracker_data, ttl_hash=round(time.time() / 3600)
    )

    print(f"query_model intent: {intent}")
    print(f"query_model entities: {entities}")

    return ModelResponse(intent=intent, entities=entities, action_result=action_result)
