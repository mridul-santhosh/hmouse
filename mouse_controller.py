import pyautogui
import numpy as np
import time

class MouseController:
    def __init__(self, screen_width=None, screen_height=None, smoothing_factor=0.3):
        # Disable pyautogui fail-safe
        pyautogui.FAILSAFE = False
        
        # Get screen size if not provided
        if screen_width is None or screen_height is None:
            screen_width, screen_height = pyautogui.size()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Movement parameters
        self.smoothing_factor = smoothing_factor
        self.last_x = screen_width // 2
        self.last_y = screen_height // 2
        
        # State tracking
        self.is_dragging = False
        self.eyes_closed_start = None
        self.eyes_closed_threshold = 1.0  # seconds
        
        # Head movement scaling
        self.x_scale = 150  # Adjust these values to control sensitivity
        self.y_scale = 150
        
    def update_mouse_position(self, head_x, head_y):
        # Convert head rotation to screen coordinates
        # Adjust the scaling and offset to make movements more natural
        target_x = self.screen_width // 2 + (head_x * self.x_scale)
        target_y = self.screen_height // 2 + (head_y * self.y_scale)
        
        # Apply smoothing
        new_x = int(self.last_x + (target_x - self.last_x) * self.smoothing_factor)
        new_y = int(self.last_y + (target_y - self.last_y) * self.smoothing_factor)
        
        # Clamp to screen boundaries
        new_x = max(0, min(new_x, self.screen_width))
        new_y = max(0, min(new_y, self.screen_height))
        
        # Move mouse
        pyautogui.moveTo(new_x, new_y)
        
        # Update last position
        self.last_x = new_x
        self.last_y = new_y
        
    def handle_mouth_state(self, mouth_state):
        if mouth_state == "opened" and not self.is_dragging:
            pyautogui.mouseDown()
            self.is_dragging = True
        elif mouth_state == "closed" and self.is_dragging:
            pyautogui.mouseUp()
            self.is_dragging = False
            
    def handle_eyes_state(self, right_eye_state, left_eye_state):
        current_time = time.time()
        
        # Check if both eyes are closed
        if right_eye_state == "closed" and left_eye_state == "closed":
            if self.eyes_closed_start is None:
                self.eyes_closed_start = current_time
            elif current_time - self.eyes_closed_start >= self.eyes_closed_threshold:
                pyautogui.rightClick()
                self.eyes_closed_start = None  # Reset timer
        else:
            self.eyes_closed_start = None