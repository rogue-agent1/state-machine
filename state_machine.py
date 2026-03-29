#!/usr/bin/env python3
"""Finite state machine with guards, actions, and hierarchical states."""
import sys

class State:
    def __init__(self, name, on_enter=None, on_exit=None, parent=None):
        self.name = name; self.on_enter = on_enter; self.on_exit = on_exit
        self.parent = parent; self.transitions = {}
    def __repr__(self): return f"State({self.name})"

class Transition:
    def __init__(self, target, guard=None, action=None):
        self.target = target; self.guard = guard; self.action = action

class StateMachine:
    def __init__(self, initial):
        self.states = {}; self.current = None; self.initial = initial
        self.history = []; self.context = {}

    def add_state(self, state):
        self.states[state.name] = state; return state

    def add_transition(self, source, event, target, guard=None, action=None):
        if isinstance(source, str): source = self.states[source]
        t = Transition(target, guard, action)
        source.transitions.setdefault(event, []).append(t)

    def start(self):
        self.current = self.states[self.initial]
        self.history.append(self.current.name)
        if self.current.on_enter: self.current.on_enter(self.context)

    def send(self, event, **kwargs):
        self.context.update(kwargs)
        state = self.current
        while state:
            if event in state.transitions:
                for t in state.transitions[event]:
                    if t.guard is None or t.guard(self.context):
                        if self.current.on_exit: self.current.on_exit(self.context)
                        if t.action: t.action(self.context)
                        self.current = self.states[t.target]
                        self.history.append(self.current.name)
                        if self.current.on_enter: self.current.on_enter(self.context)
                        return True
            state = self.states.get(state.parent) if hasattr(state, 'parent') and state.parent else None
        return False

    def is_in(self, state_name): return self.current.name == state_name

    def visualize(self):
        lines = [f"Current: [{self.current.name}]", ""]
        for name, state in self.states.items():
            for event, transitions in state.transitions.items():
                for t in transitions:
                    guard = f" [{t.guard.__name__}]" if t.guard else ""
                    lines.append(f"  {name} --{event}{guard}--> {t.target}")
        return "\n".join(lines)

def demo():
    print("=== State Machine: Traffic Light ===\n")
    sm = StateMachine("red")
    sm.add_state(State("red", on_enter=lambda ctx: print("  🔴 RED - Stop!")))
    sm.add_state(State("green", on_enter=lambda ctx: print("  🟢 GREEN - Go!")))
    sm.add_state(State("yellow", on_enter=lambda ctx: print("  🟡 YELLOW - Caution!")))
    sm.add_transition("red", "timer", "green")
    sm.add_transition("green", "timer", "yellow")
    sm.add_transition("yellow", "timer", "red")
    sm.add_transition("red", "emergency", "red")
    sm.add_transition("green", "emergency", "red")
    sm.add_transition("yellow", "emergency", "red")
    sm.start()
    for event in ["timer", "timer", "timer", "timer", "emergency", "timer"]:
        print(f"Event: {event}")
        sm.send(event)
    print(f"\nHistory: {' -> '.join(sm.history)}")
    print(f"\n{sm.visualize()}")

    print("\n=== State Machine: Vending Machine ===\n")
    vm = StateMachine("idle")
    vm.add_state(State("idle", on_enter=lambda ctx: print(f"  Insert coins (balance: {ctx.get('balance',0)}¢)")))
    vm.add_state(State("selecting", on_enter=lambda ctx: print(f"  Select item (balance: {ctx['balance']}¢)")))
    vm.add_state(State("dispensing", on_enter=lambda ctx: print(f"  Dispensing {ctx.get('item','?')}!")))
    vm.add_transition("idle", "coin", "selecting", action=lambda ctx: ctx.update({"balance": ctx.get("balance",0)+25}))
    sm2 = vm
    sm2.add_transition("selecting", "coin", "selecting", action=lambda ctx: ctx.update({"balance": ctx["balance"]+25}))
    sm2.add_transition("selecting", "select", "dispensing",
        guard=lambda ctx: ctx.get("balance",0) >= 50,
        action=lambda ctx: ctx.update({"balance": ctx["balance"]-50}))
    sm2.add_transition("dispensing", "done", "idle")
    sm2.start()
    for event, kw in [("coin",{}), ("coin",{}), ("select",{"item":"Cola"}), ("done",{})]:
        print(f"Event: {event} {kw}")
        sm2.send(event, **kw)

def main(): demo()
if __name__ == "__main__": main()
