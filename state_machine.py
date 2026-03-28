#!/usr/bin/env python3
"""Finite state machine with guards and actions."""
import sys
class StateMachine:
    def __init__(self,initial):
        self.state=initial;self.transitions={};self.on_enter={};self.on_exit={};self.history=[]
    def add(self,state,event,target,guard=None,action=None):
        self.transitions.setdefault(state,{})[event]=(target,guard,action)
    def enter(self,state,fn): self.on_enter[state]=fn
    def exit(self,state,fn): self.on_exit[state]=fn
    def send(self,event,ctx=None):
        t=self.transitions.get(self.state,{}).get(event)
        if not t: return False
        target,guard,action=t
        if guard and not guard(ctx): return False
        old=self.state
        if old in self.on_exit: self.on_exit[old](ctx)
        if action: action(ctx)
        self.state=target;self.history.append((old,event,target))
        if target in self.on_enter: self.on_enter[target](ctx)
        return True
def main():
    sm=StateMachine("idle")
    sm.add("idle","start","running")
    sm.add("running","pause","paused")
    sm.add("running","complete","done")
    sm.add("paused","resume","running")
    sm.add("paused","cancel","idle")
    sm.enter("running",lambda _:print("  → Entered RUNNING"))
    sm.exit("running",lambda _:print("  ← Exited RUNNING"))
    events=["start","pause","resume","complete"]
    for e in events:
        ok=sm.send(e)
        print(f"Event '{e}': {'✓' if ok else '✗'} → state={sm.state}")
    print(f"\nHistory: {sm.history}")
if __name__=="__main__": main()
