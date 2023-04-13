# Auto-GPT Task Planner
A planner for Auto-GPT that uses GPT-4 to create a detailed set of atomic steps that Auto-GPT can follow in order to increase its speed and efficiency. Furthermore, this can prevent Auto-GPT from getting stuck in loops and work towards the final objective with a more concrete plan for both the AI and the end user.
Auto-GPT is quite good at simple tasks but struggles with larger tasks. This paradigm aims to rectify this by allowing the Auto-GPT instances to direct all of their attention and focus to simple, atomic tasks.

## planner.py
The code for planning the tasks, returning the plan for Auto-GPT to follow in JSON format.

## lana.py
A very simple and hacky logger I bodged together in like an hour.

## output_sample.log
An incomplete extract of the output from the planner.py file to the console.

## task_planner_prompt.txt
Just realising now that I forgot to add this to the repo before I left, I will add it when I get home tonight. Sorry 🙃

# Version
The current state of this repository is simply a code dump of the code I've been using to prototype the idea. A forked repository contributing to the Auto-GPT should follow shortly.

# Plan
I have the following goals for the planner to achieve
 - Give Auto-GPT an object oriented overhaul to allow multiple instances / AIs to run within one program more easily (this could also help with Auto-GPT instances that could benefit from working in parallel with other instances).
 - Allow an Auto-GPT instance to run for each atomic subtask in sequence, making that subtask its primary goal.
 - Add each Auto-GPT instance's final output to the input of the next instance
