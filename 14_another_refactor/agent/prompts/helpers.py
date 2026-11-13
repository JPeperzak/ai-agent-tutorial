from agent.models.data_types import MemoryFact

def format_facts(facts: list[MemoryFact]) -> str:
    return "\n".join(f"- {fact.statement}" for fact in facts)