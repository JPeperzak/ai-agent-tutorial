# A tool is a function the agent can execute to acquire information it does not implicitly have access to.
def get_temperature(location: str):
    temps = {
        "new york": "22°C",
        "london": "15°C",
        "amsterdam": "8°C",
        "brussels": "12°C",
        "paris": "20°C",
    }
    return temps.get(location, "Unknown")

def get_age_category(age: int):
    return "young" if age < 30 else "old"