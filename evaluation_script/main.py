import numpy as np
import json
from bleu import Bleu
from f1 import F1
from utils import is_japanese_sentence, normalize_answer
from typing import Dict, Any

# compute f1 score
def compute_f1(a_gold: Dict[Any, str], a_pred: Dict[Any, str]):
    gts = {}
    res = {}
    for key in a_gold:
        answer = a_gold[key]
        gts[key] = normalize_answer(a_gold[key], is_japanese_sentence(answer))
        res[key] = normalize_answer(a_pred[key], is_japanese_sentence(answer))
    
    f1 = F1()
    score = f1.compute_score(gts, res)

    return score

# compute avg. BLEU score
def compute_avg_bleu(a_gold, a_pred):
    gts = {}
    res = {}
    for key in a_gold:
        answer = a_gold[key]
        gts[key] = [" ".join(normalize_answer(a_gold[key], is_japanese_sentence(answer)))]
        res[key] = [" ".join(normalize_answer(a_pred[key], is_japanese_sentence(answer)))]

    bleu = Bleu()
    scores, _ = bleu.compute_score(gts, res)

    return np.array(scores).mean()


def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    """
    Evaluates the submission for a particular challenge phase and returns score
    Arguments:

        `test_annotations_file`: Path to test_annotation_file on the server
        `user_submission_file`: Path to file submitted by the user
        `phase_codename`: Phase to which submission is made

        `**kwargs`: keyword arguments that contains additional submission
        metadata that challenge hosts can use to send slack notification.
        You can access the submission metadata
        with kwargs['submission_metadata']

        Example: A sample submission metadata can be accessed like this:
        >>> print(kwargs['submission_metadata'])
        {
            'status': u'running',
            'when_made_public': None,
            'participant_team': 5,
            'input_file': 'https://abc.xyz/path/to/submission/file.json',
            'execution_time': u'123',
            'publication_url': u'ABC',
            'challenge_phase': 1,
            'created_by': u'ABC',
            'stdout_file': 'https://abc.xyz/path/to/stdout/file.json',
            'method_name': u'Test',
            'stderr_file': 'https://abc.xyz/path/to/stderr/file.json',
            'participant_team_name': u'Test Team',
            'project_url': u'http://foo.bar',
            'method_description': u'ABC',
            'is_public': False,
            'submission_result_file': 'https://abc.xyz/path/result/file.json',
            'id': 123,
            'submitted_at': u'2017-03-20T19:22:03.880652Z'
        }
    """

    with open(test_annotation_file) as f:
        ground_truth = json.load(f)
        
    with open(user_submission_file) as f:
        results = json.load(f)

    f1 = compute_f1(ground_truth, results)
    bleu = compute_avg_bleu(ground_truth, results)

    output = {}
    if phase_codename == "public_test":
        print("Evaluating for Public Test Phase")
        output["result"] = {
            "public_test_split": {
                "Avg. BLEU": bleu,
                "F1": f1
            }
        }
        # To display the results in the result file
        output["submission_result"] = output["result"]["public_test_split"]
        print("Completed evaluation for Public Test Phase")
    elif phase_codename == "private_test":
        print("Evaluating for Private Test Phase")
        output["result"] = {
            "private_test_split": {
                "Avg. BLEU": bleu,
                "F1": f1
            }
        }
        # To display the results in the result file
        output["submission_result"] = output["result"]["private_test_split"]
        print("Completed evaluation for Private Test Phase")
    return output
