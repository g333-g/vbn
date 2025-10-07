from django.shortcuts import render
from .forms import PuzzleForm
import math
import random

def index(request):
    result = None
    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['number']
            t = form.cleaned_data['text']

            # Number puzzle
            is_even = (n % 2 == 0)
            if is_even:
                number_msg = f"The number {n} is even. Its square root is {math.sqrt(n)}."
            else:
                number_msg = f"The number {n} is odd. Its cube is {n ** 3}."

            # Text puzzle: binary + vowel count (aeiou, case-insensitive)
            binary_str = ' '.join(format(ord(c), '08b') for c in t)
            vowels = sum(1 for c in t.lower() if c in 'aeiou')
            text_msg = f"Binary: {binary_str} | Vowel Count: {vowels}"

            # Treasure hunt: simulate guessing 1-100, win if <= 5 tries
            secret = random.randint(1, 100)
            attempts = []
            low, high = 1, 100
            won = False
            for i in range(1, 6):
                guess = (low + high) // 2
                if guess > secret:
                    attempts.append(f"Attempt {i}: {guess} (Too high!)")
                    high = guess - 1
                elif guess < secret:
                    attempts.append(f"Attempt {i}: {guess} (Too low!)")
                    low = guess + 1
                else:
                    attempts.append(f"Attempt {i}: {guess} (Correct!)")
                    won = True
                    break
            treasure_msg = f"The secret number is {secret}. " + " ".join(attempts)
            if won:
                treasure_msg += f" You found the treasure in {len(attempts)} attempts!"

            result = {
                'number_msg': number_msg,
                'text_msg': text_msg,
                'treasure_msg': treasure_msg,
            }
    else:
        form = PuzzleForm()

    return render(request, 'puzzle/index.html', {'form': form, 'result': result})

