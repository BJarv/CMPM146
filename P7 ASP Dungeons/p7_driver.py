import subprocess
from p7_visualize import parse_json_result
from p7_visualize import render_ascii_dungeon

def solve():
    """Run clingo with the provided argument list and return the parsed JSON result."""
    
    #CLINGO = "./clingo-4.5.0-macos-10.9/clingo"
    
    #clingo = subprocess.Popen(
    #    [CLINGO, "--outf=2"] + list(args),
    #    stdout=subprocess.PIPE,
    #    stderr=subprocess.PIPE)
    command = "./gringo level-core.lp level-style.lp level-sim.lp level-shortcuts.lp | ./reify | ./clingo - meta.lp metaD.lp metaO.lp metaS.lp --parallel-mode=4 --outf=2 > example_noshortcut.json"
    clingo = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = clingo.communicate()
    if err:
        print err
        
    return parse_json_result(out)

map = solve()
print render_ascii_dungeon(map)