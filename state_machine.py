#!/usr/bin/env python3
"""state_machine - Finite state machine framework."""
import argparse, json

class StateMachine:
    def __init__(self, initial, transitions, accepting=None):
        self.state = initial; self.initial = initial
        self.transitions = transitions  # {(state, event): new_state}
        self.accepting = accepting or set()
        self.history = [initial]
    def send(self, event):
        key = (self.state, event)
        if key in self.transitions:
            old = self.state
            self.state = self.transitions[key]
            self.history.append(self.state)
            return old, self.state
        return self.state, None
    def is_accepting(self): return self.state in self.accepting
    def reset(self): self.state = self.initial; self.history = [self.initial]
    def process(self, events):
        results = []
        for e in events:
            old, new = self.send(e)
            results.append({"event": e, "from": old, "to": new or old})
        return results

def main():
    p = argparse.ArgumentParser(description="State machine")
    p.add_argument("--demo", choices=["turnstile", "traffic", "vending"], default="turnstile")
    p.add_argument("-e", "--events", nargs="+")
    args = p.parse_args()
    if args.demo == "turnstile":
        sm = StateMachine("locked", {
            ("locked", "coin"): "unlocked", ("unlocked", "push"): "locked",
            ("locked", "push"): "locked", ("unlocked", "coin"): "unlocked"
        })
        events = args.events or ["push", "coin", "push", "push", "coin", "coin", "push"]
    elif args.demo == "traffic":
        sm = StateMachine("green", {
            ("green", "timer"): "yellow", ("yellow", "timer"): "red",
            ("red", "timer"): "green", ("red", "emergency"): "red",
            ("green", "emergency"): "red", ("yellow", "emergency"): "red"
        })
        events = args.events or ["timer", "timer", "timer", "emergency", "timer", "timer"]
    elif args.demo == "vending":
        sm = StateMachine("idle", {
            ("idle", "coin"): "has_coin", ("has_coin", "coin"): "has_two",
            ("has_two", "select"): "dispensing", ("dispensing", "done"): "idle",
            ("has_coin", "cancel"): "idle", ("has_two", "cancel"): "idle"
        })
        events = args.events or ["coin", "coin", "select", "done", "coin", "cancel"]
    results = sm.process(events)
    for r in results:
        arrow = f"{r['from']} -> {r['to']}" if r['to'] != r['from'] else f"{r['from']} (no change)"
        print(f"  [{r['event']:>10s}] {arrow}")
    print(f"\nFinal state: {sm.state}")
    print(f"History: {' -> '.join(sm.history)}")

if __name__ == "__main__":
    main()
