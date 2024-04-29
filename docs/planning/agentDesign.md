# Agent design

## Environment

When designing an AI agent for playing Tetris, it's essential to understand the task environment's properties. Here's a breakdown of these properties according to common AI environment classifications:

### Observability (Fully Observable vs. Partially Observable)

**Fully Observable:** In Tetris, the AI can see the entire game board at all times, including the positions and shapes of all placed pieces. It also knows the current piece and usually the next piece(s) to come. Therefore, Tetris is considered a fully observable environment.

### Determinism (Deterministic vs. Stochastic)

**Deterministic**
The environment in Tetris is deterministic because the next state of the environment is completely determined by the current state and the action executed by the agent. There is no randomness in how the pieces respond to control inputs; however, the sequence of the Tetris pieces themselves can introduce some level of unpredictability if the sequence generation is not known in advance, yet the piece manipulation is deterministic.

### Episodic vs. Sequential

**Sequential:**
Tetris is sequential because the decisions an agent makes depend on the previous actions, and these decisions accumulate over time to affect the final outcome. Each move affects future opportunities and challenges.

### Static vs. Dynamic

**Semi-Dynamic:**
While the game board itself does not change while the agent is making a decision (the timer stops if the piece is not moved), the game introduces new pieces continually, which requires dynamic planning and response. Therefore, it's static during decision-making but dynamic overall because the game progresses with the addition of new pieces.

### Discrete vs. Continuous

**Discrete:** Both the time in which decisions are made and the actions available (e.g., moving pieces left, right, rotating them, or dropping them) are discrete. The game operates in steps defined by piece movements and placements.

### Single-agent vs. Multi-agent

**Single-agent:** Although some versions of Tetris feature competitive play against other players, the standard environment for Tetris is a single-agent setting where the AI competes against the game environment itself, not against other agents.
Understanding these properties can significantly influence how you design your AI agent, from the decision-making algorithms used (like heuristic functions in deterministic environments) to handling the unpredictability of piece sequence and managing the game's progression.

## Agent types

Here are some suggested agent types for playing Tetris:

- **Random Agent**: Makes random moves without any strategy.
- **Heuristic Agent**: Uses a set of predefined rules or heuristics to evaluate the game state and make decisions. Usually makes the greedy choice based on the current state.
- **Search-based Agent**: Uses search algorithms like iterative deepening, or Monte Carlo Tree Search to explore possible future states and make decisions based on the search results.
- **Reinforcement Learning Agent**: Learns to play Tetris through trial and error, adjusting its strategy based on rewards and penalties received during gameplay.
- Genetic Algorithm Agent: Uses genetic algorithms to evolve a population of agents over time, selecting the best-performing agents for reproduction and mutation.

## Thoughts

When doing search based agents it is worth to experiment with giving it foresight into several moves ahead to see if it can make better decisions. And maybe try different reward distributions to see if it can reliebly set up for tetrises.
