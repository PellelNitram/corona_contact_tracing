clear;
close all;
%figure('units','normalized','outerposition',[0 0 1 1])

infectionRate = 0.01;
diffusionRate = 0.8;
len = 25;
beta = linspace(0.1,1,len);
kays = logspace(0,3,len);
[BETA,KAYS] = meshgrid(beta,kays);
proportionOfRecovered = zeros(len);

runsPerSetting = 5;

for i = 1:len
    for l = 1:len
        tempProportion = zeros(runsPerSetting,1);
        gamma = beta(i)/kays(l);
        for m = 1:runsPerSetting
            tempProportion(m) = DiseaseFunction(infectionRate, beta(i), gamma, diffusionRate);
        end
        proportionOfRecovered(i,l) = mean(tempProportion); 
    end
end

h=gca;
surf(KAYS,BETA,proportionOfRecovered.')
set(h,'xscale','log')
xlabel('$k(\beta/\gamma)$','Interpreter','latex', 'FontSize', 28)
ylabel('$\beta$','Interpreter','latex', 'FontSize', 28)
zlabel('$R_\infty$','Interpreter','latex', 'FontSize', 28)


