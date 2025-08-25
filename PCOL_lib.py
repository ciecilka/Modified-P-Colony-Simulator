import random
import math
#from typing import List, Tuple

MAX=100


class Rule:
    n_rules = 0
    def __init__(self,type:str, lhs:str,rhs:str,RAI:float):
        Rule.n_rules += 1
        self.rule_number = Rule.n_rules
        self.type = type
        self.rhs=str()
        self.rhs = rhs
        self.lhs=str()
        self.lhs = lhs
        self.RAI = RAI

    def __str__(self):
        return f"rule {self.rule_number}: ({self.type}, {self.lhs}, {self.rhs}, {self.RAI})"
    
    def print_rule(self):
        return f"rule {self.rule_number}: ({self.type}, {self.lhs}, {self.rhs}, {self.RAI})"
    
    def change_RAI(self, operator: str, number: float):
        if(operator=="plus"):
            self.RAI += number
        elif(operator =="times"):
            self.RAI *= number
        elif(operator =="minus"):
            self.RAI -= number
        elif(operator =="div"):
            self.RAI /= number
        if self.RAI < 1:
            self.RAI = 1 
        #print(str(self.RAI))

    def get_RAI(self):
        return self.RAI

    def get_lhs(self):
        return self.lhs
    
    def get_rhs(self):
        return self.rhs
    
    def get_type(self):
        return self.type

class Agent:
    n_agents = 0
    def __init__(self, content:str, rules:list[Rule]):
        
        Agent.n_agents += 1
        self.agent_number = Agent.n_agents
        self.content=str()
        self.content = content
        #self.rules = list()
        self.rules = rules
        i=1
        for r in self.rules:
            r.rule_number=i
            i += 1


    def print_agent(self):
        prules=""
        for rule in self.rules:
            prules=prules+", "+rule.print_rule()

        return f"Agent {self.agent_number}: ({self.content}, [{prules}])"   
    
    def get_content(self):
        return self.content
    
    def get_RAI_vector(self):
        RAI_vector= list()
        for rule in self.rules:
            RAI_vector.append(rule.get_RAI())
        return RAI_vector
    
    def get_rules(self):
        return self.rules
    
    def set_content(self, new_content:str):
        self.content=new_content

class Colony:
    def __init__(self,alphabet:list[str],env_chr:str,content:str, agents:list[Agent], op_plus:str, num_plus:float, op_minus:str, num_minus:float, fin_opt:list[str]):
        self.alphabet=alphabet
        self.env_chr=env_chr
        self.content=content
        self.agents=agents
        self.op_plus=op_plus
        self.op_minus=op_minus
        self.num_plus=num_plus
        self.num_minus=num_minus
        self.fin_opt=fin_opt
    
    def print_colony(self):
        agentlist="Agents: "
        for agent in self.agents:
            agentlist=agentlist+", "+agent.print_agent()
        
        fopt="["+str(self.fin_opt[0])+", "+str(self.fin_opt[1])+", "+str(self.fin_opt[2])+"]"
        return f"P Colony: (A={self.alphabet}, e='{self.env_chr}', {agentlist}, w_E= {self.content}, plus:{self.op_plus}{self.num_plus}, minus: {self.op_minus}{self.num_minus}, fin= {self.fin_opt})"

    def get_content(self):
        return self.content
    
    def get_opplus(self):
        return self.op_plus
    
    def get_opminus(self):
        return self.op_minus
    
    def get_numplus(self):
        return self.num_plus
    
    def get_numminus(self):
        return self.num_minus
    
    def get_num_agents(self):
        return len(self.agents)
    
    def get_contents_agents(self):
        contents=list()
        for agent in self.agents:
            contents.append(agent.content)
        return contents
    
    def get_all_rules(self):
        rules=list()
        for agent in self.agents:
            rules= rules+agent.rules
        return rules

    def get_fin_opt(self):
        return self.fin_opt
    
    def get_fin_object(self):
        return self.fin_opt[1]
    
    def get_res_mode(self):
        return self.fin_opt[2]
    
    def get_res_area(self):
        return self.fin_opt[0]
    
    def get_config(self):
        config="("+self.content+", "
        rai_vector=list()
        for agent in self.agents:
            config=config + agent.content+", "
            rai_vector.append(agent.get_RAI_vector())
        config=config + "["
        for vector in rai_vector:
            config=config + "("
            for i in range(len(vector)):
                config=config + str(vector[i])
                if i<(len(vector)-1): config +=", " 
            config += "), "
        config = config[:-2]
        config += "])\n"
        return config


    def update_content(self, new_content:str):
        self.content=new_content

    def update_contents_agents(self, new_contnets:list[str]):
        i=1
        for agent in self.agents:
            agent.content=new_contnets[i-1]
            i=i+1
        
    def update_content_agent(self,i:int,content:str):
        self.agents[i-1].content=content

    def find_applicable_rules(self) -> list[tuple[int,Rule]]:
        app_rules=list()
        for agent in self.agents:
            #print("Agent "+str(agent.agent_number))
            for rule in agent.rules:
                #print(rule.print_rule()+"\n")
                #print(agent.content.count(rule.lhs))
                if (agent.content.count(rule.lhs) >= math.floor(rule.RAI))or(rule.lhs=="*"):
                    #print(rule.print_rule())
                    #print((agent.content.count(rule.lhs) >= math.floor(rule.RAI))or(rule.lhs==""))
                    if rule.type == "com":
                        if (self.content.count(rule.rhs) >= math.floor(rule.RAI))or(rule.rhs=="*")or(rule.rhs==self.env_chr):
                            app_rules.append([agent.agent_number,rule])
                    else:
                        app_rules.append([agent.agent_number,rule])
        
        return app_rules