import os
import sys
import logging
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    # Initialize the client. It automatically picks up the OPENAI_API_KEY env variable.
    # To use local models (like Ollama), change base_url to "http://localhost:11434/v1"
    client = OpenAI()

    # Define the model to use
    model_name = "gpt-4o-mini"

    # Maintain the conversation history to give the LLM context
    messages = [
        {"role": "system", "content": "You are a helpful, concise terminal assistant."}
    ]

    print("====================================================")
    print(f"LLM CLI Chat Initialized ({model_name})")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("====================================================\n")

    logging.info(f"Chat session started with model: {model_name}")

    while True:
        try:
            user_input = input("You: ").strip()  
   
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
                
            if not user_input:
                continue

         
            messages.append({"role": "user", "content": user_input})

            print("AI: ", end="", flush=True)

            start_time = time.perf_counter()
            
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
            )
            
            elapsed_time = time.perf_counter() - start_time

            assistant_message = response.choices[0].message.content
            
            print(assistant_message)

            print("\n")

            messages.append({"role": "assistant", "content": assistant_message})

            usage = response.usage
            logging.info(
                f"API Response - Latency: {elapsed_time:.2f}s | "
                f"Input tokens: {usage.prompt_tokens} | "
                f"Output tokens: {usage.completion_tokens} | "
                f"Total tokens: {usage.total_tokens}"
            )

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break

        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()
