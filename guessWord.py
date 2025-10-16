#!/usr/bin/env python3
"""
Simple Word Guessing Game with Easy AI Hints

A fun and easy word guessing game where AI gives simple, human-like hints.
"""

import os
import random
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_simple_hint(secret_word, guess):
    """
    Generate a very simple and easy hint using OpenAI API.
    
    Args:
        secret_word (str): The correct word to guess
        guess (str): The player's incorrect guess
    
    Returns:
        str: A simple, easy hint from OpenAI
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly helper. Give VERY SIMPLE hints for a word guessing game. Use easy words that anyone can understand. Give hints like: 'It starts with letter X', 'It has 5 letters', 'It's an animal', 'It's something you eat', etc. Keep it super simple - like talking to a child. Only 1 sentence."
                },
                {
                    "role": "user",
                    "content": f"The secret word is '{secret_word}' and the player guessed '{guess}'. Give a very simple hint."
                }
            ],
            max_tokens=50,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback simple hints
        if len(guess) != len(secret_word):
            return f"It has {len(secret_word)} letters, not {len(guess)}."
        else:
            return f"Try a different word with {len(secret_word)} letters."

def play_word_guessing_game():
    """Main game function that handles the word guessing game loop."""
    
    # Simple, everyday words that are easy to guess
    word_list = [
        "cat", "dog", "sun", "moon", "tree", "house", "car", "book",
        "fish", "bird", "cake", "milk", "water", "apple", "orange",
        "happy", "smile", "music", "dance", "friend", "family",
        "school", "teacher", "student", "pizza", "chicken", "pizza"
    ]
    
    # Select a random secret word
    secret_word = random.choice(word_list).lower()
    
    print("🎮 Welcome to the Simple Word Guessing Game!")
    print("=" * 45)
    print(f"💡 I'm thinking of a word with {len(secret_word)} letters.")
    print("🤖 I'll give you easy hints when you guess wrong!")
    print("=" * 45)
    
    attempts = 0
    max_attempts = 8
    
    while attempts < max_attempts:
        try:
            # Get player's guess
            guess = input(f"\n🎯 Your guess (try {attempts + 1}/{max_attempts}): ").strip().lower()
            
            if not guess:
                print("❌ Please enter a word!")
                continue
            
            attempts += 1
            
            # Check if guess is correct
            if guess == secret_word:
                print(f"\n🎉 YES! You got it!")
                print(f"🏆 The word was '{secret_word.upper()}'!")
                print(f"🎯 You guessed it in {attempts} try{'ies' if attempts != 1 else ''}!")
                return True
            
            # Generate and display simple hint
            print(f"\n❌ '{guess}' is not right.")
            if attempts < max_attempts:
                print("🤖 Let me help you...")
                hint = get_simple_hint(secret_word, guess)
                print(f"💡 {hint}")
            else:
                print(f"\n😔 Game Over! No more tries left.")
                print(f"🎯 The word was: '{secret_word.upper()}'")
                return False
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Bye! The word was '{secret_word.upper()}'")
            return False
        except Exception as e:
            print(f"❌ Something went wrong: {e}")
            continue
    
    return False

def main():
    """Main entry point of the application."""
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ You need to set your OpenAI API key first!")
        print("💡 Run this command:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\n🔗 Get your key from: https://platform.openai.com/api-keys")
        return
    
    try:
        # Play the game
        won = play_word_guessing_game()
        
        # Ask if player wants to play again
        while True:
            play_again = input(f"\n🔄 Play again? (y/n): ").strip().lower()
            if play_again in ['y', 'yes']:
                print("\n" + "=" * 50)
                play_word_guessing_game()
            elif play_again in ['n', 'no']:
                print("\n👋 Thanks for playing!")
                break
            else:
                print("❌ Just type 'y' or 'n'")
                
    except Exception as e:
        print(f"❌ Oops! Something went wrong: {e}")

if __name__ == "__main__":
    main()