from collections import defaultdict

_history: dict[int, list[dict]] = defaultdict(list)
MAX_TURNS = 8

def get_history(user_id: int) -> list[dict]:
    return _history[user_id]

def add_turn(user_id: int, question: str, answer: str) -> None:
    _history[user_id].append({"role": "user", "content": question})
    _history[user_id].append({"role": "assistant", "content": answer})
    _history[user_id] = _history[user_id][-MAX_TURNS * 2:]

def clear_history(user_id: int) -> None:
    _history.pop(user_id, None)