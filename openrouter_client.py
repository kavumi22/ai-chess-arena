import requests
import json
import re
import time

class OpenRouterClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai"
        self.session = requests.Session()
        
    def set_api_key(self, api_key):
        self.api_key = api_key
        
    def get_move(self, model, board_fen, legal_moves, current_player):
        if not self.api_key:
            raise ValueError("API key not set")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ai-chess-arena",
            "X-Title": "AI Chess Arena"
        }
        
        prompt = self.create_chess_prompt(board_fen, legal_moves, current_player)
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a chess engine. You must respond with ONLY a valid chess move in UCI notation. Examples: e2e4, g1f3, d7d5, a7a8q. Respond with exactly 4 or 5 characters, nothing else."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 20,
            "temperature": 0.3,
            "stop": ["\n", " ", "."]
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"API Response Status: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            print(f"API Response: {result}")
            
            if 'choices' in result and len(result['choices']) > 0:
                move_text = result['choices'][0]['message']['content'].strip()
                print(f"AI Response Text: '{move_text}'")
                move = self.extract_move_from_response(move_text, legal_moves)
                print(f"Parsed Move: {move}")
                return move
            else:
                print(f"No choices in response: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Full API Error: {e}")
            print(f"Response status: {getattr(response, 'status_code', 'No response')}")
            print(f"Response text: {getattr(response, 'text', 'No response text')}")
            if "404" in str(e):
                print(f"API endpoint not found. Please check your OpenRouter API key and model name.")
            elif "401" in str(e):
                print(f"Unauthorized. Please check your API key.")
            elif "403" in str(e):
                print(f"Forbidden. Your API key may not have access to this model.")
            else:
                print(f"API request failed: {e}")
            return self.get_random_legal_move(legal_moves)
        except Exception as e:
            print(f"Error parsing response: {e}")
            return self.get_random_legal_move(legal_moves)
            
    def create_chess_prompt(self, board_fen, legal_moves, current_player):
        prompt = f"""Position: {board_fen}
Player: {current_player}

Valid moves: {', '.join(legal_moves[:15])}

Pick ONE move from the valid moves list above. Reply with exactly 4-5 characters only:"""
        
        return prompt
        
    def extract_move_from_response(self, response_text, legal_moves):
        print(f"Extracting move from: '{response_text}'")
        print(f"Available legal moves: {legal_moves[:10]}...")  # Show first 10 moves
        
        response_text = response_text.lower().strip()
        
        move_patterns = [
            r'\b([a-h][1-8][a-h][1-8][qrbn]?)\b',
            r'\b([a-h]\d[a-h]\d[qrbn]?)\b'
        ]
        
        for pattern in move_patterns:
            matches = re.findall(pattern, response_text)
            print(f"Pattern {pattern} found: {matches}")
            for match in matches:
                if match in legal_moves:
                    print(f"Valid move found: {match}")
                    return match
                    
        words = response_text.split()
        for word in words:
            clean_word = re.sub(r'[^a-h0-9]', '', word)
            if clean_word in legal_moves:
                print(f"Valid word move found: {clean_word}")
                return clean_word
                
        for move in legal_moves:
            if move in response_text:
                print(f"Direct match found: {move}")
                return move
        
        print(f"No valid move found in response: '{response_text}'")        
        return None
        
    def get_random_legal_move(self, legal_moves):
        if legal_moves:
            import random
            return random.choice(legal_moves)
        return None
        
    def test_connection(self):
        if not self.api_key:
            return False, "API key not set"
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Connection successful"
            else:
                return False, f"HTTP {response.status_code}: {response.text}"
                
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
            
    def get_available_models(self):
        if not self.api_key:
            return []
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                models_data = response.json()
                free_models = []
                
                for model in models_data.get('data', []):
                    if model.get('pricing', {}).get('prompt', 0) == 0:
                        free_models.append(model['id'])
                        
                return free_models
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
