import csv
import json

class StimuliItems:
    def __init__(self, path_to_file):
        self.data = self.parse(path_to_file)


    def item(self, item_id):
        return self.data[item_id]

    def parse(self, path_to_file):
        items = {}
        current_item_id = -99
        detail_item_id, vak, max_score, stimulus, vraag, scoring = None, None, None, None, None, None
        voorbeelden = []
        with open(path_to_file) as f_input:
            for line in f_input:
                line = line.strip()
                if not line: # if an empty string
                    continue
                if line.startswith("## Item"):

                    if current_item_id != -99:
                        items[current_item_id] = {"detail_item_id": detail_item_id,
                                                  "vak": vak,
                                                  "max_score": max_score,
                                                  "stimulus": stimulus,
                                                  "vraag": vraag,
                                                  "voorbeelden": voorbeelden,
                                                  "scoring": scoring}
                        detail_item_id, vak, max_score, stimulus, vraag, scoring = None, None, None, None, None, None
                        voorbeelden = []
                elif line.startswith("vak ="):
                    vak = line.split()[-1]
                elif line.startswith("item_id ="):
                    current_item_id = line.split()[-2]
                    detail_item_id = line.split()[-1].replace("(", "").replace(")", "")
                elif line.startswith("max_score ="):
                    max_score = int(line.split()[-1])
                elif line.startswith("stimulus:"):
                    stimulus = line.replace("stimulus:", "").strip()
                elif line.startswith("vraag:"):
                    vraag = line.replace("vraag:", "").strip()
                elif line.startswith("- "):
                    voorbeelden.append(line.replace("- ", "").strip())
                elif line.startswith("scoring:"):
                    scoring = line.replace("scoring:", "").strip()
        # add the last item
        items[current_item_id] = {"detail_item_id": detail_item_id,
                                  "vak": vak,
                                  "max_score": max_score,
                                  "stimulus": stimulus,
                                  "vraag": vraag,
                                  "voorbeelden": voorbeelden,
                                  "scoring": scoring}
        return items


#stimuli = StimuliItems("/home/skrjanec/cito_opdracht/data/items.txt")
#stimuli.item("i01")
# {'detail_item_id': '32jt68',
# 'vak': 'aardrijkskunde',
# 'max_score': 1,
# 'stimulus': 'In 2017 en 2018 kwamen de meeste immigranten in Nederland uit Europa. Uit de andere werelddelen kwamen veel minder migranten naar Nederland. Een van de redenen hiervan is dat Nederland voor Europese migranten dichtbij ligt.',
# 'vraag': 'Noem nog een reden waarom de meeste immigranten in Nederland uit Europa komen.',
# 'voorbeelden': ['Inwoners uit de lidstaten van de Europese Unie kunnen zich vrij vestigen (wonen/werken/studeren) in andere lidstaten.', 'Veel bedrijven hebben vestigingen in meerdere landen in de Europese Unie.', 'Binnen Europa zijn veel overeenkomsten in cultuur.'],
# 'scoring': '1 punt voor een goed antwoord'}
#import pdb; pdb.set_trace()

def read_in_responses(file_path):
    input_file = csv.DictReader(open(file_path))
    responses = {}
    for row in input_file:
        row["score"] = int(row["score"])
        if row["item_id"] in responses:
            responses[row["item_id"]].append(row)
        if row["item_id"] not in responses:
            responses[row["item_id"]] = [row]
    return responses


def read_in_new_responses(file_path):
    input_file = csv.DictReader(open(file_path))
    responses = {}
    for row in input_file:
        if row["item_id"] in responses:
            responses[row["item_id"]].append(row)
        if row["item_id"] not in responses:
            responses[row["item_id"]] = [row]
    return responses

#responses = read_in_responses("/home/skrjanec/cito_opdracht/data/responses.csv")
#import pdb; pdb.set_trace()

def read_in_extended_answers(file_path):
    with open(file_path) as f_input:
        data = json.load(f_input)
    return data










