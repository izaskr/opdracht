import csv
from .parse_items_responses import StimuliItems, read_in_responses, read_in_new_responses, read_in_extended_answers

def score_question(correct_answers, response):
    """
    :param correct_answers: answer provided by teachers, list
    :param response: responses provided by students, str
    :return: 0 (answer and response do not match) or 1 (they match), int
    """
    score = 0
    correct_answers, response = [c.lower() for c in correct_answers], response.lower()
    for correct_answer in correct_answers:
        if correct_answer in response:
            score = 1
            return score
        # remove all white spaces to catch cases like "wortel haren"
        response = response.replace(" ", "")
        correct_answer = correct_answer.replace(" ", "")
        if correct_answer in response:
            score = 1
            return score
    return score



def automatic_scoring_responses_item3(item_i03, responses_i03, extended_answers_i03):
    teacher_system_match = {"total_responses": 0, "matches": 0}

    mismatches = []

    teacher_answers = item_i03['voorbeelden']
    # [delen van de blad: huidmondjes, delen van de wortel: wortelharen]
    first_answer, second_answer = [teacher_answers[0].split(":")[-1].strip()], [teacher_answers[1].split(":")[-1].strip()]

    #first_answer.append("stoma")

    # extend the list of teachers' answers with lemmas
    print(extended_answers_i03)
    first_answer, second_answer = extended_answers_i03[0], extended_answers_i03[1]

    #print(first_answer, second_answer)

    for response_row in responses_i03:
        response = response_row["antwoord"]
        teacher_score = response_row["score"]
        splt = response.split("][")
        if len(splt) != 2:
            print("Issue with parsing the response. Does not comply with the expected format.")
            continue
        first_response, second_response = splt
        first_response.replace("[", "")
        second_response.replace("]", "")

        first_score = score_question(first_answer, first_response)
        second_score = score_question(second_answer, second_response)
        automatic_total_score = first_score + second_score

        teacher_system_match["total_responses"] += 1

        if automatic_total_score == teacher_score:
            teacher_system_match["matches"] += 1
        else:
            response_row["automatic_score_first"] = first_score
            response_row["automatic_score_second"] = second_score
            mismatches.append(response_row)

    # write mismatches into a csv file
    keys = mismatches[0].keys()
    with open("/home/skrjanec/cito_opdracht/results/mismatches_item_i03.csv", "w") as f_out:
        dict_writer = csv.DictWriter(f_out, keys)
        dict_writer.writeheader()
        dict_writer.writerows(mismatches)

    return teacher_system_match


def automatic_scoring_new_responses_item3(item_i03, responses_i03, extended_answers_i03):
    scored_data = []

    teacher_answers = item_i03['voorbeelden']
    # [delen van de blad: huidmondjes, delen van de wortel: wortelharen]
    first_answer, second_answer = [teacher_answers[0].split(":")[-1].strip()], [teacher_answers[1].split(":")[-1].strip()]

    #first_answer.append("stoma")

    # extend the list of teachers' answers with lemmas
    first_answer, second_answer = extended_answers_i03[0], extended_answers_i03[1]

    for response_row in responses_i03:
        response = response_row["antwoord"]
        splt = response.split("][")
        if len(splt) != 2:
            print("Issue with parsing the response. Does not comply with the expected format.")
            continue
        first_response, second_response = splt
        first_response.replace("[", "")
        second_response.replace("]", "")

        first_score = score_question(first_answer, first_response)
        second_score = score_question(second_answer, second_response)
        automatic_total_score = first_score + second_score

        response_row["automatic_score_first"] = first_score
        response_row["automatic_score_second"] = second_score

        scored_data.append(response_row)

    # write automatic responses into file
    keys = scored_data[0].keys()
    with open("/home/skrjanec/cito_opdracht/results/scored_data_item_i03.csv", "w") as f_out:
        dict_writer = csv.DictWriter(f_out, keys)
        dict_writer.writeheader()
        dict_writer.writerows(scored_data)


def automatic_scoring_responses_item4(item_i04, responses_i04, extended_answers_i04):
    teacher_system_match = {"total_responses": 0, "matches": 0}
    mismatches = []

    teacher_answers = item_i04['voorbeelden']

    for response_row in responses_i04:
        response = response_row["antwoord"].strip().lower()
        teacher_score = response_row["score"]

        automatic_total_score = score_question(extended_answers_i04, response)

        teacher_system_match["total_responses"] += 1

        if automatic_total_score == teacher_score:
            teacher_system_match["matches"] += 1
        else:
            response_row["automatic_score_total"] = automatic_total_score
            mismatches.append(response_row)

    # write mismatches into a csv file
    keys = mismatches[0].keys()
    with open("/home/skrjanec/cito_opdracht/results/mismatches_item_i04.csv", "w") as f_out:
        dict_writer = csv.DictWriter(f_out, keys)
        dict_writer.writeheader()
        dict_writer.writerows(mismatches)

    print(teacher_system_match)

    return teacher_system_match


def automatic_scoring_new_responses_item4(item_i04, responses_i04, extended_answers_i04):
    teacher_answers = item_i04['voorbeelden']
    scored_data = []

    for response_row in responses_i04:
        response = response_row["antwoord"].strip().lower()

        automatic_total_score = score_question(extended_answers_i04, response)
        response_row["automatic_score_total"] = automatic_total_score

        scored_data.append(response_row)

    # write automatically scored data into a csv file
    keys = scored_data[0].keys()
    with open("/home/skrjanec/cito_opdracht/results/scored_data_item_i04.csv", "w") as f_out:
        dict_writer = csv.DictWriter(f_out, keys)
        dict_writer.writeheader()
        dict_writer.writerows(scored_data)

"""

stimuli = StimuliItems("/home/skrjanec/cito_opdracht/data/items.txt")
item4 = stimuli.item("i04")
extended_answers = read_in_extended_answers("/home/skrjanec/cito_opdracht/data/extended_answers.json")["i04"]
responses = read_in_responses("/home/skrjanec/cito_opdracht/data/responses.csv")["i04"]

matches = automatic_scoring_responses_item4(item4, responses, extended_answers)

# new data:
new_responses = read_in_new_responses("/home/skrjanec/cito_opdracht/data/dummy_data_new.csv")["i04"]
automatic_scoring_new_responses_item4(item4, new_responses, extended_answers)
"""