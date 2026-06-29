from collections import deque
from typing import Deque, Dict


def needs_alert(local_score: float, peer_scores: Deque[float], threshold: float, peer_count: int) -> bool:
    if local_score < threshold:
        return False
    confirmed = sum(1 for score in peer_scores if score >= threshold)
    return confirmed >= peer_count


class PeerConsensus:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.peer_scores: Dict[str, Deque[float]] = {}

    def add_peer_score(self, peer_id: str, score: float) -> None:
        if peer_id not in self.peer_scores:
            self.peer_scores[peer_id] = deque(maxlen=self.window_size)
        self.peer_scores[peer_id].append(score)

    def summary(self) -> float:
        all_scores = [score for deque_ in self.peer_scores.values() for score in deque_]
        return float(sum(all_scores) / len(all_scores)) if all_scores else 0.0
