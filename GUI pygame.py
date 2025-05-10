import pygame
import sys
from pygame.locals import *

# Configuration
WIDTH, HEIGHT = 1400, 800
BACKGROUND_COLOR = (245, 245, 220)
ANIMATION_SPEED = 5
FRAME_RATE = 60

COLORS = {
    'chef': (255, 165, 0),
    'tool': (70, 130, 180),
    'ingredient': (34, 139, 34),
    'location': (210, 180, 140),
    'dirty': (139, 69, 19),
    'chopped': (0, 100, 0),
    'cooked': (178, 34, 34)
}

LOCATIONS = {
    'storage': (100, 300),
    'counter': (400, 200),
    'stove': (700, 300),
    'sink': (400, 500),
    'table': (850, 500)
}

class KitchenSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cucina Nintendo")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Game state
        self.chef_pos = LOCATIONS['table']
        self.target_pos = self.chef_pos
        self.chef_location = 'table'
        self.running = False
        self.speed = 1.0
        self.current_step = 0
        self.auto_mode = False
        self.last_step_time = 0
        self.step_delay = 1500  # milliseconds between steps
        
        # Object states
        self.tool_states = {
            'knife': {'location': 'counter', 'dirty': False},
            'pan': {'location': 'stove', 'dirty': False}
        }
        
        self.ingredient_states = {
            'chicken': {'location': 'storage', 'chopped': False, 'cooked': False},
            'salmon': {'location': 'storage', 'chopped': False, 'cooked': False},
            'tuna': {'location': 'storage', 'chopped': False, 'cooked': False},
            'rice': {'location': 'storage', 'chopped': False, 'cooked': False},
            'beans': {'location': 'storage', 'chopped': False, 'cooked': False},
            'avocado': {'location': 'storage', 'chopped': False, 'cooked': False},
            'carrot': {'location': 'storage', 'chopped': False, 'cooked': False},
            'feta': {'location': 'storage', 'chopped': False, 'cooked': False}
        }
        
        self.state_panel = {
            'held_tool': None,
            'held_ingredient': None,
            'served': []
        }
        
        # Execution plan
        self.plan = []
        self.load_pddl_plan('plan.txt')  # Load from file or use default
        self.animation_queue = []

    def load_pddl_plan(self, plan_file_path):
        """Load and parse PDDL planner output"""
        action_mapping = {
            'move': 'move',
            'take_tool': 'take_tool',
            'put_down_tool': 'put_down_tool',
            'take_ingredient': 'take_ingredient',
            'chop': 'chop',
            'cook': 'cook',
            'wash': 'wash',
            'serve_plate': 'serve_plate'
        }

        try:
            with open(plan_file_path, 'r') as f:
                for line in f:
                    line = line.strip().lower()
                    if line.startswith('('):
                        action_str = line[1:-1].split()
                        action_name = action_str[0]
                        if action_name in action_mapping:
                            sim_action = (action_mapping[action_name],) + tuple(action_str[1:])
                            self.plan.append(sim_action)
            print(f"Loaded {len(self.plan)} actions from {plan_file_path}")
        except:
            print("Using default plan")
            self.plan = [
            ("move" "table" "storage"),    
            ("take_ingredient", "tuna", "storage"),
            ("move", "storage", "stove"),
            ("take_tool", "pan", "stove"),
            ("move", "stove", "sink"),
            ("put_down_tool", "pan", "sink"),
            ("move", "sink", "counter"),
            ("take_tool", "knife", "counter"),
            ("chop", "tuna"),
            ("move", "counter", "sink"),
            ("wash", "knife"),
            ("put_down_tool", "knife", "sink"),
            ("take_tool", "pan", "sink"),
            ("move", "sink", "stove"),
            ("cook", "tuna"),
            ("move", "stove", "table"),
            ("serve_plate", "tuna"),
            ]
    
    def draw_kitchen(self):
        # Draw kitchen areas
        for loc, pos in LOCATIONS.items():
            pygame.draw.rect(self.screen, COLORS['location'], (pos[0], pos[1], 200, 150))
            text = self.font.render(loc.capitalize(), True, (0, 0, 0))
            self.screen.blit(text, (pos[0]+10, pos[1]+10))
        
        # Draw tools
        for tool, state in self.tool_states.items():
            if state['location'] in LOCATIONS:
                pos = LOCATIONS[state['location']]
                color = COLORS['dirty'] if state['dirty'] else COLORS['tool']
                pygame.draw.circle(self.screen, color, (pos[0]+50, pos[1]+100), 15)

    def draw_chef(self):
        pygame.draw.circle(self.screen, COLORS['chef'], self.chef_pos, 20)
        # Draw held items
        if self.state_panel['held_tool']:
            tool_color = COLORS['dirty'] if self.tool_states[self.state_panel['held_tool']]['dirty'] else COLORS['tool']
            pygame.draw.circle(self.screen, tool_color, (self.chef_pos[0]+25, self.chef_pos[1]-15), 10)
        if self.state_panel['held_ingredient']:
            ing = self.state_panel['held_ingredient']
            color = COLORS['ingredient']
            if self.ingredient_states[ing]['chopped']: color = COLORS['chopped']
            if self.ingredient_states[ing]['cooked']: color = COLORS['cooked']
            pygame.draw.circle(self.screen, color, (self.chef_pos[0]-25, self.chef_pos[1]-15), 10)

    def draw_ingredients(self):
        y = 475
        for ing, state in self.ingredient_states.items():
            color = COLORS['ingredient']
            if state['chopped']: color = COLORS['chopped']
            if state['cooked']: color = COLORS['cooked']
            
            pygame.draw.rect(self.screen, color, (50, y, 200, 30))
            text = self.font.render(f"{ing} ({state['location']})", True, (0, 0, 0))
            self.screen.blit(text, (60, y+5))
            y += 40

    def draw_state_panel(self):
        panel = [
            f"Chef Location: {self.chef_location}",
            f"Held Tool: {self.state_panel['held_tool']}",
            f"Held Ingredient: {self.state_panel['held_ingredient']}",
            f"Served: {', '.join(self.state_panel['served'])}",
            f"Dirty Tools: {', '.join([t for t, s in self.tool_states.items() if s['dirty']])}"
        ]
        
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 20, 350, 150))
        for i, line in enumerate(panel):
            text = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(text, (30, 30 + i*30))

    def draw_controls(self):
        controls = [
            "SPACE: AutoPlay",
            "→: Next Step",
            "←: Previous Step",
            "+/-: Adjust Speed",
            "Close Window: Exit GUI"
        ]
        
        for i, control in enumerate(controls):
            text = self.font.render(control, True, (0, 0, 0))
            self.screen.blit(text, (WIDTH-200, 20 + i*25))

    def animate_movement(self):
        if self.chef_pos != self.target_pos:
            dx = self.target_pos[0] - self.chef_pos[0]
            dy = self.target_pos[1] - self.chef_pos[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance > ANIMATION_SPEED:
                step_x = dx/distance * ANIMATION_SPEED * self.speed
                step_y = dy/distance * ANIMATION_SPEED * self.speed
                self.chef_pos = (self.chef_pos[0]+step_x, self.chef_pos[1]+step_y)
            else:
                self.chef_pos = self.target_pos


    def is_animating(self):
        """Check if any animations are in progress"""
        return self.chef_pos != self.target_pos

    def execute_action(self, action):
        action_type = action[0]
        
        if action_type == "move":
            _, from_loc, to_loc = action
            self.chef_location = to_loc
            self.target_pos = LOCATIONS[to_loc]
        
        elif action_type == "take_tool":
            _, tool, location = action
            if self.tool_states[tool]['location'] == location:
                self.state_panel['held_tool'] = tool
                self.tool_states[tool]['location'] = 'chef'

        elif action_type == "put_down_tool":
            _, tool, location = action
            if self.state_panel['held_tool'] == tool and self.chef_location == location:
                self.state_panel['held_tool'] = None
                self.tool_states[tool]['location'] = location        

        elif action_type == "take_ingredient":
            _, ingredient, location = action
            if self.ingredient_states[ingredient]['location'] == location:
                self.state_panel['held_ingredient'] = ingredient
                self.ingredient_states[ingredient]['location'] = 'chef'    
        
        elif action_type == "chop":
            _, ingredient = action
            if self.state_panel['held_tool'] == "knife":
                self.ingredient_states[ingredient]['chopped'] = True
                self.tool_states['knife']['dirty'] = True
                self.state_panel['held_ingredient'] = ingredient
        
        elif action_type == "cook":
            _, ingredient = action
            if self.state_panel['held_tool'] == "pan":
                self.ingredient_states[ingredient]['cooked'] = True
                self.tool_states['pan']['dirty'] = True

        elif action_type == "wash":
            _, tool = action
            if self.state_panel['held_tool'] == tool:
                self.tool_states[tool]['dirty'] = False       
        
        elif action_type == "serve_plate":
            _, ingredient = action
            if self.ingredient_states[ingredient]['cooked']:
                self.state_panel['served'].append(ingredient)
                self.state_panel['held_ingredient'] = None
    
    def run(self):
        self.running = True
        while self.running:
            current_time = pygame.time.get_ticks()

            # Automatic execution logic
            if self.auto_mode and not self.is_animating():
                if current_time - self.last_step_time > self.step_delay / self.speed:
                    if self.current_step < len(self.plan) - 1:
                        self.current_step += 1
                        self.execute_action(self.plan[self.current_step])
                        self.last_step_time = current_time
                    else:
                        self.auto_mode = False

            # Event handling (FIXED VERSION)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:  # Changed to elif
                    if event.key == K_SPACE:
                        self.auto_mode = not self.auto_mode
                        if self.auto_mode:
                            self.last_step_time = current_time
                    elif event.key == K_RIGHT and not self.auto_mode:
                        if self.current_step < len(self.plan)-1:
                            self.current_step += 1
                            self.execute_action(self.plan[self.current_step])
                    elif event.key == K_LEFT and not self.auto_mode:
                        if self.current_step > 0:
                            self.current_step -= 1
                    elif event.key in (K_PLUS, K_KP_PLUS):
                        self.speed = min(2.0, self.speed + 0.1)
                    elif event.key in (K_MINUS, K_KP_MINUS):
                        self.speed = max(0.5, self.speed - 0.1)

                    # Rendering
            self.screen.fill(BACKGROUND_COLOR)
            if self.running:
                self.animate_movement()

            try:
                self.draw_kitchen()
                self.draw_chef()
                self.draw_ingredients()
                self.draw_state_panel()
                self.draw_controls()
            except Exception as e:
                print(f"Drawing error: {str(e)}")
                self.running = False

            pygame.display.flip()
            self.clock.tick(FRAME_RATE)

        pygame.quit()
        sys.exit()

    
if __name__ == "__main__":
    simulator = KitchenSimulator()
    simulator.run()

