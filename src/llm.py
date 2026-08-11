"""
Local LLM using llama.cpp
"""

from llama_cpp import Llama


class LocalLLM:
    def __init__(self, model_path: str, context_length: int = 2048, threads: int = 4):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=context_length,
            n_threads=threads,
            verbose=False
        )
    
    def complete(self, prompt: str, max_tokens: int = 256, temperature: float = 0.1) -> str:
        """Generate completion for a prompt"""
        
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["\n\n", "User:", "Query:"],
            echo=False
        )
        
        return output['choices'][0]['text'].strip()