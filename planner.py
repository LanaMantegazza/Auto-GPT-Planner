import json
from memory import get_memory
import data
import chat
from lana import LANA
from config import Config

# A planner for Auto-GPT that uses GPT-4 to create a detailed set of atomic steps that Auto-GPT can follow

lana = LANA()
cfg = Config()

def create_ai_prompt(ai_name, ai_role, ai_goals, prompt):
    prompt_start = """Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications."""

    # Construct full prompt
    full_prompt = f"You are {ai_name}, {ai_role}\n{prompt_start}\n\nGOALS:\n\n"
    for i, goal in enumerate(ai_goals):
        full_prompt += f"{i+1}. {goal}\n"

    full_prompt += f"\n\n{prompt}"
    return full_prompt

def plan_task(task):
    global cfg
    lana.log_action_begin(f"Planning task: {task}")

    task_planner_prompt = create_ai_prompt(
            "The Task Splitter AI", 
            "An AI that splits a task into several simpler subtasks, evaluating whether each subtask could be considered atomic, meaning the tasks could be reasonably achieved by an average person.", 
            [
                f"Write a set of simple subtasks that could be run in sequence by a person to accomplish the task '{task}'. Do not attempt to execute the task, your job is only to split the task into subtasks.",
                "Evaluate whether the set of subtasks would fulfill the task objective when each subtask is run in sequence.",
                "Alter list of subtasks such that the set of subtasks fulfill the task objective when run in sequence."
            ], 
            data.load_prompt('task_planner_prompt.txt')
        )
    
    memory = get_memory(cfg, init=True)

    subtasks_json = None
    invalid_json = True
    while invalid_json:
        lana.log_action_single("Asking Task Splitter AI to plan task...")
        assistant_reply = chat.chat_with_ai(
            task_planner_prompt,
            "Complete the goals of The Task Splitter AI, and respond using the format specified above:",
            [],
            memory,
            cfg.fast_token_limit, cfg.debug)
        
        try:
            subtasks_json = json.loads(assistant_reply)
            lana.log_json("AI returned the following subtasks", subtasks_json)
            invalid_json = False
        except json.decoder.JSONDecodeError:
            lana.log_warning('The Task Splitter AI did not return valid JSON. Trying again...')

    lana.log_action_begin("Evaluating subtasks...")
    for subtask in subtasks_json['tasks']:
        if not subtask['is_atomic']:
            subtask_steps = plan_task(subtask['task_name'] + ': ' + subtask['task_description'])
            subtask['tasks'] = subtask_steps
    
    lana.log_action_end("Completed evaluating subtasks")
    lana.log_json("Task can be completed with the following subtasks", subtasks_json)
    lana.log_action_end("Completed planning task")
    return subtasks_json

lana.log_json("Plan to book a flight from London to New York", plan_task("Book a flight from London to New York"))