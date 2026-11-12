# Note that the agent. prefix is required because the path towards the files
# is considered from the perspective of main.py, which is in the parent directory
from agent.memory import Memory
from agent.brain import Brain
from agent.planner.planner import Planner
from agent.embedder import Embedder
from agent.vector_store import VectorStore
from agent.knowledge_loader import KnowledgeLoader
from agent.executor import Executor
from agent.tool_registry import build_tool_registry

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.brain = Brain()
        self.planner = Planner(self.memory)
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.tool_registry = build_tool_registry(
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
        goal: str
    ):
        MAX_STEPS = 10
        executor = Executor(self.brain, self.memory, self.tool_registry, goal)

        for _ in range(MAX_STEPS):
            decision = self.planner.decide_next_step(
                executor,
                self.tool_registry
            )

            if decision["action"] == "error" or decision["action"] == "answer":
                return decision["response"]

            tool_name = decision["selected_tool"]
            tool_function = self.tool_registry[tool_name]["function"]
            arguments = decision["arguments"]
            result = tool_function(**arguments)
            self.memory.add_observation(f"tool: {tool_name}")
            self.memory.add_observation(f"tool arguments: {arguments}")
            self.memory.add_observation(f"result: {result}")
        return ("Reached maximum number of iterations.")