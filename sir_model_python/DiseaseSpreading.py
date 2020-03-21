import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class Agent:

    def __init__(self, row, col, number):
        self.infected = False
        self.susceptible = True
        self.recovered = False
        self.row = row
        self.col = col
        self.number = number

    def __repr__(self):
        repr_string = str(self.number) + ' (' + str(self.row) + ',' + str(self.col) + ')'
        if self.infected:
            repr_string += ' - Inf'
        elif self.susceptible:
            repr_string += ' - Sus'
        elif self.recovered:
            repr_string += ' - Rec'

        return repr_string

class Cell:

    def __init__(self):
    #    self.agents = []
        self.infected_agents = []
        self.susceptible_agents = []
        self.recovered_agents = []

    def __repr__(self):
        repr_string = '(Inf: ' + str(len(self.infected_agents)) + ' Sus: ' + str(len(self.susceptible_agents)) + ' Rec: ' + str(len(self.recovered_agents)) + ')'
        return repr_string

class DiseaseSpreading:

    def __init__(self, rows, cols, n_agents, infected_radius, infection_prob, recovery_prob, diffusion_rate):
        self.n_agents = n_agents

        self.infection_prob = infection_prob
        self.recovery_prob = recovery_prob
        self.diffusion_rate = diffusion_rate

        centre_row = int(rows / 2)
        centre_col = int(cols / 2)
        self.rows = rows
        self.cols = cols

        self.grid = [[Cell() for j in range(cols)] for i in range(rows)]

        self.infected_agents = []
        self.recovered_agents = []
        self.susceptible_agents = []

        self.agents = [Agent(0, 0, 0) for i in range(n_agents)]

        for i in range(n_agents):
            x = np.random.randint(0, rows)
            y = np.random.randint(0, cols)
            tmp_agent = Agent(x, y, i)
            self.agents[i] = tmp_agent
            self.susceptible_agents.append(tmp_agent)
           # self.grid[x][y].agents.append(tmp_agent)
            self.grid[x][y].susceptible_agents.append(tmp_agent)

        for row in range(rows):
            for col in range(cols):
                dist = np.sqrt(np.square(row - centre_row) + np.square(col - centre_col))
                if dist < infected_radius and len(self.grid[row][col].susceptible_agents) > 0:
                    self.infect(row, col)

        self.n_infected = len(self.infected_agents)
        self.n_susceptible = len(self.susceptible_agents)
        self.n_recovered = len(self.recovered_agents)



    def update_position(self, agent):
        r = np.random.random()

        if r < self.diffusion_rate:
            possible_directions = [1, 2, 3, 4]
            if agent.row == 0:
                possible_directions.remove(2)
            if agent.row == self.rows - 1:
                possible_directions.remove(4)
            if agent.col == 0:
                possible_directions.remove(1)
            if agent.col == self.cols - 1:
                possible_directions.remove(3)

            direction = np.random.choice(possible_directions)
            self.move(agent, direction)

    def move(self, agent, direction):
        old_row = agent.row
        old_col = agent.col

        if direction == 1:  # left
            new_row = old_row
            new_col = old_col - 1
        elif direction == 2:  # up
            new_row = old_row - 1
            new_col = old_col
        elif direction == 3:  # right
            new_row = old_row
            new_col = old_col + 1
        else:                   # down
            new_row = old_row + 1
            new_col = old_col

      #  self.grid[old_row][old_col].agents.remove(agent)
       # self.grid[new_row][new_col].agents.append(agent)

        if agent.infected:
            self.grid[old_row][old_col].infected_agents.remove(agent)
            self.grid[new_row][new_col].infected_agents.append(agent)
        elif agent.susceptible:
            self.grid[old_row][old_col].susceptible_agents.remove(agent)
            self.grid[new_row][new_col].susceptible_agents.append(agent)
        elif agent.recovered:
            self.grid[old_row][old_col].recovered_agents.remove(agent)
            self.grid[new_row][new_col].recovered_agents.append(agent)

        agent.row = new_row
        agent.col = new_col

    def try_infect(self, row, col):
        n_infected_agents = len(self.grid[row][col].infected_agents)
        r = np.random.rand(n_infected_agents, 1)

        if np.any(r < self.infection_prob):
            self.infect(row, col)

    def infect(self, row, col):

        susceptible_agents = self.grid[row][col].susceptible_agents

        for agent in susceptible_agents:
            agent.infected = True
            agent.susceptible = False
            self.susceptible_agents.remove(agent)

        # update grid information
        self.infected_agents.extend(self.grid[row][col].susceptible_agents)

        # update cell information
        self.grid[row][col].infected_agents.extend(self.grid[row][col].susceptible_agents)
        self.grid[row][col].susceptible_agents = []

      #  self.n_infected += 1
      #  self.n_susceptible -= 1

    def try_recover(self, agent):
        r = np.random.random()

        if r < self.recovery_prob:
            self.recover(agent)

    def update_counters(self):
        self.n_infected = len(self.infected_agents)
        self.n_susceptible = len(self.susceptible_agents)
        self.n_recovered = len(self.recovered_agents)

    def recover(self, agent):
        row = agent.row
        col = agent.col

        agent.infected = False
        agent.recovered = True

        # update grid information
        self.infected_agents.remove(agent)
        self.recovered_agents.append(agent)

        # update cell information
        self.grid[row][col].infected_agents.remove(agent)
        self.grid[row][col].recovered_agents.append(agent)

     #   self.n_infected -= 1
      #  self.n_recovered += 1

    def get_plot_data_agents(self):
       # n_infected = len(self.infected_agents)
       # n_susceptible = len(self.susceptible_agents)
       #n_recovered = len(self.recovered_agents)

        x_infected = np.zeros(self.n_infected)
        y_infected = np.zeros(self.n_infected)
        x_susceptible = np.zeros(self.n_susceptible)
        y_susceptible = np.zeros(self.n_susceptible)
        x_recovered = np.zeros(self.n_recovered)
        y_recovered = np.zeros(self.n_recovered)

        counter_infected = 0
        counter_susceptible = 0
        counter_recovered = 0

        for agent in self.agents:
            if agent.infected:
                x_infected[counter_infected] = agent.row
                y_infected[counter_infected] = agent.col
                counter_infected += 1
            elif agent.susceptible:
                x_susceptible[counter_susceptible] = agent.row
                y_susceptible[counter_susceptible] = agent.col
                counter_susceptible += 1
            elif agent.recovered:
                x_recovered[counter_recovered] = agent.row
                y_recovered[counter_recovered] = agent.col
                counter_recovered += 1

        return x_infected, y_infected, x_susceptible, y_susceptible, x_recovered, y_recovered

    def init_agent_plot(self):
        agent_fig = plt.figure(1)
        agent_ax = plt.gca()
        scat_inf = plt.scatter([], [], c='red')
        scat_sus = plt.scatter([], [], c='blue')
        scat_rec = plt.scatter([], [], c='green')
        plt.title('Distribution of agents')
        plt.xlabel('x')
        plt.ylabel('y')
        agent_ax.set_xlim(-1, self.cols)
        agent_ax.set_ylim(self.rows, -1)
        return agent_fig, agent_ax, scat_inf, scat_sus, scat_rec

    def create_animation_agents(self, data_inf, data_sus, data_rec, time_steps, filename):
        agent_fig = plt.figure(3)
        agent_ax = plt.gca()
        scat_inf = plt.scatter([], [], c='red')
        scat_sus = plt.scatter([], [], c='blue')
        scat_rec = plt.scatter([], [], c='green')
        plt.title('Distribution of agents')
        agent_ax.set_xlim(-1, self.cols)
        agent_ax.set_ylim(self.rows, -1)
        agent_ani = animation.FuncAnimation(agent_fig, self.update_agents, frames=time_steps,
                               fargs=(data_inf, data_sus, data_rec, scat_inf, scat_sus, scat_rec))

        gifWriter = animation.ImageMagickFileWriter()
        mp4Writer = animation.FFMpegFileWriter()
        agent_ani.save(filename, writer=gifWriter)

    # def create_animation_stat(self, y_infected_agents, y_susceptible_agents, y_recovered_agents, time_steps):
    #     stat_fig = plt.figure(4)
    #     stat_ax = stat_fig.add_subplot(111)
    #     line_inf, = stat_ax.plot([], [], c='red')
    #     line_sus, = stat_ax.plot([], [], c='blue')
    #     line_rec, = stat_ax.plot([], [], c='green')
    #     plt.title('Distribution of agent status')
    #     plt.xlabel('x')
    #     plt.ylabel('y')
    #     agent_ax.set_xlim(-1, self.cols)
    #     agent_ax.set_ylim(self.rows, -1)
    #     agent_ani = animation.FuncAnimation(agent_fig, self.update_stat_plot, frames=time_steps,
    #                            fargs=(y_infected_agents, y_susceptible_agents, y_recovered_agents, line_inf, line_sus, line_rec))
    #
    #     gifWriter = animation.ImageMagickFileWriter()
    #     mp4Writer = animation.FFMpegFileWriter()
    #     agent_ani.save('location.mp4', writer=gifWriter)

    # def update_stat(self, i, y_infected_agents, y_susceptible_agents, y_recovered_agents, line_inf, line_sus, line_rec):
    #     plt.pause(0.01)
    #
    #     scat_inf.set_offsets(data_inf[i])
    #     scat_sus.set_offsets(data_sus[i])
    #     scat_rec.set_offsets(data_rec[i])

    def update_agents(self, i, data_inf, data_sus, data_rec, scat_inf, scat_sus, scat_rec):
       # plt.pause(0.1)

        scat_inf.set_offsets(data_inf[i])
        scat_sus.set_offsets(data_sus[i])
        scat_rec.set_offsets(data_rec[i])

    def plot_agents(self, data_inf, data_sus, data_rec, scat_inf, scat_sus, scat_rec):
        plt.pause(0.01)

        scat_inf.set_offsets(data_inf)
        scat_sus.set_offsets(data_sus)
        scat_rec.set_offsets(data_rec)

        return scat_inf, scat_sus, scat_rec

    def init_plot(self, time_steps):
        stat_fig = plt.figure(2)
        stat_ax = stat_fig.add_subplot(111)
        line_inf, = stat_ax.plot([], [], c='red', label='infected')
        line_sus, = stat_ax.plot([], [], c='blue', label='susceptible')
        line_rec, = stat_ax.plot([], [], c='green', label='recovered')
        plt.title('d = ' + str(self.diffusion_rate) + ', beta = ' + str(self.infection_prob) + ' , gamma = ' + str(self.recovery_prob))
        plt.xlabel('time step')
        plt.ylabel('Number of agents')

        plt.legend(loc=1)
        stat_ax.set_ylim(-1, self.n_agents)
        stat_ax.set_xlim(-1, time_steps)

        return stat_fig, stat_ax, line_inf, line_sus, line_rec

    def update_stat_plot(self, current_time_step, y_infected_agents, y_susceptible_agents, y_recovered_agents, line_inf, line_sus, line_rec):
        x_values = np.linspace(0, current_time_step, current_time_step + 1)

        line_inf.set_data(x_values, y_infected_agents)
        line_sus.set_data(x_values, y_susceptible_agents)
        line_rec.set_data(x_values, y_recovered_agents)
        plt.draw()
        plt.pause(0.01)
        return line_inf, line_sus, line_rec


