import os
import random
from story_parser import read_story_file, Story
from get_actions_plan import get_actions_plan


def get_selection(options = ["Nothing"]):
    """Gets a selection from the user.

    Args:
        options: A list of strings, each string being an option.

    Returns:
        The index of the selected option.
    """
    
    next_action_prompts = [
        "What would you like to do next?",
        "What is your next steps?",
        "What are you planning to do next?",
        "What would you like to explore next?",
        "What would you like to achieve next?",
        "What would you like to do to move forward?",
        "What would you like to accomplish next?",
    ]
    prompt = next_action_prompts[random.randrange(0, len(next_action_prompts))]
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}: {option}")

    selection = int(input("Enter your selection: "))
    return selection - 1



def execute_story(json_path):
    """Executes a story interactivelly.

    Args:
    json_path: The path to the story file

    """

    story = read_story_file(json_path)
    domain_str = story.genPDDLDomain()

    save_path = os.path.dirname(json_path)
    story.write_domain_file(domain_str = domain_str, path = save_path)

    story_finished = False
    next_possible_bot_actions = None
    while not story_finished:
        problem_strs = story.genPDDLProblems(next_actions=next_possible_bot_actions)

        for problem_str in problem_strs:
            story.write_problem_file(problem_str,save_path)
            action_names = get_actions_plan(save_path)
            if len(action_names) != 0:
                story_finished = False
                break
            else:
                story_finished = True
        
        if story_finished: break
        
        bot_action = story.actions[action_names[0]["action"]]
        next_possible_user_actions = story.execute_action(bot_action.name)
        
        print(bot_action.text)
        print()
        if len(next_possible_user_actions) == 0: break

        next_action_index = get_selection([act.pretext for act in next_possible_user_actions])
        user_action = next_possible_user_actions[next_action_index]
        next_possible_bot_actions = story.execute_action(user_action.name)

        print(user_action.text)
        if len(next_possible_bot_actions) == 0: break
        

execute_story("/home/pas/Documents/University/eai/patrizi/InteractiveStorytelling/PDDLs/test1/test1.json")