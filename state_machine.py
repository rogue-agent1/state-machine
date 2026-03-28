#!/usr/bin/env python3
"""Finite state machine with DSL-style definition."""
import sys, json

class StateMachine:
    def __init__(self, initial):
        self.state = initial; self.transitions = {}
        self.on_enter = {}; self.on_exit = {}; self.history = [initial]
    def add(self, state, event, next_state, action=None):
        self.transitions[(state, event)] = (next_state, action)
    def send(self, event):
        key = (self.state, event)
        if key not in self.transitions:
            return False
        next_state, action = self.transitions[key]
        old = self.state
        if old in self.on_exit: self.on_exit[old](old, event)
        self.state = next_state
        self.history.append(next_state)
        if action: action(old, event, next_state)
        if next_state in self.on_enter: self.on_enter[next_state](next_state, event)
        return True
    def can(self, event): return (self.state, event) in self.transitions

if __name__ == '__main__':
    # Traffic light example
    sm = StateMachine('red')
    sm.add('red', 'timer', 'green')
    sm.add('green', 'timer', 'yellow')
    sm.add('yellow', 'timer', 'red')
    sm.add('red', 'emergency', 'red')
    sm.add('green', 'emergency', 'red')
    sm.add('yellow', 'emergency', 'red')
    events = ['timer','timer','timer','timer','emergency','timer']
    print("Traffic Light FSM:\n")
    print(f"  State: {sm.state}")
    for e in events:
        sm.send(e)
        print(f"  --{e}--> {sm.state}")
    print(f"\nHistory: {' → '.join(sm.history)}")
