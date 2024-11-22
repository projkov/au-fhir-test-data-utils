from .constants import (
    ALLERGY_INTOLERANCE_REPLACE,
    HEALTHCARE_SERVICE_REPLACE,
    ORGANIZATION_REPLACE,
    PRACTITIONER_ROLE_REPLACE,
)

def remove_time(data):
    if not isinstance(data, str):
        return data
    parts = data.split(" ")
    return parts[0]


def replace_substring_in_file(file_path, target_substring, replacement_substring):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    modified_lines = []

    for line in lines:
        if target_substring in line:
            modified_lines.append(line.replace(target_substring, replacement_substring))
        else:
            modified_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(modified_lines)


def replace_substrings_in_file(file_path, substring_pairs):
    for substring_pair in substring_pairs:
        replace_substring_in_file(file_path, substring_pair[0], substring_pair[1])


def add_empty_columns(file_path, number_of_columns):
    for _i in range(number_of_columns):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        modified_lines = [line.rstrip("\n") + "," + "\n" for line in lines]

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(modified_lines)


def post_process_sheet(sheet, file_path):
    post_process_actions = {
        "AllergyIntolerance": lambda file_path: replace_substrings_in_file(file_path, ALLERGY_INTOLERANCE_REPLACE),
        "Encounter": lambda file_path: replace_substring_in_file(file_path, "inpatient encounter	", '"inpatient encounter	"'),
        "Immunization": lambda file_path: replace_substring_in_file(file_path, "Unnamed: 45", ""),
        "HealthcareService": lambda file_path: (
            replace_substrings_in_file(file_path, HEALTHCARE_SERVICE_REPLACE),
            add_empty_columns(file_path, 2),
        ),
        "Organization": lambda file_path: (
            replace_substrings_in_file(file_path, ORGANIZATION_REPLACE),
            add_empty_columns(file_path, 2),
        ),
        "PractitionerRole": lambda file_path: replace_substrings_in_file(file_path, PRACTITIONER_ROLE_REPLACE),
        "RelatedPerson": lambda file_path: add_empty_columns(file_path, 1),
        "Practitioner": lambda file_path: add_empty_columns(file_path, 1),
    }

    if sheet in post_process_actions:
        post_process_actions[sheet](file_path)


def process_sheet(sheet, df):
    process_actions = {
        "Patient": lambda df: df.assign(birthDate=df["birthDate"].apply(remove_time)),
        "RelatedPerson": lambda df: df.assign(
            birthDate=df["birthDate"].apply(remove_time),
            patient_dob=df["patient_dob"].apply(remove_time)
        )
    }

    if sheet in process_actions:
        df[:] = process_actions[sheet](df)
