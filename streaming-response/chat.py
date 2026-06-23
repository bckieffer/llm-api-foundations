import os
import sys
import logging
import time
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

def count_tokens(messages, model_name):
    encoding = tiktoken.encoding_for_model(model_name)
    token_count = 0
    for message in messages:
        token_count += 4
        for value in message.values():
            token_count += len(encoding.encode(value))
    return token_count

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

            stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True
            )

            assistant_message = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    assistant_message += content

            elapsed_time = time.perf_counter() - start_time

            print("\n")

            messages.append({"role": "assistant", "content": assistant_message})

            input_tokens = count_tokens(messages[:-1], model_name)
            output_tokens = len(tiktoken.encoding_for_model(model_name).encode(assistant_message))
            total_tokens = input_tokens + output_tokens

            logging.info(
                f"API Response - Latency: {elapsed_time:.2f}s | "
                f"Input tokens: {input_tokens} | "
                f"Output tokens: {output_tokens} | "
                f"Total tokens: {total_tokens} (estimated)"
            )

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break

        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()
