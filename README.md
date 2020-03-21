# Corona Contact Tracing

Package for evaluating Corona traces from people's mobility data.

This package aims to do the following things

- Simulate realistic movement of agents and their health status using a SIR model.
- Effectively identify contact persons based on time stamped location histories
- Identify contact persons with many secondary contact persons to prioritize them during testing.

This should serve as an early detection of super spreading events.

It uses an existing stochastic SIR simulation to generate data sets.
This simulation has full access to all health states.
These data sets are presented in a csv table, its headers are described in the repo.
The health status is only partially observed through tests.
Next pairwise distances are evaluated and multiple informations derived from this information.
The first trivial information is the contact persons of infected persons.
The second information derived is the number of secondary contact persons of contact persons.
This is valuable to know, as some of the primary contact persons might by super spreaders and thus should get prioritized testing.

These informations should be utilized to slow down the pandemic.

This package was created within the #WirVsVirus Hackathon of the German government and is Work in Progress!

## Install

- set up conda env with environment.yml

## License

- tbd
