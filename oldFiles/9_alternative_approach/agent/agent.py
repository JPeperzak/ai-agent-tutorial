from agent.memory import Memory
from agent.executor import Executor
from agent.planner import Planner
from agent.embedder import Embedder
from agent.vector_store import VectorStore
from agent.knowledge_loader import KnowledgeLoader
from agent.tool_registry import build_tool_registry
from agent.state.agent_state import AgentState
from agent.constants.ActionTypeEnum import ActionType

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.planner = Planner()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.registry = build_tool_registry(
            self.embedder,
            self.vector_store
        )
        self.load_knowledge()

        self.executor = Executor(self.registry)

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
        user_request
    ):
        MAX_STEPS = 10
        state = AgentState(user_request)
        for _ in range(MAX_STEPS):
            if not state.finished:
                step = self.planner.decide_next_step(state)
                match step:
                    case ActionType.SELECT_TOOL:
                        self.executor.select_tool(state)
                    case ActionType.GENERATE_ARGUMENTS:
                        self.executor.generate_arguments(state)
                    case ActionType.EXECUTE_TOOL:
                        self.executor.execute_tool(state)
                    case ActionType.ANSWER:
                        return state.final_answer
                


            # if decision["type"] == "error" or decision["type"] == "answer":
            #     return decision["response"]

            # tool_name = decision["tool_name"]
            # tool = self.tools[tool_name]
            # tool_function = tool["function"]
            # arguments = decision["tool_arguments"]
            # result = tool_function(**arguments)
            # self.memory.add(f"tool: {tool_name}")
            # self.memory.add(f"tool arguments: {arguments}")
            # self.memory.add(f"result: {result}")
        return ("Reached maximum number of iterations.")