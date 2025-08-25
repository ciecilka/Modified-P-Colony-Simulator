import random
import math

#from typing import List, Tuple
from PCOL_lib import Agent,Colony,Rule
E_strings=list()
step_period=100

def pressed_y() -> bool:
    klavesa = input("Enter Y to continue, otherwise enter any other key: ").strip().lower()
    return klavesa == "y"

def extract(string:str,c:str)->str:
    idx=string.find(c)
    if idx != -1:
        string = string[:idx]+string[idx+1:]
    if string=="": string="*"
    return string

def replace(string:str,c:str,d:str)->str:
    if c=="*"and d=="*": pass
    elif c=="*"and d!="*":
        if string!="*":string+=d
        else: string=d
    else:
        idx=string.find(c)
        if idx != -1:
            if(d!="*"):
                string = string[:idx]+d+string[idx+1:]
            else:
                string = string[:idx]+string[idx+1:]
    if string=="":string="*"
    #print(string)
    return string 

def check_env (env_chr, alphabet):
        if env_chr in alphabet: return env_chr
        else: 
            E_strings.append("env_ch not in Alphabet")
            return 0

def check_char (chr, alphabet):
        if (chr in alphabet)or(chr=="lambda"): 
            if chr=="lambda": chr="*"
            return chr
        else: 
            E_strings.append("env_ch not in Alphabet")
            return 0

def check_content(content:str,alphabet):
    if not all(znak in alphabet for znak in content)and not(content=="lambda"): 
        E_strings.append("environment contains wrong symbol")
        return 0
    if content=="lambda": content="*"
    return content

def check_op(op):
        if op not in {"plus","minus","times","div"}:    
            E_strings.append("operation is unrecognized, use: plus, minus, times or div")
            return 0
        return op

def check_rmode(mode):
        if mode not in {"hr","emr","epr"}:    
            E_strings.append("result mode is unrecognized, use: hr, emr or epr")
            return 0
        return mode

def check_type(mode):
        if mode not in {"evo","com"}:    
            E_strings.append("rule type is not valid, use: evo or com")
            return 0
        return mode

def check_float(num):
        if not isinstance(num, float):
            E_strings.append("number "+num+" is not float")
            return 0
        return num

def random_max_set_rules(colony:Colony,appset:list[tuple[int,Rule]])->list[tuple[int,Rule]]:
    content=colony.get_content()
    agent_content=colony.get_contents_agents()
    a_rules=list()
    b_rules=appset

    while len(b_rules)>0:
        i = random.randrange(len(b_rules))
        selected_rule=b_rules.pop(i)
        type=selected_rule[1].get_type()
        lhs=selected_rule[1].get_lhs()
        rhs=selected_rule[1].get_rhs()
        RAI=selected_rule[1].get_RAI()
        n_agent=selected_rule[0]
        #print("Agent: "+str(selected_rule[0])+selected_rule[1].print_rule())

        notfind=0
        j=0
        if ((agent_content[n_agent-1].count(lhs)>=math.floor(RAI))or(lhs=="*"))and(not(type=="com")or((content.count(rhs)>=math.floor(RAI))or(rhs=="*")or(rhs==colony.env_chr))):
            #print(((agent_content[n_agent-1].count(lhs)>=math.floor(RAI))or(lhs=="*"))and(not(type=="com")or((content.count(rhs)>=math.floor(RAI))or(rhs=="*")or(rhs==colony.env_chr))))
            while (j< math.floor(RAI)):
                #print("j:"+str(j)+", RAI:"+str(math.floor(RAI)))
                #print("before: "+agent_content[n_agent-1])
                idx = agent_content[n_agent-1].find(lhs)
                #print("lhs:"+lhs+", agent_con:"+agent_content[n_agent-1]+", find:"+str(idx))
                if idx != -1:
                    agent_content[n_agent-1] = agent_content[n_agent-1][:idx] + agent_content[n_agent-1][idx+1:] 
                #print(" after: "+ agent_content[n_agent-1]+"\n")
                idx=content.find(rhs)
                if idx != -1:
                    content = content[:idx]+content[idx+1:] 
                j+=1
        else: notfind=1

        if notfind==0: a_rules.append(selected_rule) 
    return a_rules

def print_ruleset(app_r:list[tuple[int,Rule]]):
    print("***set of rules***\n")
    for rule in app_r:
        print(f"Agent {rule[0]}: rule[1]")
        print("\n")
    print("***************\n")

def step(colony:Colony,selset:list[tuple[int,Rule]]):
    content = colony.get_content()
    agent_content = colony.get_contents_agents()
    b_rules = selset
    a_rules = colony.find_applicable_rules() 
    #print("applicable rules:")
    #print_ruleset(a_rules)
    #print("selected rules:")
    #print_ruleset(b_rules)
    
    for rule in b_rules:
        #print("Agent "+str(rule[0])+": "+rule[1].print_rule())
        j=0
        while (j<math.floor(rule[1].get_RAI())):
            agent_content[rule[0]-1]=replace(agent_content[rule[0]-1],rule[1].get_lhs(),rule[1].get_rhs())
            colony.agents[rule[0]-1].content=agent_content[rule[0]-1]
            if rule[1].get_type=="com":
                content=replace(content,rule[1].get_rhs(),rule[1].get_lhs())
                colony.content=content
            j+=1
    
    for agent in colony.agents:
         h_rule:tuple[int,Rule]
         x:Rule
         for x in agent.rules:
            h_rule=[agent.agent_number,x] # type: ignore
            #print("h_rule: "+str(agent.agent_number)+", "+x.print_rule())
            #print(h_rule in b_rules)
            if h_rule in b_rules:
                #print("rule "+x.print_rule()+" is in b set")
                x.change_RAI(colony.get_opplus(),colony.get_numplus())
            elif h_rule not in a_rules:
                #print("rule "+x.print_rule()+" is not in a set")
                x.change_RAI(colony.get_opminus(),colony.get_numminus())

