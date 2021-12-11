# Telegram PizzaBot

## Requirements
1. **Python 3.10** or higher is required
2. transitions
3. requests

## Usage
1. Install requirements
```
python -m pip install -r requirements.txt
```
2. Start `start.py`

You can also use bot apart from telegram API interface.<br />
Just import `PizzaBot` class into your script and call `chat()` method on it's example
#### Example:
```python
from bot import PizzaBot

bot = PizzaBot()

while True:
    print(bot.chat(input()))
```