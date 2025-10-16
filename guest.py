import os
import random
from openai import OpenAI

def main():
    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    # List of words for the game
    words = [
        "python", "computer", "programming", "algorithm", "database",
        "function", "variable", "loop", "condition", "debugging",
        "software", "hardware", "network", "security", "encryption",
        "artificial", "intelligence", "machine", "learning", "neural"
    ]
    
    # Select a random word
    target_word = random.choice(words).lower()
    
    print("🎯 Welcome to the Word Guessing Game!")
    print("I'm thinking of a word. Can you guess what it is?")
    print("Type your guesses below (one word at a time):")
    print("-" * 50)
    
    guess_count = 0
    
    while True:
        # Get user input
        guess = input("\nYour guess: ").lower().strip()
        guess_count += 1
        
        # Check if the guess is correct
        if guess == target_word:
            print("\n🎉 Congratulations! You guessed it!")
            print(f"The word was: {target_word.upper()}")
            print(f"You took {guess_count} guess{'es' if guess_count > 1 else ''}!")
            print("🎊 Well done! 🎊")
            break
        
        # Generate hint using OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are a helpful assistant giving hints for a word guessing game. The target word is '{target_word}'. The player guessed '{guess}' which is incorrect. Give a helpful hint without revealing the word directly. Keep it encouraging and concise (1-2 sentences max)."
                    },
                    {
                        "role": "user", 
                        "content": f"Give me a hint for the word '{target_word}' after my incorrect guess of '{guess}'"
                    }
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            hint = response.choices[0].message.content.strip()
            print(f"\n💡 Hint: {hint}")
            
        except Exception as e:
            # Fallback hint if API fails
            if len(guess) < len(target_word):
                print(f"\n💡 Hint: The word has {len(target_word)} letters.")
            elif len(guess) > len(target_word):
                print(f"\n💡 Hint: The word has {len(target_word)} letters.")
            else:
                print(f"\n💡 Hint: The word has {len(target_word)} letters. Keep trying!")
        
        print(f"(Attempt #{guess_count})")

if __name__ == "__main__":
    main()
