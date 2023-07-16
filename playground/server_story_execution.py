import os, sys, uuid, tempfile
from StoryTelling.story_parser import read_story_file, Story
from StoryTelling.get_actions_plan import get_actions_plan
from RAIM.ipc_client import IPCClient
from RAIM.raim_command import Command

import argparse

# action = {"action_type":str, "action_properties":{}, "is_successful":bool}

class StoryTellingServer:
    def __init__(self, ipc_server_host, ipc_server_port, stories_folder, debug = False, **kwargs) -> None:
        self.ipc = IPCClient("story_telling")
        self.stories_folder = stories_folder
        self.stories_in_execution = {}
        self.ipc.debug = debug
        
        self.ipc.set_command_listener(self.request_listener)
        self.ipc.connect(host=ipc_server_host, port=ipc_server_port)

    def shutdown(self):
        print("Shutting down the server...")
        self.ipc.disconnect()
    
    def send_response(self, command_in, action  = None, is_successful = False):
        if command_in.request:
            command_out = command_in.gen_response(is_successful = is_successful, data=action)
        else:
            command_out = Command(
                data=action,
                to_client_id=command_in.from_client_id
            )
        self.ipc.dispatch_command(command_out)

    def request_listener(self, command: Command):
        if "actions" in command.data:
            action = command.data["actions"][0]
            action_type = action["action_type"]
            action_properties = None if "action_properties" not in action else action["action_properties"]

            if action_type == "quit":
                self.shutdown()

            if action_type == "story_list":
                response_action, is_successful = self.list_stories()
                self.send_response(command_in=command, action=response_action, is_successful=is_successful)

            if action_type == "story_start":
                story_name = action_properties["story_name"]
                story_lang = action_properties["story_language"]
                response_action, is_successful = self.start_story(story_name, story_lang)
                self.send_response(command_in=command, action=response_action, is_successful=is_successful)

            if action_type == "story_until_now":
                story_id = action_properties["story_id"]
                response_action, is_successful = self.get_story_response(story_id)
                self.send_response(command_in=command, action=response_action, is_successful=is_successful)

            if action_type == "story_execute_action":
                story_id = action_properties["story_id"]
                story_action_index = action_properties["story_action_index"]
                response_action, is_successful = self.execute_user_action(story_id,story_action_index)
                self.send_response(command_in=command, action=response_action, is_successful=is_successful)
    
    def create_action_properties(self, story_id):
        if story_id not in self.stories_in_execution:
            return {}

        story = self.stories_in_execution[story_id]["story"]
        save_path = self.stories_in_execution[story_id]["save_path"]
        next_user_actions = self.stories_in_execution[story_id]["next_user_actions"]
        next_bot_actions = self.stories_in_execution[story_id]["next_bot_actions"]
        story_finished = self.stories_in_execution[story_id]["story_finished"]

        return {
            "story_id": story_id,
            "story_finished": story_finished,
            "prompts": [act.text for act in story.actions_history],
            "moods": [act.mood for act in story.actions_history],
            "possible_user_actions": [act.pretext for act in next_user_actions]
        }
    
    def list_stories(self):
        stories = [
            folder for folder in os.listdir(self.stories_folder)
            if os.path.isdir(os.path.join(self.stories_folder, folder))
            and os.path.exists(os.path.join(self.stories_folder, folder, "story.json"))
        ]
        is_successful = True if len(stories)>0 else False
        action = {"action_type":"story_list", "action_properties":{"stories": stories}, "is_successful":is_successful}
        return action, is_successful
    
    def execute_bot_action(self, story_id):
        story = self.stories_in_execution[story_id]["story"]
        save_path = self.stories_in_execution[story_id]["save_path"]
        next_user_actions = self.stories_in_execution[story_id]["next_user_actions"]
        next_bot_actions = self.stories_in_execution[story_id]["next_bot_actions"]
        story_finished = self.stories_in_execution[story_id]["story_finished"]

        # Requesting bot action execution, but no bot actions are available, probably the story is finished
        if len(next_bot_actions) == 0:
            self.stories_in_execution[story_id]["story_finished"] = False
            return False # Didn't execute any bot actions on this story

        problem_strs = story.genPDDLProblems(next_actions=next_bot_actions)

        for problem_str in problem_strs:
            story.write_problem_file(problem_str,save_path)
            action_names = get_actions_plan(save_path)
            if len(action_names) != 0:
                story_finished = False
                break
            else:
                story_finished = True
        
        if story_finished:
            self.stories_in_execution[story_id]["story_finished"] = True
            return False # Didn't execute any bot actions on this story
        
        bot_action = story.actions[action_names[0]["action"]] # The next action in the plan
        next_possible_user_actions = story.execute_action(bot_action.name)
        self.stories_in_execution[story_id]["next_user_actions"] = next_possible_user_actions
        
        if len(next_possible_user_actions) == 0:
            self.stories_in_execution[story_id]["story_finished"] = True
            return True # Did execute a bot action on this story

        return True # Did execute a bot action on this story

    def execute_user_action(self, story_id, story_action_index):
        story = self.stories_in_execution[story_id]["story"]
        save_path = self.stories_in_execution[story_id]["save_path"]
        next_user_actions = self.stories_in_execution[story_id]["next_user_actions"]
        next_bot_actions = self.stories_in_execution[story_id]["next_bot_actions"]
        story_finished = self.stories_in_execution[story_id]["story_finished"]

        # Requesting user action execution, but no user actions are available, probably the story is finished
        if len(next_user_actions) == 0:
            self.stories_in_execution[story_id]["story_finished"] = True
            return {"action_type":"story_execute_action", "action_properties":self.create_action_properties(story_id), "is_successful":False}, False

        user_action = next_user_actions[story_action_index]
        next_possible_bot_actions = story.execute_action(user_action.name)
        self.stories_in_execution[story_id]["next_bot_actions"] = next_possible_bot_actions

        if len(next_possible_bot_actions) == 0:
            self.stories_in_execution[story_id]["story_finished"] = True
            return {"action_type":"story_execute_action", "action_properties":self.create_action_properties(story_id), "is_successful":True}, True

        bot_execution_result = self.execute_bot_action(story_id)
        return {"action_type":"story_execute_action", "action_properties":self.create_action_properties(story_id), "is_successful":True}, True
            

    def start_story(self,story_name,lang = "EN"):
        action = {"action_type":"start_story", "action_properties":{}, "is_successful":False}
        if not os.path.exists(os.path.join(self.stories_folder, story_name, "story.json")):
            return action, False
        story_id = str(uuid.uuid4())
        json_path = os.path.join(self.stories_folder, story_name, "story.json")
        story = read_story_file(json_path, lang)
        domain_str = story.genPDDLDomain()

        save_path = tempfile.mkdtemp()
        story.write_domain_file(domain_str = domain_str, path = save_path)

        self.stories_in_execution[story_id] = {
            "story": story,
            "save_path": save_path,
            "next_user_actions":[],
            "next_bot_actions":None,
            "story_finished": False
        }

        self.execute_bot_action(story_id)

        return {"action_type":"story_start", "action_properties":self.create_action_properties(story_id), "is_successful":True}, True

    def get_story_response(self, story_id):
        return {"action_type":"story_until_now", "action_properties":self.create_action_properties(story_id), "is_successful":True}, True 




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Face Recognition server')
    parser.add_argument('--ipc_server_host', type=str, default='localhost', help='IPC server hostname (default: localhost)')
    parser.add_argument('--ipc_server_port', type=int, default=5001, help='IPC server port number (default: 5001)')
    parser.add_argument('--stories_folder', type=str, default="./stories", help="The path with the stories' folders (default: ./stories)")
    parser.add_argument('--debug', type=bool, default=False, help='Print debug infos (default: False)')
    args = vars(parser.parse_args())

    fr_server = StoryTellingServer(**args)