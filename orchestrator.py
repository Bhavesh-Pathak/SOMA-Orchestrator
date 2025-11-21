import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.manager import AgentManager
from core.memory import Memory
from core.logging import Logger
from agents.shruti_parser import ShrutiParserAgent
from agents.lora_evaluator import LoRAEvaluatorAgent
from agents.knowledge_agent import KnowledgeAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py 'your query here'")
        return

    input_text = ' '.join(sys.argv[1:])

    # Initialize components
    memory = Memory()
    logger = Logger()
    manager = AgentManager(memory, logger)

    # Register agents
    manager.register_agent('shruti_parser', ShrutiParserAgent())
    manager.register_agent('lora_evaluator', LoRAEvaluatorAgent())
    manager.register_agent('knowledge_agent', KnowledgeAgent())

    # Execute
    result = manager.execute(input_text)

    # Print results
    print("Execution Results:")
    for agent, output in result['results'].items():
        print(f"{agent}: {output}")

if __name__ == '__main__':
    main()