import re
from typing import Dict, List, Any

class AgentManager:
    def __init__(self, memory, logger):
        self.agents: Dict[str, Any] = {}
        self.memory = memory
        self.logger = logger

    def register_agent(self, name: str, agent):
        self.agents[name] = agent

    def route(self, input_text: str) -> List[str]:
        # Simple keyword + intent matching
        agents_to_run = []
        if re.search(r'\banalyze\b', input_text, re.IGNORECASE):
            agents_to_run.append('shruti_parser')
        if re.search(r'\bbenchmark\b', input_text, re.IGNORECASE):
            agents_to_run.append('lora_evaluator')
        if re.search(r'\bquery\b|\bwhat\b|\bhow\b|\btell\b|\bexplain\b', input_text, re.IGNORECASE):
            agents_to_run.append('knowledge_agent')
        # If no match, default to knowledge agent
        if not agents_to_run:
            agents_to_run.append('knowledge_agent')
        return list(set(agents_to_run))  # Remove duplicates

    def execute(self, input_text: str) -> Dict[str, Any]:
        agents = self.route(input_text)
        results = {}
        trace = []
        for agent_name in agents:
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                self.logger.log(f"Running agent: {agent_name}")
                try:
                    # For different agents, input might differ, but for simplicity, pass input_text
                    # In real, parse input for specific params
                    output = agent.run(input_text)
                    results[agent_name] = output
                    trace.append({"agent": agent_name, "input": input_text, "output": output})
                except Exception as e:
                    self.logger.log(f"Error in {agent_name}: {e}")
                    results[agent_name] = {"error": str(e)}
                    trace.append({"agent": agent_name, "input": input_text, "output": {"error": str(e)}})
            else:
                self.logger.log(f"Agent {agent_name} not found")
                trace.append({"agent": agent_name, "input": input_text, "output": "Agent not found"})
        self.memory.save_session(input_text, results, trace)
        self.logger.save_session(input_text, results, trace)
        return {"results": results, "trace": trace}