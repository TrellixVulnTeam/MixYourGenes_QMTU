

#from .nucleus import INHERITANCE

#S_INHERITANCE={"dominance":{1.0:["A.A","A.a"],0.0:["a.a"]},"intermedier":{2.0:["A.A;A.A"],1.5:["A.A;A.a"],1.0:["A.a;A.a","A.A;a.a"],0.5:["A.a;a.a"],0.0:["a.a;a.a"]}}



def DoesMemberHave(list,member):
    if member in list:
        return True
    else:
        return False

class Child():
    def __init__(self,boy,girl):
        self.boy=boy
        self.girl=girl


    def get_max(self,which):
        if which:
            max_p=max(list(self.boy.values()))
            for i in self.boy.keys():
                if self.boy[i]==max_p:
                    gt=i
        else:
            max_p=max(list(self.boy.values()))
            for i in self.boy.keys():
                if self.boy[i]==max_p:
                    gt=i
        return {max_p:gt}

    def get_all(self):
        pass

class Children():
    pass

class Gene():
    def __init__(self,inheritance,name,is_X_linked):
        self.inheritance=inheritance
        self.name=name
        self.genotype=0
        self.possibility=0
        self.is_X_linked=is_X_linked

    def recombination(self,other,self_sex):
        if isinstance(other,Gene):
            if self.is_X_linked:
                if self.inheritance=="dominance":
                    return self.dom_x_linked_recombination(other,self_sex)
                elif self.inheritance=="recessive":
                    return self.rec_x_linked_recombination(other,self_sex)
            else:
                if self.inheritance=="dominance":
                    return self.dom_recombination(other)
                elif self.inheritance=="recessive":
                    return self.rec_recombination(other)
        elif other:
            if self.is_X_linked:
                if self.inheritance=="recessive":
                    return Child({1:0,0:1},{0:1,1:0,0.5:0})
                elif self.inheritance=="dominance":
                    return Child({1:1,0:0},{0.5:(2/3),1:(1/3),0:0})
            else:
                if self.inheritance=="recessive":
                    return {1:0,0:1,0.5:0}
                elif self.inheritance=="dominance":
                    return {1:(1/3),0.5:(2/3),0:0}
        else:
            if self.is_X_linked:
                if self.inheritance=="recessive":
                    return Child({1:1,0:0},{0.5:(2/3),1:(1/3),1:0})
                elif self.inheritance=="dominance":
                    return Child({0:1,1:0},{0:1,0.5:0,1:0})
            else:
                if self.inheritance=="recessive":
                    return {0.5:(2/3),0:0,1:(1/3)}
                elif self.inheritance=="dominance":
                    return {0:1,1:0,0.5:0}
    def dom_recombination(self,other):
        dom=self.genotype+other.genotype
        if dom==2:
            return {1:1,0.5:0,0:0}
        elif dom==1.5:
            return {0.5:0.75,1:0.25,0:0}
        elif dom==1:
            return {0.5:1,0:0,1:0}
        elif dom==0.5:
            return {0.5:1,0:0,1:0}
        elif dom==0:
            return {0.5:0,0:0,1:0}

    def rec_recombination(self,other):
        rec=self.genotype+other.genotype
        if rec==1:
            return {0.5:0.75,1:0,0:0.25}
        elif rec==0.5:
            return {0.5:0.5,1:0,0:0.5}
        elif rec==0:
            return {0:1,1:0}
        else:
            return {0.5:0,0:0,1:0}


    def rec_x_linked_recombination(self,other,self_sex):
        rec=self.genotype+other.genotype
        if rec==2:
            return Child({1:1,0:0},{1:1,0.5:0,0:0})
        elif rec==1.5:
            return Child({1:0.5,0:0.5},{1:0.5,0.5:0.5,0:0})
        elif rec==1:
            if self.genotype>other.genotype:
                if self_sex:
                    return Child({0:1,1:0},{0.5:1,1:0,0:0})
                else:
                    return Child({0:0,1:1},{0.5:1,1:0,0:0})
        elif rec==0.5:
            return Child({0:0.5,1:0.5},{0.5:0.5,0:0.5,1:0})
        elif rec==0.0:
            return Child({0:1,1:0},{0:1,1:0,0.5:0})
    def dom_x_linked_recombination(self,other,self_sex):
        dom=self.genotype+other.genotype
        if dom==2:
            return Child({1:1,0:0},{1:1,0.5:0,0:0})
        elif dom==1.5:
            return Child({1:0.5,0:0.5},{1:0.5,0.5:0.5,0:0})
        elif dom==1:
            if self.genotype>other.genotype:
                if self_sex:
                    return Child({0:0,1:1},{0.5:1,1:0,0:0})
                else:
                    return Child({0:0,1:1},{0.5:1,1:0,0:0})
        elif dom==0.5:
            return Child({0:0.5,1:0.5},{0.5:0.5,0:0.5,1:0})
        elif dom==0.0:
            return Child({0:1,1:0},{0:1,1:0,0.5:0})

