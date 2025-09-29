# AI Chess Arena

An exciting chess application where two AI neural networks battle against each other! Watch as different AI models from OpenRouter play strategic chess games in real-time with a beautiful graphical interface.

## Features

- **AI vs AI Chess Battles**: Watch two different AI models compete
- **Multiple AI Models**: Choose from various free models on OpenRouter.ai
- **Real-time Visualization**: Beautiful chess board with live game updates
- **Game Logging**: Track moves and game progress
- **Easy Configuration**: Simple API key setup and model selection
- **Game Speed Control**: Adjustable delay between moves (0.1-10 seconds)
- **Game Result Dialog**: Clear notification when game ends with winner
- **Cross-platform**: Works on Windows, Linux, and macOS

## Screenshots

The application features a clean, modern interface with:
- Interactive chess board with piece visualization
- Model selection for white and black pieces  
- Real-time game log and status updates
- Easy API key configuration

## Prerequisites

- Python 3.7 or higher
- An OpenRouter.ai account and API key (free tier available)

## Installation

### Windows

1. **Install Python** (if not already installed):
   - Download Python from [python.org](https://www.python.org/downloads/windows/)
   - During installation, make sure to check "Add Python to PATH"

2. **Clone or download this repository**:
   ```cmd
   git clone https://github.com/kavumi22/ai-chess-arena.git
   cd ai-chess-arena
   ```

3. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```cmd
   python main.py
   ```

### Ubuntu/Debian Linux

1. **Install Python and pip**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-tkinter git
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/kavumi22/ai-chess-arena.git
   cd ai-chess-arena
   ```

3. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

   **Note**: To run the application in the future, always activate the virtual environment first:
   ```bash
   source venv/bin/activate
   python main.py
   ```

### Fedora/CentOS/RHEL Linux

1. **Install Python and dependencies**:
   ```bash
   sudo dnf install python3 python3-pip python3-tkinter git
   # For CentOS/RHEL: sudo yum install python3 python3-pip tkinter git
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/kavumi22/ai-chess-arena.git
   cd ai-chess-arena
   ```

3. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

   **Note**: To run the application in the future, always activate the virtual environment first:
   ```bash
   source venv/bin/activate
   python main.py
   ```

### Arch Linux

1. **Install Python and dependencies**:
   ```bash
   sudo pacman -S python python-pip tk git
   # If tkinter is missing, install from AUR:
   yay -S python-tkinter
   # Or using paru: paru -S python-tkinter
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/kavumi22/ai-chess-arena.git
   cd ai-chess-arena
   ```

3. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

   **Note**: To run the application in the future, always activate the virtual environment first:
   ```bash
   source venv/bin/activate
   python main.py
   ```

### macOS

1. **Install Python** (using Homebrew - recommended):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python-tk git
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/kavumi22/ai-chess-arena.git
   cd ai-chess-arena
   ```

3. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

   **Note**: To run the application in the future, always activate the virtual environment first:
   ```bash
   source venv/bin/activate
   python main.py
   ```

   **Alternative**: Use the provided script: `./run.sh`

## Getting Your OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to the [API Keys section](https://openrouter.ai/keys)
4. Create a new API key
5. Copy your API key (keep it secure!)

## Quick Start Guide

1. **Launch the application**:
   ```bash
   python main.py  # or python3 main.py on Linux/macOS
   ```

2. **Configure your API key**:
   - Paste your OpenRouter API key in the "OpenRouter API Key" field
   - Click "Save API Key" to store it securely

3. **Select AI models**:
   - Choose a model for White pieces (e.g., "openai/gpt-3.5-turbo")
   - Choose a different model for Black pieces (e.g., "meta-llama/llama-2-70b-chat")

4. **Adjust game speed** (optional):
   - Use the "Move delay" slider to control time between moves
   - Range: 0.1 seconds (fast) to 10 seconds (slow)
   - Default: 2 seconds per move

5. **Start the battle**:
   - Click "Start Game" to begin the AI vs AI match
   - Watch the game progress in real-time
   - View move history in the game log
   - Game result will appear in a dialog when finished

6. **Control the game**:
   - Use "Stop Game" to pause the current match
   - Use "Reset Board" to start fresh

## Available Free Models

Some popular free models on OpenRouter include:
- `openai/gpt-3.5-turbo`
- `meta-llama/llama-2-70b-chat`
- `anthropic/claude-3-haiku`
- `mistralai/mistral-7b-instruct`
- `google/gemma-7b-it`

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'chess'"**
```bash
pip install chess
```

**"ModuleNotFoundError: No module named 'tkinter'" or "ImportError: libtk8.6.so" (Linux)**
```bash
# Ubuntu/Debian:
sudo apt install python3-tkinter

# Fedora/CentOS:
sudo dnf install python3-tkinter

# Arch Linux:
sudo pacman -S tk
# If still not working, try:
yay -S python-tkinter
# or
sudo pacman -S tkinter
```

**API Connection Issues**
- Verify your API key is correct
- Check your internet connection
- Ensure you have available credits on OpenRouter (free tier included)

**Application Won't Start**
- Make sure you're using Python 3.7+
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Try running with verbose output: `python -v main.py`

### Performance Tips

- Some AI models may take longer to respond than others
- For faster games, choose lighter models like `mistral-7b-instruct`
- For more strategic gameplay, try larger models like `llama-2-70b-chat`

### Virtual Environment Notes

- **Linux/macOS users**: The application uses virtual environments to avoid conflicts with system packages
- **Quick start**: Simply run `./run.sh` - it will automatically create and activate the virtual environment
- **Manual activation**: If you installed manually, remember to activate the virtual environment before running:
  ```bash
  source venv/bin/activate
  python main.py
  ```
- **Windows users**: Virtual environments are optional but recommended

## Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with the `python-chess` library for chess logic
- Uses OpenRouter.ai for AI model access
- Interface built with Python's tkinter

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information about your problem

---

**Enjoy watching AI models battle it out on the chess board!** 🤖♟️
