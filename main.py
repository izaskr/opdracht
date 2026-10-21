import csv
import pickle
import os
from utils.parse_items_responses import StimuliItems, read_in_responses, read_in_new_responses, read_in_extended_answers
from utils.scoring_items_3_4 import (automatic_scoring_responses_item3, automatic_scoring_new_responses_item3,
                                     automatic_scoring_responses_item4, automatic_scoring_new_responses_item4)
from utils.cluster_responses_1_2_3_4 import clustering_items_1_2_4
from sentence_transformers import SentenceTransformer
from huggingface_hub import login
from sklearn.cluster import KMeans


def score_data(file_path):
    stimuli = StimuliItems("/home/skrjanec/cito_opdracht/data/items.txt")
    item3 = stimuli.item("i03")
    extended_answers = read_in_extended_answers("/home/skrjanec/cito_opdracht/data/extended_answers.json")["i03"]
    responses = read_in_responses("/home/skrjanec/cito_opdracht/data/responses.csv")["i03"]

    matches = automatic_scoring_responses_item3(item3, responses, extended_answers)

    # new data:
    new_responses = read_in_new_responses("/home/skrjanec/cito_opdracht/data/dummy_data_new.csv")["i03"]
    automatic_scoring_new_responses_item3(item3, new_responses, extended_answers)

    item4 = stimuli.item("i04")
    extended_answers = read_in_extended_answers("/home/skrjanec/cito_opdracht/data/extended_answers.json")["i04"]
    responses = read_in_responses("/home/skrjanec/cito_opdracht/data/responses.csv")["i04"]

    matches = automatic_scoring_responses_item4(item4, responses, extended_answers)

    # new data:
    new_responses = read_in_new_responses("/home/skrjanec/cito_opdracht/data/dummy_data_new.csv")["i04"]
    automatic_scoring_new_responses_item4(item4, new_responses, extended_answers)


def run_clustering():
    clustering_items_1_2_4()

def evaluate_item1(new_responses_i01, model):
    """
    Assign new data to clusters
    :param new_responses_i01: New responses
    :param model: sentence embedding model
    :return:
    """
    model_path = "/home/skrjanec/cito_opdracht/models"
    m = "clusters_i01.pkl"
    full_path = os.path.join(model_path, m)
    # step 1: load clusters from pickle file
    with open(full_path, "rb") as f:
        clusters = pickle.load(f)

    # step 2: encode new responses with RobBert
    response_text = []
    for response_row in new_responses_i01:
        response_text.append(response_row["antwoord"].lower())

    new_response_embeddings = model.encode(response_text)  # each has shape: (768,)

    # step 3: assign new responses to existing clusters
    predicted_cluster_labels = clusters.predict(new_response_embeddings)

    # step 4: write into file
    fields = ["predicted_cluster_label", "antwoord"]
    with open("results/item01_assigned_clusters.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(zip(predicted_cluster_labels, [r["antwoord"] for r in new_responses_i01]))

    print("Finished clustering new responses of item 1")


def evaluate_item2(new_responses_i02, model):
    """
    Assign new data to clusters
    :param new_responses_i02: New responses
    :param model: sentence embedding model
    :return:
    """
    model_path = "/home/skrjanec/cito_opdracht/models"
    m = "clusters_i02.pkl"
    full_path = os.path.join(model_path, m)
    # step 1: load clusters from pickle file
    with open(full_path, "rb") as f:
        clusters = pickle.load(f)

    # step 2: encode new responses with RobBert
    response_text = []
    for response_row in new_responses_i02:
        response_text.append(response_row["antwoord"].lower())

    new_response_embeddings = model.encode(response_text)  # each has shape: (768,)

    # step 3: assign new responses to existing clusters
    predicted_cluster_labels = clusters.predict(new_response_embeddings)

    # step 4: write into file
    fields = ["predicted_cluster_label", "antwoord"]
    with open("results/item02_assigned_clusters.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(zip(predicted_cluster_labels, [r["antwoord"] for r in new_responses_i02]))

    print("Finished clustering new responses of item 2")


def evaluate_item3(new_responses_i03, stimuli, extended_answers):
    """
    Evaluate new responses for Item 3 by scoring them using string matching
    :param new_responses_i03: new responses
    :param stimuli: text of stimuli
    :param extended_answers: extended possible answers
    :return:
    """
    automatic_scoring_new_responses_item3(stimuli, new_responses_i03, extended_answers)
    print("Evaluated new responses for item 3")


def evaluate_item4(new_responses_i04, stimuli, extended_answers, model):
    """
    New responses of Item 4 are treated in two ways: scoring (using string matching) and similarity/relatedness
    :param new_csv:
    :param stimuli:
    :param extended_answers:
    :param model:
    :return:
    """
    # string matching: scoring
    automatic_scoring_new_responses_item4(stimuli, new_responses_i04, extended_answers)
    print("Evaluated new responses for item 4")

    # clustering: similarity/relatedness
    model_path = "/home/skrjanec/cito_opdracht/models"
    m = "clusters_i04.pkl"
    full_path = os.path.join(model_path, m)
    # step 1: load clusters from pickle file
    with open(full_path, "rb") as f:
        clusters = pickle.load(f)

    # step 2: encode new responses with RobBert
    response_text = []
    for response_row in new_responses_i04:
        response_text.append(response_row["antwoord"].lower())

    new_response_embeddings = model.encode(response_text)  # each has shape: (768,)

    # step 3: assign new responses to existing clusters
    predicted_cluster_labels = clusters.predict(new_response_embeddings)

    # step 4: write into file
    fields = ["predicted_cluster_label", "antwoord"]
    with open("results/item04_assigned_clusters.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(zip(predicted_cluster_labels, [r["antwoord"] for r in new_responses_i04]))

    print("Finished clustering new responses of item 4")



def evaluate_main():
    new_csv = "/home/skrjanec/cito_opdracht/data/new_data_new.csv"
    new_responses = read_in_new_responses(new_csv)

    stimuli = StimuliItems("/home/skrjanec/cito_opdracht/data/items.txt")
    #import pdb; pdb.set_trace()
    extended_answers = read_in_extended_answers("/home/skrjanec/cito_opdracht/data/extended_answers.json")


    model = SentenceTransformer('NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers')

    evaluate_item1(new_responses_i01=new_responses["i01"], model=model)
    evaluate_item2(new_responses_i02=new_responses["i02"], model=model)

    evaluate_item3(new_responses_i03=new_responses["i03"],
                   extended_answers=extended_answers["i03"],
                   stimuli=stimuli.item("i03"))

    evaluate_item4(new_responses_i04=new_responses["i04"],
                   stimuli=stimuli.item("i04"),
                   extended_answers=extended_answers["i04"],
                   model=model)

evaluate_main()