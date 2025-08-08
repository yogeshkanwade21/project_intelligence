import logging

logger = logging.getLogger(__name__)

def extract_intent(query: str):
    logger.info(f"Extracting intent from query: {query}")
    normalized_query = query.lower()
    # Placeholder for intent extraction logic
    # In the future, this will maybe use an NLP library to extract intent
    if "assigned to" in normalized_query:
        intent = {"assignee": "Yogesh Kanwade"}
        logger.info(f"Extracted intent: {intent}")
        return intent
    if "how many bugs" in normalized_query:
        # intent = {"type": "bug_count", "timespan": "7d"}
        intent = {"type": "bug_count"}
        logger.info(f"Extracted intent: {intent}")
        return intent
    
    logger.warning(f"No intent found for query: {query}")
    return None
