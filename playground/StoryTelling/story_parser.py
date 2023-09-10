import json
import os
import argparse
from typing import Dict, Any, List, Tuple
from .story_classes import Action, Atom, Goal

story_json_template = """
{
    "root_action": "",

    "values_set": {
        
    },

    "atoms": {
    },

    "goal": [],

    "actions": {
        "a0":{
            "nondeterministic": false,
            "pretext": "",
            "text": "",
            "preconditions":{},
            "effects": {}
        }
    },

    "actions_children": {
        
    }
    
}
"""

class Story():
    def __init__(self, root_action_name: str, atoms_init: Dict[str, Atom], goal: Goal, actions: Dict[str, Action], do_action_atoms: Dict[str, Atom], actions_children: Dict[str, Tuple[List[Action]]], story_name: str = "interactive_story") -> None:
        self.story_name = story_name
        self.root_action_name = root_action_name
        self.atoms_init = atoms_init
        self.goal = goal
        self.actions = actions
        self.do_action_atoms = do_action_atoms
        self.actions_children = actions_children

        self.knoweledge_base = {
            key:atom.clone() for key,atom in self.atoms_init.items()
        }

        self.actions_history = []
    
    def execute_action(self, action_name):
        action = self.actions.get(action_name, None)
        if action == None: return []

        self.knoweledge_base.update(action.effects)
        self.actions_history.append(action)
        next_actions = [act for block in self.actions_children.get(action_name,([],[])) for act in block]
        return next_actions
    
    
    def genPDDLDomain(self) -> str:
        predicates_str = "\n\t".join([atom.toPDDL(predicate=True) for atom in {**self.do_action_atoms,**self.atoms_init}.values()])

        actions_str = ""
        for action_name, action in self.actions.items():
            det_children_actions, nondet_children_actions = self.actions_children.get(action_name,([],[]))
            act_str = action.toPDDL(
                all_do_action_atoms=[atom for atom in self.do_action_atoms.values()],
                det_children_do_action_atoms=[action.do_action_atom for action in det_children_actions],
                nondet_children_do_action_atoms=[action.do_action_atom for action in nondet_children_actions]
            )
            actions_str += (act_str + "\n\n")
        
        domain_str = f"(define (domain {self.story_name}_domain)\n(:requirements :conditional-effects :disjunctive-preconditions)\n\n(:predicates\n\t{predicates_str}\n)\n\n{actions_str}\n)"
        return domain_str
    
    def genPDDLProblems(self, next_actions: List[Action] = None) -> List[str]:
        if next_actions == None:
            next_actions_atoms = [(self.do_action_atoms[self.root_action_name].clone())(True)] # The initial action
        else:
            next_actions_atoms = [(act.do_action_atom.clone())(True) for act in next_actions]

        init_str = "\n\t".join([atom.toPDDL() for atom in [*next_actions_atoms, *self.knoweledge_base.values()]])

        problem_strs = [f"(define (problem {self.story_name}_problem)\n(:domain {self.story_name}_domain) \n(:init\n\t{init_str}\n) \n{g}\n)" for g in self.goal]
        return problem_strs
    
    def write_domain_file(self, domain_str: str, path: str = "."):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/domain.pddl", "w") as domain_file:
            domain_file.write(domain_str)
    
    def write_problem_file(self, problem_str: str, path: str = "."):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/problem.pddl", "w") as problem_file:
            problem_file.write(problem_str)

    def create_files(self, domain_str: str, problem_str: str, path: str = "."):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/domain.pddl", "w") as domain_file:
            domain_file.write(domain_str)
        with open(f"{path}/problem.pddl", "w") as problem_file:
            problem_file.write(problem_str)


def read_story_file(path, lang="en-US") -> Story:
    with open(path, "r") as f:
        story_obj = json.load(f)

    root_action_name = story_obj["root_action"]

    # Selecting the right values given the selected language
    og_values_set = story_obj["values_set"]
    values_set: Dict[str, str] = {}
    for val_name, val_dict in og_values_set.items():
        val = (list(val_dict.values())+[""])[0] # Set the string by default as the first of the list in case the requested language is not present. If the val set is empty, use an empty string
        if lang in val_dict:
            val = val_dict[lang]
        elif "en-US" in val_dict:
            val = val_dict["en-US"]
        values_set[val_name] = val

    # Extracting the list of atoms
    og_atoms = story_obj["atoms"]
    atoms_init: Dict[str, Atom] = {}
    for atom_name, atom_val in og_atoms.items():
        atom_obj = Atom(atom_name,atom_val)
        atoms_init[atom_name] = atom_obj
    
    goal = Goal(story_obj["goal"])

    og_actions = story_obj["actions"]
    actions: Dict[str, Action] = {}
    do_action_atoms: Dict[str, Atom] = {}
    for action_name, action_val in og_actions.items():

        preconditions = {}
        for precond_atom_name, precond_atom_val in action_val["preconditions"].items():
            atom_obj = Atom(precond_atom_name,precond_atom_val)
            preconditions[precond_atom_name] = atom_obj

        effects = {}
        for eff_atom_name, eff_atom_val in action_val["effects"].items():
            atom_obj = Atom(eff_atom_name,eff_atom_val)
            effects[eff_atom_name] = atom_obj

        do_action_atom = Atom("do_"+action_name, False)

        action_obj = Action(
            name=action_name,
            pretext=values_set[action_val["pretext"]],
            text=values_set[action_val["text"]],
            mood=action_val.get("mood","happy"),
            preconditions=preconditions,
            effects=effects,
            nondeterministic=action_val.get("nondeterministic", False),
            do_action_atom=do_action_atom
        )

        actions[action_name] = action_obj
        do_action_atoms[action_name] = do_action_atom
    
    
    og_actions_children = story_obj["actions_children"]
    actions_children: Dict[str, Tuple[List[Action]]] = {}
    for action_name, act_children in og_actions_children.items():
        det_children: List[Action] = []
        nondet_children: List[Action] = []
        for child_name in act_children:
            child_action = actions[child_name]
            if child_action.nondeterministic:
                nondet_children.append(actions[child_name])
            else:
                det_children.append(actions[child_name])
        actions_children[action_name] = (det_children,nondet_children)

    story_name = os.path.splitext(os.path.basename(path))[0]
    return Story(story_name=story_name,
                 root_action_name=root_action_name,
                 atoms_init=atoms_init,
                 goal=goal,
                 actions=actions,
                 do_action_atoms=do_action_atoms,
                 actions_children=actions_children)

def generate_boilerplate_story_file(path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f"{path}", "w") as file:
        file.write(story_json_template)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('json_path', help='Path to the json file containing the story')
    parser.add_argument('pddl_path', default="", help='Path where to save the pddl domain and problem files')
    args = parser.parse_args()

    story = read_story_file(args.json_path)
    domain_str = story.genPDDLDomain()
    problem_strs = story.genPDDLProblems()

    save_path = args.pddl_path if args.pddl_path != "" else os.path.dirname(args.json_path)
    story.create_files(domain_str = domain_str, problem_str = problem_strs[0], path = save_path)

