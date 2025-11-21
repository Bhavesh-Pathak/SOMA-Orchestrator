# Architecture

## Overview

Soma-Orchestrator-Core is a modular orchestrator that coordinates multiple AI agents dynamically based on user input.

## Components

- **AgentManager**: Routes input to appropriate agents
- **Agents**: Specialized micro-services
  - Shruti Parser
  - LoRA Evaluator
  - Knowledge Agent
- **Memory**: SQLite-based session storage
- **Logging**: Terminal and file logging

## Flow

```mermaid
graph TD
    A[User Input] --> B[AgentManager]
    B --> C{Keyword Match}
    C -->|analyze| D[Shruti Parser]
    C -->|benchmark| E[LoRA Evaluator]
    C -->|query| F[Knowledge Agent]
    D --> G[Results]
    E --> G
    F --> G
    G --> H[Memory]
    G --> I[Logging]
    H --> J[SQLite DB]
    I --> K[Logs/]
    I --> L[Demo Loops/]
```

## Agent Details

- **Shruti Parser**: Calls external HTTP service for text analysis
- **LoRA Evaluator**: Mocks benchmarking of LoRA models
- **Knowledge Agent**: FAISS-based retrieval from local documents

## Data Flow

1. Input parsed for keywords
2. Agents selected and executed
3. Results collected and logged
4. Session saved to memory and demo files