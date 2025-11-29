import re
import os
import inspect
import importlib.util
import sys

# Try to import the manual latex mapping if it exists
try:
    from equation_latex_mapping import EQUATION_LATEX_MAP
except ImportError:
    EQUATION_LATEX_MAP = {}

# Helper to extract function source code
def get_function_source(module_path, function_name):
    try:
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = module
        spec.loader.exec_module(module)
        func = getattr(module, function_name)
        source = inspect.getsource(func)
        return source
    except Exception as e:
        # print(f"Could not extract source for {function_name} in {module_path}: {e}")
        return None

def parse_main_model(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    sets = []
    params = []
    vars_ = []
    constraints = []
    imports = {} # name -> module_path
    
    # Determine root folder to resolve imports
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(file_path)))
    
    # Regex patterns
    set_pattern = re.compile(r"model\.(\w+)\s*=\s*Set\(\)")
    param_pattern = re.compile(r"model\.p_(\w+)\s*=\s*Param")
    var_pattern = re.compile(r"model\.v_(\w+)\s*=\s*Var")
    constraint_pattern = re.compile(r"model\.(\w+)\s*=\s*Constraint")
    import_pattern = re.compile(r"from\s+([\w\.]+)\s+import\s+(.+)")
    
    # Helper to extract comment
    def extract_comment(line, prev_lines):
        comment = ""
        if '#' in line:
            comment = line.split('#', 1)[1].strip()
        
        desc = ""
        for i in range(len(prev_lines)-1, -1, -1):
            pl = prev_lines[i].strip()
            if pl.endswith('"""') or pl.endswith("'''"):
                for j in range(i, -1, -1):
                    pl_start = prev_lines[j].strip()
                    if pl_start.startswith('"""') or pl_start.startswith("'''"):
                        raw_desc = " ".join([l.strip() for l in prev_lines[j:i+1]])
                        raw_desc = raw_desc.replace('"""', '').replace("'''", '').strip()
                        desc = raw_desc
                        break
                break
            if pl.startswith('#') or not pl:
                continue
            break
            
        return comment, desc

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            continue

        # Imports
        m = import_pattern.search(line)
        if m:
            module_name = m.group(1)
            imported_items = m.group(2)
            
            # Resolve module path
            module_path = os.path.join(root_folder, module_name.replace('.', '/') + '.py')
            
            if '(' in imported_items:
                # Handle multiline imports or parenthesis
                # Simple heuristic: assume all following comma separated items until ) are imported
                pass 
            
            items = [item.strip() for item in imported_items.split(',') if item.strip()]
            for item in items:
                imports[item] = module_path
            continue

        # Sets
        m = set_pattern.search(line)
        if m:
            name = m.group(1)
            comment, desc = extract_comment(line, lines[:i])
            sets.append({'name': name, 'comment': comment, 'desc': desc})
            continue

        # Parameters
        m = param_pattern.search(line)
        if m:
            name = m.group(1)
            comment, desc = extract_comment(line, lines[:i])
            params.append({'name': name, 'comment': comment, 'desc': desc})
            continue

        # Variables
        m = var_pattern.search(line)
        if m:
            name = m.group(1)
            comment, desc = extract_comment(line, lines[:i])
            vars_.append({'name': name, 'comment': comment, 'desc': desc})
            continue

        # Constraints
        m = constraint_pattern.search(line)
        if m:
            name = m.group(1)
            # Try to find the rule name
            rule_match = re.search(r"rule\s*=\s*(\w+)", line)
            if not rule_match:
                # Check next few lines for rule assignment
                for j in range(i+1, min(i+10, len(lines))):
                    if "rule" in lines[j]:
                        rule_match = re.search(r"rule\s*=\s*(\w+)", lines[j])
                        break
            
            rule_name = rule_match.group(1) if rule_match else name
            
            source_code = None
            if rule_name in imports:
                source_code = get_function_source(imports[rule_name], rule_name)
            
            constraints.append({'name': name, 'rule': rule_name, 'source': source_code})
            continue

    return sets, params, vars_, constraints

