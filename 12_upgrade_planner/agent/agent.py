import traceback

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

from agent.planner.models import (
    PlanStepModel
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

    def test_answer_question(
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