class Parent():
    def __init__(self,doesHave,desease,sex,ID):
        self.sex=sex
        self.ID=ID
        self.IsGenotypeSet=False
        self.doesHave=doesHave
        self.desease=desease
        self.dad=None
        self.mom=None
        self.child=None

    #def add_dad(self,doesHave,ID):
    def add_dad(self,DAD):
        #self.dad=Parent(doesHave,Gene(self.desease.inheritance,self.desease.name,self.desease.is_X_linked),True,ID)
        self.dad=DAD
        self.dad.child=self
    #def add_mom(self,doesHave,ID):
        #self.mom=Parent(doesHave,Gene(self.desease.inheritance,self.desease.name,self.desease.is_X_linked),False,ID)
    def add_mom(self,MOM):
        self.mom=MOM
        self.mom.child=self

    def set_genotype(self):
        if self.doesHave:
            if self.dad is not None and self.mom is not None:
                self.dad.set_genotype()
                self.mom.set_genotype()
                print(self.mom.ID.user.username)
                print(self.dad.ID.user.username)
                r=self.dad.desease.recombination(self.mom.desease,self.sex)
                print(r)
                if isinstance(r,Child):
                    get_max=r.get_max(self.sex)
                    self.desease.genotype=list(get_max.keys())
                    self.desease.possibility=list(get_max.values())
                else:
                    max_p=max(r.values())
                    for genotype in r.keys():
                        if r[genotype]==max_p:
                            self.desease.genotype=genotype
                    self.desease.possibility=max_p
                return self.desease.genotype
            else:
                r=self.desease.recombination(self.doesHave,self.sex)
                print('Nodadnomom\t',r)
                if isinstance(r,Child):
                    get_max=r.get_max(self.sex)
                    self.desease.genotype=list(get_max.keys())
                    self.desease.possibility=list(get_max.values())
                else:
                    max_p=max(r.values())
                    for genotype in r.keys():
                        if r[genotype]==max_p:
                            self.desease.genotype=genotype
                    self.desease.possibility=max_p
                return self.desease.genotype
        else:
            r=self.desease.recombination(self.doesHave,self.sex)
            if isinstance(r,Child):
                get_max=r.get_max(self.sex)
                self.desease.genotype=list(get_max.keys())
                self.desease.possibility=list(get_max.values())
            else:
                max_p=max(r.values())
                for genotype in r.keys():
                    if r[genotype]==max_p:
                        self.desease.genotype=genotype
                self.desease.possibility=max_p
            return self.desease.genotype

    def add_child(self,other):
        cum=self.desease.recombination(other.desease)
        if isinstance(r,Child):
            get_max=r.get_max(self.sex)
            self.desease.genotype=list(get_max.keys())
            self.desease.possibility=list(get_max.values())
        else:
            max_p=max(r.values())
            for genotype in r.keys():
                if r[genotype]==max_p:
                    self.desease.genotype=genotype
            self.desease.possibility=max_p
        return Children()
