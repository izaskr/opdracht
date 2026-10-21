from parse_items_responses import read_in_responses
import numpy as np

def stats_responses(file_path):
    responses = read_in_responses(file_path)
    item_response_info = {k: {} for k in responses}
    for k in item_response_info:
        # number of responses and their scores
        count = len(responses[k])
        scores = [answer["score"] for answer in responses[k]]
        mean_score, stdev_score, min_score, max_score = np.mean(scores), np.std(scores), np.min(scores), np.max(scores)
        # length of responses
        answers = [len(answer["antwoord"]) for answer in responses[k]]
        mean_len, stdev_len, min_len, max_len = np.mean(answers), np.std(answers), np.min(answers), np.max(answers)

        info = {"count": count,
                "mean_score": mean_score,
                "stdev_score": stdev_score,
                "min_score": min_score,
                "max_score": max_score,
                "mean_len": mean_len,
                "stdev_len": stdev_len,
                "min_len": min_len,
                "max_len": max_len}
        item_response_info[k] = info

    return item_response_info

#info_responses = stats_responses("/home/skrjanec/cito_opdracht/data/responses.csv")
#for x, v in info_responses.items():
#    print(x, v)

