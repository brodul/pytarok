"""
Pretty broken
"""
import os
from copy import deepcopy

from transitions.extensions import MachineFactory

from pytarok.game import Session

dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    diagram_cls = MachineFactory.get_predefined(graph=True)
    machine = deepcopy(Session().machine)
    states = machine.states.keys()
    transitions = machine.get_transitions()
    dtransitions = [
        {k: getattr(t, k, "") for k in ("source", "dest", "conditions", "trigger")}
        for t in transitions
    ]
    diagram_machine = diagram_cls(
        machine.model, list(states), machine.model.state, dtransitions
    )

    diagram_machine.get_graph().draw(os.path.join(dir_path, "out.png"), prog="dot")
