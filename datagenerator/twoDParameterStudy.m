clear;
close all;
figure('units','normalized','outerposition',[0 0 1 1])

% fix beta
betas = [0.1 0.8];
infectionRate = 0.01;
diffusionRate = 0.8;
len = 25;
kays = logspace(0,3,len);
proportionOfRecovered = zeros(len, 2);

runsPerSetting = 5;

for k = 1:length(betas)
    beta = betas(k);
    gammas = betas(k)./kays;
    for t = 1:len
        gamma = gammas(t);
        tempProportion = zeros(runsPerSetting,1);
        for i = 1:runsPerSetting
            tempProportion(i) = DiseaseFunction(infectionRate, beta, gamma, diffusionRate);
        end
        proportionOfRecovered(t,k) = mean(tempProportion); 
    end
end

hold on
plot(kays, proportionOfRecovered(:,1),'LineWidth',3.0)
plot(kays, proportionOfRecovered(:,2),'r','LineWidth',3.0)
ylabel('$R_\infty$','Interpreter','latex', 'FontSize', 28)
title('Parameter Study', 'FontSize', 28)
legend({'$\beta=0.1$','$\beta=0.8$'},'Interpreter','latex', 'FontSize', 20)
xlabel('$\beta/\gamma$','Interpreter','latex', 'FontSize', 28)
set(gca, 'XScale', 'log')
axis([0 1000 0 1.01]);