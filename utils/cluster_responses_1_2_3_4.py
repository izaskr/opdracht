from .parse_items_responses import StimuliItems, read_in_responses, read_in_new_responses, read_in_extended_answers
from sentence_transformers import SentenceTransformer
from huggingface_hub import login
from sklearn.cluster import KMeans
from sklearn.metrics import homogeneity_score, completeness_score, adjusted_rand_score, v_measure_score
import numpy as np
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt

with open("/home/skrjanec/cito_opdracht/ht.txt", "r") as fh:
    for line in fh:
        hf_token = line.strip()

login(token=hf_token)


def vectorize_answers_or_responses(list_of_strings, model):
    """

    :param list of strings: Students' responses or teachers' responses
    :return: embedding representations of these responses/answers, computed using sentence transformers
    """
    return model.encode(list_of_strings)



def clustering_known_centroids(response_vectors, answer_vectors, response_scores,  n_clusters):
    """
    :param response_vectors: list of lists of embeddings of students' responses
    :param answer_vectors: list of lists of embeddings of teachers' answers
    :param response_scores: scores given by teachers
    :return: clustering object
    """

    #kmeans_clusters  = KMeans(init=answer_vectors, n_clusters=len(answer_vectors)).fit(response_vectors)
    kmeans_clusters = KMeans(n_clusters=n_clusters, random_state=18).fit(response_vectors)
    return kmeans_clusters


def inspect_clusters(cluster_object, response_scores, item_id):
    """
    homogen_score = homogeneity_score(response_scores, cluster_object.labels_)
    complet_score = completeness_score(response_scores, cluster_object.labels_)
    v_m_score = v_measure_score(response_scores, cluster_object.labels_)
    adj_ran = adjusted_rand_score(cluster_object.labels_, response_scores)

    info = {"Homogeneity Score": homogen_score,
            "Completeness Score": complet_score,
            "V measure score": v_m_score,
            "Adjusted Rand Index Score": adj_ran}

    """
    data = {"Cluster_index": cluster_object.labels_,
            "Teacher_score": response_scores,}
    df = pd.DataFrame(data)
    cross_tab = pd.crosstab(df["Cluster_index"], df["Teacher_score"])
    models_path = "/home/skrjanec/cito_opdracht/models"
    fig_path = os.path.join(models_path, item_id + "_clusters.png")
    print(cross_tab)
    cross_tab.plot(kind='bar', rot=0)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150)
    plt.close()


def show_examples(cluster_object, response_scores, response_text):
    cluster_indices = np.unique(cluster_object.labels_)
    examples = {i: {"text": [], "scores": [], "cluster_id": []} for i in cluster_indices}

    max_len = 4

    for j in range(len(response_text)):
        cluster_id = cluster_object.labels_[j]
        if len(examples[cluster_id]["text"]) >= max_len:
            continue
        text = response_text[j]
        score = response_scores[j]
        examples[cluster_id]["text"].append(text)
        examples[cluster_id]["scores"].append(score)
        examples[cluster_id]["cluster_id"].append(cluster_id)
    return examples


def clustering_items_1_2_4():
    """
    Run clustering of sentence embeddings, using kmeans with predetermined number of clusters
    """

    model = SentenceTransformer('NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers')

    stimuli = StimuliItems("/home/skrjanec/cito_opdracht/data/items.txt")

    all_items = ["i01", "i02", "i04"]
    cluster_number = {"i01": 6, "i02": 6, "i04": 6}

    for item_id in all_items:

        responses = read_in_responses("/home/skrjanec/cito_opdracht/data/responses.csv")[item_id] #["i01"]

        response_text, response_scores = [], []
        for response_row in responses:
            response_text.append(response_row["antwoord"].lower())
            response_scores.append(response_row["score"])


        response_embeddings = model.encode(response_text) # each has shape: (768,)

        clusters = clustering_known_centroids(response_vectors=response_embeddings,
                                              n_clusters=cluster_number[item_id],
                                              answer_vectors=None,
                                              response_scores=response_scores)

        print(inspect_clusters(clusters, response_scores, item_id))

        print(show_examples(clusters, response_scores, response_text))

        # save model
        model_path = "/home/skrjanec/cito_opdracht/models"
        name = os.path.join(model_path, "clusters_" + item_id + ".pkl")

        with open(name, "wb") as f:
            pickle.dump(clusters, f)


    print("Finished clustering and saved models")



