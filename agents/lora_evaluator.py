import re
import os
import subprocess
import json

class LoRAEvaluatorAgent:
    def __init__(self):
        self.benchmark_script = os.path.join(os.path.dirname(__file__), '../../Mini LoRA Benchmark Kit/run_benchmark.py')
        self.results_path = os.path.join(os.path.dirname(__file__), '../../Mini LoRA Benchmark Kit/results/results.json')

    def run(self, input_text: str) -> dict:
        try:
            # Run the benchmark script
            subprocess.run(['python', self.benchmark_script], check=True, cwd=os.path.dirname(self.benchmark_script))
            
            # Read the results
            if os.path.exists(self.results_path):
                with open(self.results_path, 'r') as f:
                    results = json.load(f)
                
                # Format the results
                formatted_results = {
                    "base_model": {
                        "accuracy": results.get("base_eval", {}).get("eval_accuracy"),
                        "f1_score": results.get("base_eval", {}).get("eval_f1"),
                        "latency_s": results.get("base_latency_s"),
                        "tokens_per_sec": results.get("base_tokens_per_sec")
                    },
                    "lora_model": {
                        "accuracy": results.get("lora_eval", {}).get("eval_accuracy"),
                        "f1_score": results.get("lora_eval", {}).get("eval_f1"),
                        "latency_s": results.get("lora_latency_s"),
                        "tokens_per_sec": results.get("lora_tokens_per_sec")
                    }
                }
                return formatted_results
            else:
                return {"error": "Benchmark results file not found"}
        except subprocess.CalledProcessError as e:
            return {"error": f"Benchmark failed: {e}"}
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}