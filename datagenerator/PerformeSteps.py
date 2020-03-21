# Generated with SMOP  0.41
from libsmop import *
# PerformeSteps.m

    
@function
def PerformeSteps(numberOfAgents=None,locations=None,gridSize=None,diffusionRates=None,*args,**kwargs):
    varargin = PerformeSteps.varargin
    nargin = PerformeSteps.nargin

    
    grid=cell(gridSize)
# PerformeSteps.m:3
    for i in arange(1,numberOfAgents).reshape(-1):
        r=copy(rand)
# PerformeSteps.m:5
        loc=locations(i,arange())
# PerformeSteps.m:6
        if r < diffusionRates(i):
            while loc == locations(i,arange()):

                direction=randi(4)
# PerformeSteps.m:9
                if direction == 1:
                    loc[1]=min(max(1,loc(1) + 1),gridSize)
# PerformeSteps.m:11
                else:
                    if direction == 2:
                        loc[1]=min(max(1,loc(1) - 1),gridSize)
# PerformeSteps.m:13
                    else:
                        if direction == 3:
                            loc[2]=min(max(1,loc(2) + 1),gridSize)
# PerformeSteps.m:15
                        else:
                            if direction == 4:
                                loc[2]=min(max(1,loc(2) - 1),gridSize)
# PerformeSteps.m:17

            locations[i,arange()]=loc
# PerformeSteps.m:20
        grid[loc(1),loc(2)]=concat([grid[loc(1),loc(2)],i])
# PerformeSteps.m:22
    
    return grid,locations
    
if __name__ == '__main__':
    pass
    