def get_res(colony:Colony):
    what=colony.get_fin_object()
    where = int(colony.get_res_area())
    how = colony.get_res_mode()
    
    if what=="*":
        if where != 0:
            return colony.agents[where-1].content
        else: return colony.content
    else:
        if where != 0:
            return colony.agents[where-1].content.count(what)
        else: return colony.content.count(what)

def computation(colony:Colony,n_step:int):
    what=colony.get_fin_object()
    where = int(colony.get_res_area())
    how = colony.get_res_mode()
    stop=0
    #print("fin_opt:("+str(where)+", "+what+", "+how+")")
    if (how=="emr"): result=list()
    elif (what=="*"): result=str()
    else: result=0

    app_set=colony.find_applicable_rules()
    if (how=="hr") and (len(app_set)==0):
        result=get_res(colony)
    if how=="emr":
        result.append(get_res(colony)) # type: ignore
    if how=="epr":
        result += get_res(colony) # type: ignore
    
    print("Step 0: "+colony.get_config())
    steps=1
         
    while (len(app_set)>0) and ((steps<=n_step)or((n_step==0)and(stop==0))):
         sel_set=random_max_set_rules(colony,app_set)
         step(colony,sel_set)
         print("Step "+str(steps)+": "+colony.get_config())
    
         if (steps % step_period) == 0:
            print("Computation run for "+str(steps)+" steps. ")
            if not pressed_y(): stop=1 
         steps +=1
         app_set=colony.find_applicable_rules()
         if (how=="hr") and (len(app_set)==0):
             result=get_res(colony)
         if how=="emr":
             result.append(get_res(colony)) # type: ignore
         if how=="epr":
            result += get_res(colony) # type: ignore
    
    return result

def read_colony_from_file(file: str) -> Colony:
    with open(file, 'r', encoding='utf-8') as f:
        rows = [r.strip() for r in f if r.strip() and not r.startswith('#')]
    
    alph=rows[0].split()
    print(alph)
    
    env_chr=check_env(rows[1],alph)

    econtent=check_content(rows[2],alph)
    #print("env content is: "+econtent) # type: ignore
    if rows[3]!="UPDATE": 
        print("Error UPDATE")
        exit # type: ignore
    opt = rows[4].split()
    opplus=check_op(opt[0])
    opminus=check_op(opt[2])
    numplus=check_float(float(opt[1]))
    numminus=check_float(float(opt[3]))
    if rows[5]!="FIN": 
        print("Error FIN")
        exit # type: ignore
    fin_opt=list()
    region=int(rows[6])
    fin_opt.append(region)
    if rows[7]=="":fobj="*"
    else:
        fobj=check_env(rows[7],alph)
    fin_opt.append(fobj)
    rmode=check_rmode(rows[8])
    fin_opt.append(rmode)
    #print(fin_opt)


    agents=list()
    rules=list()
    help=list()
    i=9
    first=1
    while(i<len(rows)):
        #print("i="+str(i))
        if(rows[i]=="AGENT"):
            if first==1 : 
                agents=list()
                first=0
            else:
                agent=Agent(content,rules) # type: ignore
                #print("New agent: "+agent.print_agent())
                agents.append(agent)
            i+=1
            #print("i="+str(i))
            content=check_content(rows[i],alph)
            #print("agent content:"+content) # type: ignore
            rules=list()
            i+=1
        else:
            #print("i="+str(i))
            #print(rows[i])
            help=rows[i].split(" ")
            #print(help)
            #for z in help: print(z)
            #print("***************")
            type=check_type(help[0])
            lhs=check_char(help[1],alph)
            rhs=check_char(help[2],alph)
            RAI=check_float(float(help[3]))
            #print("rai="+str(RAI)+", lhs="+str(lhs)+", rhs="+str(rhs)+", type="+str(type)) # type: ignore
            #print(RAI!=0 and lhs!=0 and rhs!=0 and type!=0)
            if RAI!=0 and lhs!=0 and rhs!=0 and type!=0:
                rule=Rule(type,lhs,rhs,RAI)
                #print("new rule:"+rule.print_rule())
                rules.append(rule)
            else: return 0 # type: ignore
            i+=1
    
    agent=Agent(content,rules) # type: ignore
        #for mrule in rules: print(mrule.print_rule())
    #print(agent.print_agent())
    agents.append(agent)
    print("import finished")
    return Colony(alph,env_chr,econtent,agents,opplus,numplus,opminus,numminus,fin_opt) # type: ignore




