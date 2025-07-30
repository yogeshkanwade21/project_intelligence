import logging

logger = logging.getLogger(__name__)

def generate_jql(intent: dict):
    logger.info(f"Generating JQL from intent: {intent}")
    # Placeholder for JQL generation logic
    # In the future, this will use the extracted intent to build a JQL query
    if intent.get("type") == "bug_count":
        timespan = intent.get("timespan", "7d")
        # jql = f"issuetype = Bug AND created >= -{timespan}"
        jql = "issuetype = Bug"
        logger.info(f"Generated JQL: {jql}")
        return jql
    
    logger.warning(f"Could not generate JQL for intent: {intent}")
    return None
