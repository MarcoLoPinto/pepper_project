import os
import argparse

DIR = os.path.realpath(os.path.dirname(__file__))


def get_actions_plan(pddl_folder_path, options = '--debug-output 1 --dump-policy 2 --detect-deadends 1', do_print=False):
    # Prepare the input
    pddl_domain_filepath = os.path.join(pddl_folder_path, 'domain.pddl')
    pddl_problem_filepath = os.path.join(pddl_folder_path, 'problem.pddl')
    # Run the bash script and capture the output
    output = os.popen('%s/PRP/src/prp %s %s %s' %(DIR,pddl_domain_filepath, pddl_problem_filepath, options)).read()
    # Save the formatted output in list of actions and results
    steps = []
    # Split the output into lines and iterate over them
    lines = output.split("\n")
    for i, line in enumerate(lines):
        if "Chosen operator:" in line:
            target_line = lines[i+1].strip()
            action_params = target_line[target_line.index('(')+1 : target_line.index(')')].strip().split(' ')
            action = action_params[0]
            parameters = action_params[1:]
            if do_print: print(action, parameters)
            steps.append({"action":action,"parameters":parameters})

    # # Open the file for reading
    # with open('./policy.out', 'r') as f:
    #     # Read the entire contents of the file
    #     file_contents = f.read()

    # # Print the contents of the file
    # print(file_contents)

    # Remove files generated from prp
    for file in [   './elapsed.time','./human_policy.pol','./output','./output.sas',
                    './plan_numbers_and_cost','policy.fsap','./policy.out','./sas_plan']:
        try:
            os.remove(file)
        except:
            pass
    return steps

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('pddl_folder_path', help='Path to the folder containing domain.pddl and problem.pddl files')
    parser.add_argument('--options', default='--debug-output 1 --dump-policy 2 --detect-deadends 1', help='Additional options to pass to PRP')
    args = parser.parse_args()
    
    # Call the function with the command-line arguments
    get_actions_plan(args.pddl_folder_path, args.options, True)