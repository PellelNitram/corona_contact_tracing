function [grid, locations] = PerformeSteps(numberOfAgents, locations, gridSize, diffusionRates)
%
grid = cell(gridSize);
for i = 1:numberOfAgents
   r = rand;
   loc = locations(i,:);
   if r < diffusionRates(i)
     while loc == locations(i,:)
         direction = randi(4);
         if direction == 1
             loc(1) = min(max(1,loc(1)+1),gridSize);
         elseif direction == 2
             loc(1) = min(max(1,loc(1)-1),gridSize);
         elseif direction == 3
             loc(2) = min(max(1,loc(2)+1),gridSize);
         elseif direction == 4
             loc(2) = min(max(1,loc(2)-1),gridSize);
         end
     end
     locations(i,:) = loc;
   end
   grid{loc(1),loc(2)} = [grid{loc(1),loc(2)}, i];
end
end

