import ipywidgets as widgets
from IPython.display import display
from ipywidgets import VBox, HBox
import json

# Create input fields for Participant and Experimenter
participant_input = widgets.Text(
    value='',
    placeholder='Enter participant ID',
    description='Participant:',
    layout=widgets.Layout(width='250px')  # Wider input for Participant
)

experimenter_input = widgets.Text(
    value='',
    placeholder="Enter scientist's name",
    description='Scientist:',
    layout=widgets.Layout(width='250px')  # Wider input for Experimenter
)

# Number of phases input
phases_input = widgets.IntText(
    value=1,
    description='Phases:',
    layout=widgets.Layout(width='140px')  # Wider label for Number of Phases
)

# Layout adjustments
label_layout = widgets.Layout(width='155px')  # Wider labels for longer descriptions
input_box_layout = widgets.Layout(width='90px')  # Halved input box width

# Function to create a horizontal separator
def horizontal_separator():
    return widgets.HTML(value='<hr style="border: 1px solid gray; margin: 10px 0;">')

# Function to dynamically create widgets for each phase
def create_phase_widgets(phase_num):
    duration_widget = HBox([
        widgets.Label(value=f'Duration (Phase {phase_num}):', layout=widgets.Layout(width='155px')),
        widgets.IntText(value=30, layout=input_box_layout)
    ])
    
    number_balls_widget = HBox([
        widgets.Label(value=f'Number of Balls (Phase {phase_num}):', layout=widgets.Layout(width='155px')),
        widgets.IntText(value=3, layout=input_box_layout)
    ])

    # Dynamically adjust the number of ball settings
    def update_ball_settings(change):
        num_balls = number_balls_widget.children[1].value
        
        speed_widgets.children = [
            HBox([
                widgets.Label(value=f'Speed (Ball {i + 1}):', layout=label_layout),
                widgets.FloatText(value=1.0, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        radii_widgets.children = [
            HBox([
                widgets.Label(value=f'Radius (Ball {i + 1}):', layout=label_layout),
                widgets.FloatText(value=60, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        
        points_per_reinforcement.children = [
            HBox([
                widgets.Label(value=f'Points (Ball {i + 1}):', layout=label_layout),
                widgets.IntText(value=1, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        change_to_clicks_widgets.children = [
            HBox([
                widgets.Label(value=f'Change To Clicks (Ball {i + 1}):', layout=label_layout),
                widgets.IntText(value=1, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        change_over_delay_widgets.children = [
            HBox([
                widgets.Label(value=f'Change Over Delay (Ball {i + 1}):', layout=label_layout),
                widgets.FloatText(value=5, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        
        # Color Pickers for each ball
        base_colors_widgets.children = [
            HBox([
                widgets.Label(value=f'Base Color (Ball {i + 1}):', layout=label_layout),
                widgets.ColorPicker(value="#ff0000", layout=input_box_layout)
            ]) for i in range(num_balls)
        ]

    number_balls_widget.children[1].observe(update_ball_settings, names='value')

    # Containers for the ball-specific widgets
    speed_widgets = HBox([])
    radii_widgets = HBox([])
    points_per_reinforcement = HBox([])
    change_to_clicks_widgets = HBox([])
    change_over_delay_widgets = HBox([])
    base_colors_widgets = HBox([])

    # Initial update for ball-specific widgets
    update_ball_settings(None)

    # Yoked dropdown
    yoked_widget = HBox([
        widgets.Label(value=f'Yoked (Phase {phase_num}):', layout=widgets.Layout(width='155px')),
        widgets.Dropdown(options=[('False', False), ('True', True)], value=False, layout=input_box_layout)
    ])

    # Debug dropdown
    debug_widget = HBox([
        widgets.Label(value=f'Debug (Phase {phase_num}):', layout=widgets.Layout(width='155px')),
        widgets.Dropdown(options=[('False', False), ('True', True)], value=False, layout=input_box_layout)
    ])

    # Assemble phase-specific widgets
    phase_box = VBox([
        duration_widget, 
        number_balls_widget,
        speed_widgets, 
        radii_widgets,
        base_colors_widgets,
        points_per_reinforcement, 
        change_to_clicks_widgets, 
        change_over_delay_widgets,
        yoked_widget,  # Add the Yoked dropdown
        debug_widget,  # Add the Debug dropdown
        horizontal_separator()  # Add horizontal separator after each phase
    ])

    return phase_box

# Function to update phase widgets dynamically
def update_phases(change):
    num_phases = phases_input.value
    phase_boxes.children = [create_phase_widgets(i + 1) for i in range(num_phases)]

# Save settings to a JSON file
def save_settings(button):
    settings = {
        'phases': phases_input.value,
        'phase_data': []
    }

    for phase_num in range(phases_input.value):
        phase_info = {
            'duration': phase_boxes.children[phase_num].children[0].children[1].value,
            'number_of_balls': phase_boxes.children[phase_num].children[1].children[1].value,
            'yoked': phase_boxes.children[phase_num].children[-3].children[1].value,
            'debug': phase_boxes.children[phase_num].children[-2].children[1].value,
            'balls': []
        }
        
        for ball_num in range(phase_info['number_of_balls']):
            ball_info = {
                'speed': phase_boxes.children[phase_num].children[2].children[ball_num].children[1].value,
                'radius': phase_boxes.children[phase_num].children[3].children[ball_num].children[1].value,
                'points_per_reinforcement': phase_boxes.children[phase_num].children[5].children[ball_num].children[1].value,
                'change_to_clicks': phase_boxes.children[phase_num].children[6].children[ball_num].children[1].value,
                'change_over_delay': phase_boxes.children[phase_num].children[7].children[ball_num].children[1].value,
                'base_color': phase_boxes.children[phase_num].children[4].children[ball_num].children[1].value  # Base color picker
            }
            phase_info['balls'].append(ball_info)
        
        settings['phase_data'].append(phase_info)

    with open('settings.json', 'w') as f:
        json.dump(settings, f)

# Load settings from a JSON file
def load_settings(button):
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        
        phases_input.value = settings['phases']
        
        # Update phase boxes based on loaded data
        phase_boxes.children = []
        for phase in settings['phase_data']:
            phase_widget = create_phase_widgets(len(phase_boxes.children) + 1)
            phase_widget.children[0].children[1].value = phase['duration']
            phase_widget.children[1].children[1].value = phase['number_of_balls']
            phase_widget.children[-3].children[1].value = phase['yoked']
            phase_widget.children[-2].children[1].value = phase['debug']
            
            for ball_num in range(phase['number_of_balls']):
                phase_widget.children[2].children[ball_num].children[1].value = phase['balls'][ball_num]['speed']
                phase_widget.children[3].children[ball_num].children[1].value = phase['balls'][ball_num]['radius']
                phase_widget.children[5].children[ball_num].children[1].value = phase['balls'][ball_num]['points_per_reinforcement']
                phase_widget.children[6].children[ball_num].children[1].value = phase['balls'][ball_num]['change_to_clicks']
                phase_widget.children[7].children[ball_num].children[1].value = phase['balls'][ball_num]['change_over_delay']
                phase_widget.children[4].children[ball_num].children[1].value = phase['balls'][ball_num]['base_color']
            
            phase_boxes.children += (phase_widget,)

    except FileNotFoundError:
        print("No settings file found. Please save settings first.")

# Main interface
phase_boxes = VBox([create_phase_widgets(1)])  # Start with one phase
phases_input.observe(update_phases, names='value')

# Save and Load Buttons
save_button = widgets.Button(description="Save Settings")
save_button.on_click(save_settings)

load_button = widgets.Button(description="Open Settings")
load_button.on_click(load_settings)

# Display everything
display(VBox([
    participant_input,
    experimenter_input,
    phases_input,
    horizontal_separator(),
    phase_boxes,
    HBox([save_button, load_button])  # Buttons in a horizontal box
]))
