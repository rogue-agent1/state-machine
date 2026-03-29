#!/usr/bin/env python3
"""State machine — FSM with guards, actions, and history."""
import sys

class Transition:
    def __init__(self, event, target, guard=None, action=None):
        self.event = event; self.target = target; self.guard = guard; self.action = action

class StateMachine:
    def __init__(self, initial, states):
        self.current = initial; self.states = states; self.history = [initial]; self.context = {}
    def send(self, event, **kwargs):
        self.context.update(kwargs)
        transitions = self.states.get(self.current, [])
        for t in transitions:
            if t.event == event:
                if t.guard and not t.guard(self.context): continue
                if t.action: t.action(self.context)
                old = self.current; self.current = t.target
                self.history.append(self.current)
                return f"{old} --[{event}]--> {self.current}"
        return f"{self.current}: no transition for '{event}'"
    def matches(self, state): return self.current == state

if __name__ == "__main__":
    def has_items(ctx): return ctx.get("items", 0) > 0
    def add_item(ctx): ctx["items"] = ctx.get("items", 0) + 1
    def clear(ctx): ctx["items"] = 0
    order_sm = StateMachine("idle", {
        "idle": [Transition("add_item", "has_items", action=add_item)],
        "has_items": [
            Transition("add_item", "has_items", action=add_item),
            Transition("checkout", "reviewing", guard=has_items),
            Transition("clear", "idle", action=clear),
        ],
        "reviewing": [
            Transition("confirm", "processing"),
            Transition("cancel", "has_items"),
        ],
        "processing": [
            Transition("payment_ok", "shipped"),
            Transition("payment_fail", "reviewing"),
        ],
        "shipped": [Transition("deliver", "delivered")],
        "delivered": [],
    })
    events = ["add_item", "add_item", "checkout", "confirm", "payment_ok", "deliver"]
    for e in events: print(f"  {order_sm.send(e)}")
    print(f"\nHistory: {' -> '.join(order_sm.history)}")
    print(f"Items in context: {order_sm.context.get('items', 0)}")
