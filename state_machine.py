#!/usr/bin/env python3
"""Finite state machine with guards and actions."""
class StateMachine:
    def __init__(self,initial):
        self.state=initial;self.transitions={};self.on_enter={};self.on_exit={};self.history=[]
    def add_transition(self,from_state,event,to_state,guard=None,action=None):
        self.transitions.setdefault(from_state,{})[event]={"to":to_state,"guard":guard,"action":action}
    def add_enter(self,state,fn): self.on_enter[state]=fn
    def add_exit(self,state,fn): self.on_exit[state]=fn
    def send(self,event,**kwargs):
        trans=self.transitions.get(self.state,{}).get(event)
        if not trans: return False
        if trans["guard"] and not trans["guard"](self.state,event,**kwargs): return False
        old=self.state
        if old in self.on_exit: self.on_exit[old](old,event)
        if trans["action"]: trans["action"](old,event,**kwargs)
        self.state=trans["to"]; self.history.append((old,event,self.state))
        if self.state in self.on_enter: self.on_enter[self.state](self.state,event)
        return True
    def can(self,event):
        return event in self.transitions.get(self.state,{})
if __name__=="__main__":
    sm=StateMachine("idle")
    log=[]
    sm.add_transition("idle","start","running",action=lambda s,e,**k:log.append("started"))
    sm.add_transition("running","pause","paused")
    sm.add_transition("paused","resume","running")
    sm.add_transition("running","stop","idle")
    sm.add_transition("paused","stop","idle")
    sm.send("start"); assert sm.state=="running"
    sm.send("pause"); assert sm.state=="paused"
    sm.send("resume"); assert sm.state=="running"
    sm.send("stop"); assert sm.state=="idle"
    assert len(sm.history)==4; assert "started" in log
    print(f"History: {sm.history}"); print("State machine OK")
