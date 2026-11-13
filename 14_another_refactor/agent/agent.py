import traceback

# Note that the agent. prefix is required because the path towards the files
# is considered from the perspective of main.py, which is in the parent directory
from agent.memory import Memory
from agent.brain import Brain, StructuredOutputError
from agent.planner import Planner
from agent.executor import Executor
from agent.tool_registry import build_tool_registry
from agent.data_processing.embedder import Embedder
from agent.data_processing.knowledge_loader import KnowledgeLoader
from agent.data_processing.vector_store import VectorStore
from agent.data_processing.chunker import TextChunker

from agent.models.response import (
    PlanStepModel,
    Action
)
from agent.models.data_types import (
    MemoryFact,
    ToolResult,
)

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.brain = Brain()
        self.planner = Planner(self.memory)
        self.embedder = Embedder()
        self.vector_store = VectorStore(self.embedder)
        self.chunker = TextChunker()
        self.tool_registry = build_tool_registry(
            self.embedder,
            self.vector_store,
            self.chunker
        )
        self.loader = KnowledgeLoader()
        self.prepare_knowledge()

    def prepare_knowledge(self):
        documents = self.loader.load_documents("knowledge")
        for document in documents:
            chunks = self.chunker.chunk_document(
                document.file_name,
                document.content
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

    def answer_question(
        self,
        goal: str
    ):
        self.memory.reset()
        MAX_ITERATIONS = 25
        MAX_TOOL_CALLS = 6
        tool_calls = 0
        executor = Executor(
            self.brain, 
            self.memory, 
            self.tool_registry, 
            goal
        )
        try:
            for _ in range(MAX_ITERATIONS):
                next_action = self.planner.decide_next_action(
                    executor,
                )
                match next_action:
                    case Action.COMPLETE_STEP:
                        self.memory.complete_current_step()
                        continue
                    case Action.TOOL:
                        if tool_calls >= MAX_TOOL_CALLS:
                            self.memory.add_observation("Tool call budget exhausted.")
                            self.memory.log_memory()
                            return executor.generate_final_answer()
                        tool_calls += 1
                        result = self.planner.decide_tool(executor, self.tool_registry)
                        tool_name = result.tool_name
                        arguments = result.arguments
                        tool_function = self.tool_registry[tool_name].function
                        try:
                            result = tool_function(**arguments)
                        except Exception as e:
                            result = ToolResult(message=f"The tool failed with an error: {e}")

                        observation = f"""Used tool: {tool_name} 
With arguments: {arguments} 
Result: {result.to_text()}
"""
                        self.memory.add_observation(observation)
                        # If there is nothing to extract, move on and let the observation tell the agent what happened
                        if not result.has_results():
                            continue

                        # We're gonna perform one fact-extraction call per source, with the source attached in the code
                        contents_by_source: dict[str, list[str]] = {}
                        for passage in result.passages:
                            contents_by_source.setdefault(passage.source, []).append(passage.content)

                        for source, contents in contents_by_source.items():
                            extracted = executor.extract_facts("\n\n".join(contents))
                            self.memory.add_facts(
                                [
                                    MemoryFact(
                                        statement=fact.statement,
                                        source=source,
                                    )
                                    for fact in extracted.facts
                                ]
                            )

                    case Action.DONE:
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
        except StructuredOutputError as e:
            self.memory.log_memory()
            return f"I could not get a valid response from the model: {e}"
        except Exception as e:
            self.memory.log_memory()
            print("An error occurred:")
            traceback.print_exc()
            return f"An unexpected error occurred: {e}"

        self.memory.log_memory()
        return ("Reached maximum number of iterations.")