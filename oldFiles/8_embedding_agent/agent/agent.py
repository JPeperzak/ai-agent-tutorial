# Note that the agent. prefix is required because the path towards the files
# is considered from the perspective of main.py, which is in the parent directory
from agent.memory import Memory
from agent.brain import Brain
from agent.planner import Planner
from agent.embedder import Embedder
from agent.vector_store import VectorStore
from agent.knowledge_loader import KnowledgeLoader
from agent.tool_registry import build_tool_registry

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.brain = Brain()
        self.planner = Planner(
            self.brain
        )
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.tools = build_tool_registry(
            self.embedder,
            self.vector_store
        )
        self.load_knowledge()

    def load_knowledge(self):
        loader = KnowledgeLoader()
        documents = loader.load_documents("knowledge")
        for document in documents:
            embedding = self.embedder.embed(document["content"])
            self.vector_store.add_document(
                document["filename"],
                document["content"],
                embedding
            )

    def answer_question(
        self,
        question
    ):
        MAX_STEPS = 10

        for _ in range(MAX_STEPS):
            decision = self.planner.decide_next_step(
                question,
                self.memory.get_all(),
                self.tools
            )

            if decision["type"] == "error" or decision["type"] == "answer":
                return decision["response"]

            tool_name = decision["tool_name"]
            tool = self.tools[tool_name]
            tool_function = tool["function"]
            arguments = decision["tool_arguments"]
            result = tool_function(**arguments)
            self.memory.add(f"tool: {tool_name}")
            self.memory.add(f"tool arguments: {arguments}")
            self.memory.add(f"result: {result}")
        return ("Reached maximum number of iterations.")