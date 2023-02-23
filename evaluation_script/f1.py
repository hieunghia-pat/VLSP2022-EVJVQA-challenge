import numpy as np
from typing import Dict, List, Any

class F1:
    def precision(self, gt: List[str], r: List[str]) -> float:
        common = set(gt) & set(r)
        return len(common) / len(set(r))

    def recall(self, gt: List[str], r: List[str]) -> float:
        common = set(gt) & set(r)
        return len(common) / len(set(gt))

    def compute(self, gt: List[str], r: List[str]) -> float:
        # if either the prediction or the truth is no-answer then f1 = 1 if they agree, 0 otherwise
        if len(r) == 0 or len(gt) == 0:
            return int(r == gt)

        precision = self.precision(gt, r)
        recall = self.recall(gt, r)

        if precision == 0 or recall == 0:
            return 0

        f1 = 2*precision*recall / (precision+recall)

        return f1

    def compute_score(self, gts: Dict[Any, List[str]], res: Dict[Any, List[str]]):
        assert isinstance(gts, dict), "gts must be a dict where values are lists of strings"
        assert isinstance(res, dict), "res must be a dict where values are lists of strings"
        assert(gts.keys() == res.keys()), "gts and res must have exactly the same keys"

        scores = []
        for key in gts:
            gt = gts[key]
            r = res[key]
            scores.append(self.compute(gt, r))

        return np.array(scores).mean()