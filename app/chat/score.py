import random
from app.chat.redis import client

def random_component_by_score(component_type, component_map):
    # Make sure component_type is 'llm', 'retriever', or 'memory'
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError(f"Invalid component type")

    # From redis, get the hash containing the sum total scores for the given component_type
    values = client.hgetall(f"{component_type}_score_values")
    # From redis, get the hash containing the number of times each component has been voted on
    counts = client.hgetall(f"{component_type}_score_counts")
    # Get all the valid component names from the component map
    names = component_map.keys()

    # Loop over those valid names and use them to calculate the average score for each
    # Add average score to a dictionary
    avg_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        avg = score / count
        avg_scores[name] = max(avg, 0.1)

    # Do a weighted random selection
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in avg_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name


def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score, 0), 1)

    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)

    client.hincrby("retriever_score_values", llm, score)
    client.hincrby("retriever_score_counts", llm, 1)

    client.hincrby("memory_score_values", llm, score)
    client.hincrby("memory_score_counts", llm, 1)

def get_scores():
    """

    Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [avg_score],
                'chatopenai-4': [avg_score]
            },
            'retriever': { 'pinecone_store': [avg_score] },
            'memory': { 'persist_memory': [avg_score] }
        }
    """

    pass
