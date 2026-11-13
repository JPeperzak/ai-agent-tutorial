import traceback

# Note that the agent. prefix is required because the path towards the files
# is considered from the perspective of main.py, which is in the parent directory
from agent.memory import Memory
from agent.brain import Brain
from agent.planner import Planner
from agent.executor import Executor
from agent.tool_registry import build_tool_registry
from agent.data_processing.embedder import Embedder
from agent.data_processing.knowledge_loader import KnowledgeLoader
from agent.data_processing.vector_store import VectorStore
from agent.data_processing.chunker import TextChunker

from agent.models.response import (
    PlanStepModel
)
from agent.models.data_types import (
    MemoryFact
)

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
        self.chunker = TextChunker()
        self.loader = KnowledgeLoader()
        self.prepare_knowledge()

    def prepare_knowledge(self):
        documents = self.loader.load_documents("knowledge")
        for document in documents:
            chunks = self.chunker.chunk_document(
                document["filename"],
                document["content"]
            )
            for chunk in chunks:
                chunk_object = chunk.model_dump()
                embedding = self.embedder.embed(
                    chunk_object["content"]
                )
                self.vector_store.add(
                    chunk,
                    embedding
                )

    def load_knowledge(self):
        documents = self.loader.load_documents("knowledge")
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
        executor = Executor(
            self.brain, 
            self.memory, 
            self.tool_registry, 
            goal
        )
        try:
            for _ in range(MAX_STEPS):
                next_action = self.planner.decide_next_action(
                    executor,
                )

                if next_action == "complete_step":
                    self.memory.complete_current_step()
                    continue
                if next_action == "tool":
                    result = self.planner.decide_tool(executor, self.tool_registry)
                    if result.get("error"):
                        self.memory.log_memory()
                        return result["error"]
                    tool_name = result["tool_name"]
                    arguments = result["arguments"]
                    tool_function = self.tool_registry[tool_name]["function"]
                    result = tool_function(**arguments)
                    observation = f"""Used tool: {tool_name} 
With arguments: {arguments} 
Result: {result}
"""
                    self.memory.add_observation(observation)
                    facts = executor.extract_facts(str(result))
                    self.memory.add_facts(
                        [
                            MemoryFact(
                                statement=fact["statement"],
                                source=fact["source"],
                            )
                            for fact in facts["facts"]
                        ]
                    )
                if next_action == "done":
                    finished = executor.assess_information()
                    if finished:
                        self.memory.log_memory()
                        return executor.generate_final_answer()
                    self.memory.plan.steps.append(
                        PlanStepModel(description="Gather additional information")
                    )
                    # INSTEAD OF ADDING A NEW STEP TO THE EXISTING PLAN, EVENTUALLY WE SHOULD
                    # USE A .replan() METHOD TO GENERATE A NEW PLAN WITH THE AVAILABLE INFORMATION.
                    # updated_plan = executor.replan()

                    # self.memory.set_plan(
                    #     updated_plan
                    # )
                    continue
        except BaseException as e:
            self.memory.log_memory()
            print("An error occurred:")
            traceback.print_exc()
            return ""

        self.memory.log_memory()
        return ("Reached maximum number of iterations.")