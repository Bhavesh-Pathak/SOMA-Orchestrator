# Test Scenarios

## Scenario 1: Text Analysis

**Input**: "Analyze the sentiment of this happy poem"

**Expected Agents**: Shruti Parser

**Expected Output**: JSON with sentiment, entities, etc.

## Scenario 2: Benchmarking

**Input**: "Benchmark llama-7b-lora and mistral-7b-lora models"

**Expected Agents**: LoRA Evaluator

**Expected Output**: Dict with model metrics

## Scenario 3: Multi-Agent Query

**Input**: "Analyze this text and tell me about AI"

**Expected Agents**: Shruti Parser, Knowledge Agent

**Expected Output**: Combined results from both agents

## Scenario 4: Knowledge Query

**Input**: "What is machine learning?"

**Expected Agents**: Knowledge Agent

**Expected Output**: Retrieved chunks from knowledge base

## Scenario 5: No Match

**Input**: "Hello world"

**Expected Agents**: Knowledge Agent (default)

**Expected Output**: Knowledge response or default message