from typing import Any, Tuple, List, Dict

TERMINAL_ATOM_NAME = "$end$"

class MultiText():
    def __init__(self, *language_and_text: List[Tuple[str,str]]) -> None:
        self.texts = {}
        for lang, text in language_and_text:
            self.texts[lang] = text

    def __getitem__(self, lang: str):
        return self.texts[lang]
    
    def __setitem__(self, lang: str, text: str):
        self.texts[lang] = text

class Atom():
    def __init__(self, name, value: bool) -> None:
        self.name = name
        self.value = bool(value)

    def __call__(self, newValue: bool = None) -> Any:
        if newValue != None: self.value = bool(newValue)
        return self

    def clone(self):
        return Atom(name=self.name, value=self.value)

    def toPDDL(self, predicate=False):
        if predicate or self.value == True:
            return f"({self.name})"
        else:
            return f"(not ({self.name}))"
        
    def __str__(self) -> str:
        return "Atom " + self.name
    def __repr__(self) -> str:
        return "Atom " + self.name

class Action():
    def __init__(self, name:str, pretext: str, text: str, mood: str, preconditions: Dict[str, Atom] = {}, effects: Dict[str, Atom] = {}, nondeterministic: bool = False, do_action_atom: Atom = None) -> None:
        self.name = name
        self.pretext = pretext
        self.text = text
        self.mood = mood
        self.preconditions = preconditions
        self.effects = effects
        self.nondeterministic = nondeterministic
        self.do_action_atom =  do_action_atom if do_action_atom != None else Atom("do_"+name, False)
    
    def __str__(self) -> str:
        return "Action " + self.name
    def __repr__(self) -> str:
        return "Action " + self.name
    
    def toPDDL(self, all_do_action_atoms: List[Atom], det_children_do_action_atoms: List[Atom], nondet_children_do_action_atoms: List[Atom]):

        nonchildren_do_action_atoms = [atom for atom in all_do_action_atoms if (atom not in det_children_do_action_atoms) and (atom not in nondet_children_do_action_atoms)]

        precondition_str = f"and {self.do_action_atom(True).toPDDL()} " + " ".join([atom.toPDDL() for atom in self.preconditions.values()])

        nonchildren_effect_str = " ".join([Atom(atom.name, False).toPDDL() for atom in nonchildren_do_action_atoms])
        det_children_effect_str = " ".join([Atom(atom.name, True).toPDDL() for atom in det_children_do_action_atoms])
        nondet_children_effect_str = "(oneof " + " ".join([Atom(atom.name, True).toPDDL() for atom in nondet_children_do_action_atoms]) + ")" if len(nondet_children_do_action_atoms) > 0 else ""
        personale_effect_str = " ".join([atom.toPDDL() for atom in self.effects.values()])
        terminal_atom = Atom(TERMINAL_ATOM_NAME,True).toPDDL() if len(det_children_do_action_atoms)+len(nondet_children_do_action_atoms) == 0 else ""
        
        effect_str = f"and {nonchildren_effect_str} {det_children_effect_str} {nondet_children_effect_str} {personale_effect_str} {terminal_atom}" 

        return f"(:action {self.name} \n\t:parameters () \n\t:precondition(\n\t\t{precondition_str}\n\t) \n\t:effect(\n\t\t{effect_str}\n\t)\n)"
    
class Goal():
    def __init__(self, goalList: List[List[str]] = []) -> None:
        self.atomToken = "atom"
        self.functionTokens = ["and"]
        goalList.append(["atom",TERMINAL_ATOM_NAME,True])
        isValid = True
        for subGoalList in goalList:
            isValid = self.__validateList(subGoalList)
            if not isValid: break
        if isValid == False: raise Exception("The Goal is not well formatted")
        self.goalList = goalList

    def __validateList(self, goalList):
        func, val = goalList[0], goalList[1:]
        if (func not in self.functionTokens and func != self.atomToken):
            return False
        
        if func == self.atomToken:
            if len(val) != 2:
                return False
            if not isinstance(val[0],str):
                return False
            
        else:
            if not isinstance(val[0],list):
                return False
            for subList in val:
                subResult = self.__validateList(subList)
                if subResult == False:
                    return False

        return True
    
    def toPDDL(self, index=0):
        return f"(:goal\n\t{self.__toPDDLBlock(self.goalList[index])}\n)"
        
    
    def __toPDDLBlock(self,goalList):
        func, val = goalList[0], goalList[1:]
        
        if func == self.atomToken: return Atom(val[0],val[1]).toPDDL()
            
        else:
            pddl_block = f"({func} "
            for subList in val:
                subResult = self.__toPDDLBlock(subList)
                pddl_block = pddl_block + subResult + " "

        return pddl_block + ")"

    def __len__(self):
        return len(self.goalList)
    
    def __iter__(self):
        return iter([self.toPDDL(i) for i in range(len(self))])
