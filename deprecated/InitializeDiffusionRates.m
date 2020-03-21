function [diffusionRates] = InitializeDiffusionRates(numberOfAgents)
    
    p = 6;
    xmin=0;
    xmax=1;
    diffusionRates = xmin + (xmax - xmin)*sum(rand(numberOfAgents,p),2)/p;
    
    
end

