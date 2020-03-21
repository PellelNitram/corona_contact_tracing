# Generated with SMOP  0.41
from libsmop import *
# InitializeDiffusionRates.m

    
@function
def InitializeDiffusionRates(numberOfAgents=None,*args,**kwargs):
    varargin = InitializeDiffusionRates.varargin
    nargin = InitializeDiffusionRates.nargin

    
    p=6
# InitializeDiffusionRates.m:3
    xmin=0
# InitializeDiffusionRates.m:4
    xmax=1
# InitializeDiffusionRates.m:5
    diffusionRates=xmin + dot((xmax - xmin),sum(rand(numberOfAgents,p),2)) / p
# InitializeDiffusionRates.m:6
    return diffusionRates
    
if __name__ == '__main__':
    pass
    