n_agents = 1000
rows = 100
cols = 100
time_steps = 2000
infected_radius = 6
filename = 'limitedRun.gif'

n_avg_times = 7
n_runs_beta = 25
n_runs_gamma = 25
recovered_rate = [None] * n_runs_gamma

k = np.logspace(1, 4, n_runs_gamma)
infection_prob = np.linspace(0.1, 0.9, n_runs_beta)

#recovery_prob = np.logspace(-1, -4, n_runs_gamma)
diffusion_rate = 0.8
#
# fig = plt.figure()
# ax = plt.gca()
# ax.set_xscale('log')
# plt.xlabel('k')
# plt.ylabel('rate of recovered agents')

for j_beta in range(n_runs_beta):
    print('j_beta ' + str(j_beta) + ' : ' + str(infection_prob))
    recovery_prob = infection_prob[j_beta] / k
    for m_gamma in range(n_runs_gamma):
        print('m_gamma ' + str(m_gamma) + ' : ' + str(recovery_prob[m_gamma]))
        n_recovered = 0

        #start_time = time.time()

        for k in range(n_avg_times):
            ds = DiseaseSpreading(rows, cols, n_agents, infected_radius, infection_prob[j_beta], recovery_prob[m_gamma], diffusion_rate)

            # y_infected_agents = [None] * (time_steps + 1)
            # y_susceptible_agents = [None] * (time_steps + 1)
            # y_recovered_agents = [None] * (time_steps + 1)
            # y_infected_agents[0] = ds.n_infected
            # y_susceptible_agents[0] = ds.n_susceptible
            # y_recovered_agents[0] = ds.n_recovered
            #
            # x_infected, y_infected, x_susceptible, y_susceptible, x_recovered, y_recovered = ds.get_plot_data_agents()
            # tot_data_inf = [None] * (time_steps + 1)
            # tot_data_sus = [None] * (time_steps + 1)
            # tot_data_rec = [None] * (time_steps + 1)
            # tot_data_inf[0] = np.column_stack((x_infected, y_infected))
            # tot_data_sus[0] = np.column_stack((x_susceptible, y_susceptible))
            # tot_data_rec[0] = np.column_stack((x_recovered, y_recovered))

            #agent_fig, agent_ax, scat_inf, scat_sus, scat_rec = ds.init_agent_plot()
            #stat_fig, stat_ax, line_inf, line_sus, line_rec = ds.init_plot(time_steps)

            for i in range(time_steps):
                for agent in ds.agents:
                    ds.update_position(agent)

              #  grid_start_time = time.time()

                for agent in ds.infected_agents:
                    cell = ds.grid[agent.row][agent.col]

                    if len(cell.infected_agents) > 0:
                        infected_agents = cell.infected_agents

                        if len(cell.susceptible_agents) > 0:
                            # for infected_agent in infected_agents:
                            #     susceptible_agents = ds.grid[row][col].susceptible_agents
                            #     for susceptible_agent in susceptible_agents:
                            #         ds.try_infect(susceptible_agent)
                            ds.try_infect(cell.infected_agents[0].row, cell.infected_agents[0].col)
                        for infected_agent in infected_agents:
                            ds.try_recover(infected_agent)

                # for row in range(rows):
                #     for col in range(cols):
                # for row in ds.grid:
                #     for cell in row:

                #         if len(cell.infected_agents) > 0:
                #             infected_agents = cell.infected_agents
                #
                #             if len(cell.susceptible_agents) > 0:
                #                 # for infected_agent in infected_agents:
                #                 #     susceptible_agents = ds.grid[row][col].susceptible_agents
                #                 #     for susceptible_agent in susceptible_agents:
                #                 #         ds.try_infect(susceptible_agent)
                #                 ds.try_infect(cell.agents[0].row, cell.agents[0].col)
                #             for infected_agent in infected_agents:
                #                 ds.try_recover(infected_agent)

                        # if len(ds.grid[row][col].infected_agents) > 0:
                        #     infected_agents = ds.grid[row][col].infected_agents
                        #
                        #     if len(ds.grid[row][col].susceptible_agents) > 0:
                        #         # for infected_agent in infected_agents:
                        #         #     susceptible_agents = ds.grid[row][col].susceptible_agents
                        #         #     for susceptible_agent in susceptible_agents:
                        #         #         ds.try_infect(susceptible_agent)
                        #         ds.try_infect(row, col)
                        #     for infected_agent in infected_agents:
                        #         ds.try_recover(infected_agent)


              #  grid_end_time = time.time()
             #   print('grid')
            #    print(grid_end_time-grid_start_time)
                ds.update_counters()

                # y_infected_agents[i+1] = ds.n_infected
                # y_susceptible_agents[i+1] = ds.n_susceptible
                # y_recovered_agents[i+1] = ds.n_recovered
                #
                # x_infected, y_infected, x_susceptible, y_susceptible, x_recovered, y_recovered = ds.get_plot_data_agents()
                #
                # data_inf = np.column_stack((x_infected, y_infected))
                # data_sus = np.column_stack((x_susceptible, y_susceptible))
                # data_rec = np.column_stack((x_recovered, y_recovered))
                # #
                # tot_data_inf[i+1] = np.column_stack((x_infected, y_infected))
                # tot_data_sus[i+1] = np.column_stack((x_susceptible, y_susceptible))
                # tot_data_rec[i+1] = np.column_stack((x_recovered, y_recovered))

                if len(ds.infected_agents) == 0:
                    break
                elif len(ds.susceptible_agents) == 0:
                    ds.n_recovered = n_agents
                    break

            # print('gamma' + str(m_gamma))
            # print('beta' + str(j_beta))
            # print(ds.n_recovered)
            n_recovered += ds.n_recovered/n_agents
            print(ds.n_recovered / n_agents)
               # ds.plot_agents(data_inf, data_sus, data_rec, scat_inf, scat_sus, scat_rec)
            # end_time = time.time()
            # print('done')
            # print(end_time-start_time)

        recovered_rate[m_gamma] = n_recovered / n_avg_times

    k = infection_prob[j_beta] / recovery_prob
    print(k)
    print(recovered_rate)
    beta_data = [infection_prob[j_beta]] * n_runs_gamma
    data = np.column_stack((k, recovered_rate, beta_data, recovery_prob))

    np.save('dataTis2' + str(j_beta) + '.npy', data)

  #  ax.plot(k, recovered_rate)
  #  plt.draw()
   # plt.pause(0.01)

#plt.savefig('Fin3.2.png')
#plt.show()

          #  ds.update_stat_plot(i, y_infected_agents, y_susceptible_agents, y_recovered_agents, line_inf, line_sus, line_rec)

    #ds.update_stat_plot(time_steps, y_infected_agents, y_susceptible_agents, y_recovered_agents, line_inf, line_sus, line_rec)

    #ds.create_animation_agents(tot_data_inf, tot_data_sus, tot_data_rec, time_steps, filename)
    #ds.create_animation_stat(y_infected_agents, y_susceptible_agents, y_recovered_agents, time_steps)



    #plt.show()

