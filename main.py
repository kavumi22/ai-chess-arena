import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import time
from chess_engine import ChessGame
from openrouter_client import OpenRouterClient

class ChessArenaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Chess Arena")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        self.game = ChessGame()
        self.client = OpenRouterClient()
        self.game_running = False
        self.move_delay = 2.0
        
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(control_frame, text="OpenRouter API Key:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.api_key_var = tk.StringVar()
        tk.Entry(control_frame, textvariable=self.api_key_var, show="*", width=40).grid(row=0, column=1, padx=(0, 5))
        tk.Button(control_frame, text="Save API Key", command=self.save_api_key).grid(row=0, column=2, padx=(0, 10))
        
        tk.Label(control_frame, text="White Model:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.white_model_var = tk.StringVar()
        self.white_model_combo = ttk.Combobox(control_frame, textvariable=self.white_model_var, width=35)
        self.white_model_combo.grid(row=1, column=1, padx=(0, 5))
        
        tk.Label(control_frame, text="Black Model:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.black_model_var = tk.StringVar()
        self.black_model_combo = ttk.Combobox(control_frame, textvariable=self.black_model_var, width=35)
        self.black_model_combo.grid(row=2, column=1, padx=(0, 5))
        
        tk.Label(control_frame, text="Move delay (seconds):").grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
        self.speed_var = tk.StringVar(value="2.0")
        speed_frame = tk.Frame(control_frame)
        speed_frame.grid(row=3, column=1, sticky=tk.W, padx=(0, 5))
        
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=10.0, resolution=0.1, 
                                  orient=tk.HORIZONTAL, variable=self.speed_var, length=200)
        self.speed_scale.pack(side=tk.LEFT)
        
        tk.Label(speed_frame, textvariable=self.speed_var).pack(side=tk.LEFT, padx=(5, 0))
        self.speed_scale.bind("<Motion>", self.update_speed)
        
        button_frame = tk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        tk.Button(button_frame, text="Start Game", command=self.start_game, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Stop Game", command=self.stop_game, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reset Board", command=self.reset_board, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Test API", command=self.test_api, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        
        game_frame = tk.Frame(main_frame)
        game_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(game_frame, bg="white", width=640, height=640)
        self.canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        info_frame = tk.Frame(game_frame)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(info_frame, text="Game Log:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        log_frame = tk.Frame(info_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, width=40, height=20, font=("Courier", 10))
        scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        status_frame = tk.Frame(info_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(status_frame, text="Status:").pack(anchor=tk.W)
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(status_frame, textvariable=self.status_var, font=("Arial", 10), fg="blue").pack(anchor=tk.W)
        
        self.setup_chess_board()
        self.load_models()
        
    def setup_chess_board(self):
        self.canvas.delete("all")
        square_size = 80
        
        colors = ["#F0D9B5", "#B58863"]
        
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1, y1 = col * square_size, row * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
        for row in range(8):
            self.canvas.create_text(10, row * square_size + 40, text=str(8-row), font=("Arial", 12))
            
        for col in range(8):
            self.canvas.create_text(col * square_size + 40, 650, text=chr(ord('a') + col), font=("Arial", 12))
        
        self.draw_pieces()
        
    def draw_pieces(self):
        piece_symbols = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }
        
        self.canvas.delete("piece")
        
        board = self.game.get_board()
        square_size = 80
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    x = col * square_size + 40
                    y = row * square_size + 40
                    symbol = piece_symbols.get(piece, piece)
                    self.canvas.create_text(x, y, text=symbol, font=("Arial", 48), tags="piece")
    
    def load_models(self):
        models = [
            "openai/gpt-3.5-turbo",
            "meta-llama/llama-2-70b-chat",
            "anthropic/claude-3-haiku",
            "mistralai/mistral-7b-instruct",
            "google/gemma-7b-it"
        ]
        
        self.white_model_combo['values'] = models
        self.black_model_combo['values'] = models
        
        if models:
            self.white_model_var.set(models[0])
            self.black_model_var.set(models[1] if len(models) > 1 else models[0])
    
    def update_speed(self, event=None):
        self.move_delay = float(self.speed_var.get())
    
    def show_game_result(self, result):
        messagebox.showinfo("Game Over", f"🎯 Game Result:\n\n{result}", parent=self.root)
    
    def test_api(self):
        if not self.api_key_var.get():
            messagebox.showerror("Error", "Please enter your OpenRouter API key first")
            return
            
        self.client.set_api_key(self.api_key_var.get())
        self.log_message("Testing API connection...")
        
        threading.Thread(target=self._test_api_thread, daemon=True).start()
    
    def _test_api_thread(self):
        try:
            success, message = self.client.test_connection()
            if success:
                self.root.after(0, lambda: self.log_message("✅ API connection successful!"))
                self.root.after(0, lambda: messagebox.showinfo("Success", "API connection works!"))
            else:
                self.root.after(0, lambda: self.log_message(f"❌ API connection failed: {message}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"API connection failed:\n{message}"))
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ API test error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"API test failed:\n{str(e)}"))
    
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.api_key_var.set(config.get('api_key', ''))
                self.white_model_var.set(config.get('white_model', ''))
                self.black_model_var.set(config.get('black_model', ''))
                self.speed_var.set(str(config.get('move_delay', 2.0)))
                self.move_delay = config.get('move_delay', 2.0)
        except FileNotFoundError:
            pass
    
    def save_api_key(self):
        config = {
            'api_key': self.api_key_var.get(),
            'white_model': self.white_model_var.get(),
            'black_model': self.black_model_var.get(),
            'move_delay': self.move_delay
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f)
        
        self.client.set_api_key(self.api_key_var.get())
        messagebox.showinfo("Success", "Configuration saved!")
        
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        
    def start_game(self):
        if not self.api_key_var.get():
            messagebox.showerror("Error", "Please enter your OpenRouter API key")
            return
            
        if not self.white_model_var.get() or not self.black_model_var.get():
            messagebox.showerror("Error", "Please select models for both white and black")
            return
        
        self.game_running = True
        self.status_var.set("Game in progress...")
        self.log_message("=== Game Started ===")
        self.log_message(f"White: {self.white_model_var.get()}")
        self.log_message(f"Black: {self.black_model_var.get()}")
        
        self.client.set_api_key(self.api_key_var.get())
        
        threading.Thread(target=self.game_loop, daemon=True).start()
        
    def stop_game(self):
        self.game_running = False
        self.status_var.set("Game stopped")
        self.log_message("=== Game Stopped ===")
        
    def reset_board(self):
        self.stop_game()
        self.game.reset()
        self.setup_chess_board()
        self.log_message("=== Board Reset ===")
        self.status_var.set("Ready")
        
    def game_loop(self):
        move_count = 0
        
        while self.game_running and not self.game.is_game_over():
            try:
                current_player = "White" if self.game.current_turn == 'white' else "Black"
                model = self.white_model_var.get() if self.game.current_turn == 'white' else self.black_model_var.get()
                
                self.root.after(0, lambda: self.status_var.set(f"{current_player} ({model}) is thinking..."))
                
                board_state = self.game.get_fen()
                valid_moves = self.game.get_legal_moves()
                
                move = self.client.get_move(model, board_state, valid_moves, self.game.current_turn)
                
                if move and self.game.make_move(move):
                    move_count += 1
                    self.root.after(0, self.draw_pieces)
                    self.root.after(0, lambda: self.log_message(f"{move_count}. {current_player}: {move}"))
                    
                    if self.game.is_check():
                        self.root.after(0, lambda: self.log_message("Check!"))
                        
                    if self.game.is_game_over():
                        result = self.game.get_game_result()
                        self.root.after(0, lambda: self.log_message(f"Game Over: {result}"))
                        self.root.after(0, lambda: self.status_var.set(f"Game Over: {result}"))
                        self.root.after(0, lambda: self.show_game_result(result))
                        break
                        
                    time.sleep(self.move_delay)
                        
                else:
                    self.root.after(0, lambda move=move: self.log_message(f"{current_player} failed to make valid move: {move}"))
                    
                    
                    if valid_moves:
                        import random
                        fallback_move = random.choice(valid_moves)
                        if self.game.make_move(fallback_move):
                            move_count += 1
                            self.root.after(0, self.draw_pieces)
                            self.root.after(0, lambda: self.log_message(f"{move_count}. {current_player}: {fallback_move} (fallback)"))
                            time.sleep(self.move_delay)
                        else:
                            self.root.after(0, lambda: self.log_message(f"Game stopped - no valid moves available"))
                            break
                    else:
                        self.root.after(0, lambda: self.log_message(f"Game stopped - no legal moves available"))
                        break
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Error: {str(e)}"))
                break
                
        self.game_running = False
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChessArenaApp()
    app.run()
