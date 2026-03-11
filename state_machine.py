#!/usr/bin/env python3
"""state_machine — Finite state machine with guards and actions. Zero deps."""

class StateMachine:
    def __init__(self, initial):
        self.state = initial
        self.transitions = {}
        self.on_enter = {}
        self.on_exit = {}
        self.history = [initial]

    def add_transition(self, from_state, event, to_state, guard=None, action=None):
        self.transitions.setdefault((from_state, event), []).append((to_state, guard, action))

    def add_enter(self, state, callback):
        self.on_enter[state] = callback

    def add_exit(self, state, callback):
        self.on_exit[state] = callback

    def send(self, event, **ctx):
        key = (self.state, event)
        for to_state, guard, action in self.transitions.get(key, []):
            if guard and not guard(ctx):
                continue
            if self.state in self.on_exit:
                self.on_exit[self.state](self.state, event)
            old = self.state
            self.state = to_state
            if action:
                action(old, event, to_state, ctx)
            if to_state in self.on_enter:
                self.on_enter[to_state](to_state, event)
            self.history.append(to_state)
            return True
        return False

    def can(self, event):
        return (self.state, event) in self.transitions

def main():
    sm = StateMachine("idle")
    log = []
    sm.add_transition("idle", "start", "running", action=lambda *a: log.append("Started"))
    sm.add_transition("running", "pause", "paused")
    sm.add_transition("paused", "resume", "running")
    sm.add_transition("running", "stop", "idle", action=lambda *a: log.append("Stopped"))
    sm.add_transition("paused", "stop", "idle")
    # Guarded transition
    sm.add_transition("running", "error", "failed", guard=lambda ctx: ctx.get("severity") == "critical")
    sm.add_transition("failed", "reset", "idle")

    events = [("start",{}), ("pause",{}), ("resume",{}), ("error",{"severity":"warning"}),
              ("error",{"severity":"critical"}), ("reset",{})]
    print("State Machine:")
    for event, ctx in events:
        old = sm.state
        ok = sm.send(event, **ctx)
        print(f"  {old} --{event}--> {sm.state} {'✓' if ok else '✗ (blocked)'}")
    print(f"\nHistory: {' -> '.join(sm.history)}")
    print(f"Actions: {log}")

if __name__ == "__main__":
    main()