def generate_latex(sets, params, vars_, constraints):
    latex = []
    latex.append(r"\documentclass{article}")
    latex.append(r"\usepackage[utf8]{inputenc}")
    latex.append(r"\usepackage{geometry}")
    latex.append(r"\geometry{a4paper, margin=1in}")
    latex.append(r"\usepackage{longtable}")
    latex.append(r"\usepackage{hyperref}")
    latex.append(r"\usepackage{amsmath}")
    latex.append(r"\usepackage{array}") # For p column types
    latex.append(r"\title{OSeMOSYS-Pyomo Model Documentation}")
    latex.append(r"\author{Generated automatically}")
    latex.append(r"\date{\today}")
    latex.append(r"\begin{document}")
    latex.append(r"\maketitle")
    latex.append(r"\tableofcontents")
    latex.append(r"\newpage")

    latex.append(r"\section{General Description}")
    latex.append(r"This document describes the sets, parameters, variables, and equations of the OSeMOSYS-Pyomo model.")

    # Sets
    latex.append(r"\section{Sets}")
    latex.append(r"\begin{longtable}{|p{0.3\textwidth}|p{0.65\textwidth}|}")
    latex.append(r"\hline")
    latex.append(r"\textbf{Set Name} & \textbf{Description} \\")
    latex.append(r"\hline")
    latex.append(r"\endhead")
    for s in sets:
        desc = s['desc'] if s['desc'] else s['comment']
        # escape underscores, $, &
        name = s['name'].replace('_', r'\_')
        desc = desc.replace('_', r'\_').replace('%', r'\%').replace('$', r'\$').replace('&', r'\&')
        latex.append(f"{name} & {desc} \\\\")
        latex.append(r"\hline")
    latex.append(r"\end{longtable}")

    # Parameters
    latex.append(r"\section{Parameters}")
    latex.append(r"\begin{longtable}{|p{0.35\textwidth}|p{0.6\textwidth}|}")
    latex.append(r"\hline")
    latex.append(r"\textbf{Parameter Name} & \textbf{Description} \\")
    latex.append(r"\hline")
    latex.append(r"\endhead")
    for p in params:
        desc = p['desc'] if p['desc'] else p['comment']
        name = "p\_" + p['name'].replace('_', r'\_')
        desc = desc.replace('_', r'\_').replace('%', r'\%').replace('$', r'\$').replace('&', r'\&')
        latex.append(f"{name} & {desc} \\\\")
        latex.append(r"\hline")
    latex.append(r"\end{longtable}")

    # Variables
    latex.append(r"\section{Variables}")
    latex.append(r"\begin{longtable}{|p{0.35\textwidth}|p{0.6\textwidth}|}")
    latex.append(r"\hline")
    latex.append(r"\textbf{Variable Name} & \textbf{Description} \\")
    latex.append(r"\hline")
    latex.append(r"\endhead")
    for v in vars_:
        desc = v['desc'] if v['desc'] else v['comment']
        name = "v\_" + v['name'].replace('_', r'\_')
        desc = desc.replace('_', r'\_').replace('%', r'\%').replace('$', r'\$').replace('&', r'\&')
        latex.append(f"{name} & {desc} \\\\")
        latex.append(r"\hline")
    latex.append(r"\end{longtable}")

    # Constraints
    latex.append(r"\section{Equations}")
    latex.append(r"The following constraints are defined in the model. Where available, the mathematical formulation is provided.")
    
    for c in constraints:
        name_safe = c['name'].replace('_', r'\_')
        rule_name = c['rule']
        latex.append(r"\subsection{" + name_safe + "}")
        
        # Check if we have a manual latex definition
        if rule_name in EQUATION_LATEX_MAP:
            latex.append(r"\begin{equation}")
            latex.append(EQUATION_LATEX_MAP[rule_name])
            latex.append(r"\end{equation}")
        elif c['name'] in EQUATION_LATEX_MAP:
             latex.append(r"\begin{equation}")
             latex.append(EQUATION_LATEX_MAP[c['name']])
             latex.append(r"\end{equation}")
        else:
            latex.append(r"\textit{Equation formulation pending.}")

    latex.append(r"\end{document}")
    return "\n".join(latex)

if __name__ == "__main__":
    main_model_path = "OSeMOSYS/MainModel.py"
    # Add current directory to sys.path to allow importing equation_latex_mapping
    sys.path.append(os.getcwd())
    sys.path.append(os.path.join(os.getcwd(), 'scripts'))

    if not os.path.exists(main_model_path):
        # Fallback for when running from root
        main_model_path = os.path.join(os.getcwd(), "OSeMOSYS/MainModel.py")
    
    sets, params, vars_, constraints = parse_main_model(main_model_path)
    latex_content = generate_latex(sets, params, vars_, constraints)
    
    output_path = "docs/model_documentation.tex"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(latex_content)
    
    print(f"Documentation generated at {output_path}")
