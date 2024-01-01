import random
from app.chat.redis import client

def random_component_by_score(component_type: str, component_map: dict):
    # Ensure that we have a valid component type in the argument
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError("Invalid component_type")
    
    # Get total score from redis hash for a component type
    score_values = client.hgetall(f"{component_type}_score_values")
     
    # Get total counts from redis hash for a component type
    score_counts = client.hgetall(f"{component_type}_score_counts")
    
    # Get all valid component names from component map
    names = component_map.keys()
    avg_scores = {}
    for name in names:
        score = int(score_values.get(name, 1))
        count = int(score_counts.get(name, 1))
        avg = score / count
        avg_scores[name] = max(avg, 0.1) # no component ever gets 0 which can lead to it never being picked 
    
    # Do a weighted random selection
    sum_avg_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_avg_scores)
    cumulative = 0
    for name, score in avg_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name
    

"""
    This function interfaces with langfuse to assign a score to a conversation, specified by its ID.
    It creates a new langfuse score utilizing the provided llm, retriever, and memory components.
    The details are encapsulated in JSON format and submitted along with the conversation_id and the score.

    :param conversation_id: The unique identifier for the conversation to be scored.
    :param score: The score assigned to the conversation.
    :param llm: The Language Model component information.
    :param retriever: The Retriever component information.
    :param memory: The Memory component information.

    Example Usage:

    score_conversation('abc123', 0.75, 'llm_info', 'retriever_info', 'memory_info')
"""
def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    
    # score should always be between 0 and 1
    score = min(max(score, 0), 1)

    # save values to redis database
    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)

    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_counts", retriever, 1)

    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_counts", memory, 1)


"""
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

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
def get_scores():
    aggregate = {"llm": {}, "retriever": {}, "memory": {}}
    
    for component_type in aggregate.keys():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")
        
        names = values.keys()
        for name in names:
            # eg. for every model of llm
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg_score = score / count
            aggregate[component_type][name] = [avg_score]
    
    return aggregate