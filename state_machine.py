#!/usr/bin/env python3
"""state_machine - Finite state machine implementation."""
import sys
class StateMachine:
    def __init__(s,initial):s.state=initial;s.transitions={};s.actions={};s.history=[initial]
    def add(s,frm,event,to,action=None):s.transitions[(frm,event)]=to;
    if action:s.actions[(frm,event)]=action
    def trigger(s,event):
        key=(s.state,event)
        if key not in s.transitions:raise ValueError(f"No transition from {s.state} on {event}")
        if key in s.actions:s.actions[key]()
        s.state=s.transitions[key];s.history.append(s.state)
    def can(s,event):return(s.state,event) in s.transitions
    def reset(s):s.state=s.history[0];s.history=[s.history[0]]
if __name__=="__main__":
    sm=StateMachine("idle")
    sm.add("idle","start","running");sm.add("running","pause","paused")
    sm.add("paused","resume","running");sm.add("running","stop","idle")
    sm.add("paused","stop","idle")
    events=["start","pause","resume","stop"]
    for e in events:
        print(f"  {sm.state} --{e}--> ",end="");sm.trigger(e);print(sm.state)
    print(f"  History: {' → '.join(sm.history)}")
