*This project has been created as part of the 42 curriculum by trakotoz.*

# Fly-in: Drones are interesting.


## Description

**Fly-in** is a cooperative **multi-drone pathfinding simulator**. Given a map made
of *zones* (hubs) connected by *links*, and a number of drones stationed at a start
zone, the goal is to route every drone to the end zone **as fast as possible and
without conflicts**: no two drones may occupy the same zone or the same link at the
same time (unless the zone/link's declared capacity allows it).

Concretely, the project:

- parses a custom map-description text format into a validated domain model
  (zones, links/connections, zone types such as `normal` / `blocked` / `restricted`
  / `priority`, and per-zone/per-link drone capacity),
- builds a graph from that map,
- computes, for every drone, a conflict-free path through **space and time** using a
  prioritized multi-agent pathfinding algorithm,
- writes a turn-by-turn textual report of the solution,
- and, optionally, **replays the solution visually** in a 2D pygame window (zones,
  links, animated drones, live dashboard).


## Instructions

### Requirements:
Before running the project, make sure the following dependencies are installed:

- Python 3.10 or later
- `make` (optional)
- `uv` for better management (optional but recommanded)

All project dependencies is managed by `pyproject.toml`.

### Installation:

#### Manual execution:
Using `uv` is the recommanded way to install and run the project.

```bash
uv sync                 # Install and synchronize the project dependencies
uv run python -m fly_in    # Run the Application
```

If using pip:
```bash
pip install -e .
```

> Supported Flags:
- `-i`/ `--input`: Path to a map file to simulate.
- `-o`/ `--output`: File to write the output file. (default to `logs/simulation.log`)
- `-b`/ `--benchmark`: File to write benchmark result. (default to `logs/benchmark.log`)
- `-v`/ `--visual`: Turn visual mode on.


#### Makefile:
A `Makefile` is provided at the root of the repository to simplity common tasks.

```bash
make install             # Installing all dependencies
make run                 # Run the application
make run_visual          # Run the application
make help                # Display avaliable commands.
```

> `Note`: Additional command-line arguments can be passed through the `ARGS` Makefile variable.

### Example Usage:

#### Eample Map:
```
nb_drones : 4


start_hub: a 0 0
end_hub: b 1 1
hub: c 0 -1

connection: a-c
connection: c-b
```

#### Running using the example map:
```bash
uv run python -m fly_in -i example_map.txt
uv run python -m fly_in -i example_map.txt -v # For visual mode
```

#### Output:
```
D1-c
D1-b D2-c
D2-b D3-c
D3-b D4-c
D4-b

Total turn: 5 
```

## Algorithm choices & implementation strategy

### Domain & graph

The map is parsed into an immutable [pydantic](https://docs.pydantic.dev/) domain
model (`Zone`, `Connection`, `Map`) that validates itself on construction (e.g. no
self-loop connections, no blocked start/end hub, no duplicate zone names). A `Graph`
wraps the `Map` as an adjacency list and exposes neighbor lookup, per-zone-type
travel weight, and node/link capacity.

### Solver: Prioritized Cooperative Space-Time A*

Each drone is planned **one at a time, in priority order**, using a **Space-Time
A\*** search: a node in the search space is not just a zone but a `(zone, time)`
pair, so the algorithm reasons about *when* a drone is somewhere, not just *where*.
Once a drone's path is found, its occupancy of every zone and link over time is
**reserved** in a shared `WorldState` (a reservation table), so the next drone's
search automatically avoids colliding with already-planned drones. A Dijkstra
shortest-path pass (ignoring time) is used as the admissible heuristic that guides
each A* search toward the goal.

Zone types affect the search directly: `restricted` zones cost more to cross,
`priority` zones are preferred (see below), and `blocked` zones are simply
unreachable.

### Why prioritized cooperative A*, and not CBS or a Time-Expanded Graph

Two other approaches were explored and discarded:

- **Conflict-Based Search (CBS)** assumes each agent has its own start/goal; here,
  every drone shares the *same* start and goal, which breaks CBS's usual conflict
  tree and made it a poor fit for this problem.
- **Time-Expanded Graph** (unrolling the whole graph across every timestep and
  solving as a flow/graph problem) gives clean guarantees but its memory and
  runtime cost grew too fast for the map sizes and turn limits of this project.

Prioritized cooperative Space-Time A* was the pragmatic middle ground: correct
(no two drones ever collide), fast enough on every provided map, and simple enough
to reason about and implement for this project.

### Complexity

Time complexity is not perfectly nailed down (this is called out explicitly, not
glossed over): each individual Space-Time A* search is roughly `O((V·T) log(V·T))`
in the size of the explored `(zone, time)` state space, and the whole solve is that,
repeated per drone. In practice, across the provided maps, observed behavior sits
somewhere between `O(n)` and `O(n log n)` in the number of drones — see the
`logs/benchmark.log` output produced by `--benchmark` for actual timing/memory
numbers per map.

### Priority zones and the minimal-turn result

The bonus objective (reaching the goal in 43 turns) was achieved, and the solver
finds a near-minimal turn count on almost every provided map. This comes from how
`priority` zones are weighted during the search: drones are steered to prefer
routes through priority zones, which — combined with reserving reservations
zone-by-drone in priority order — reduces the contention/detours that would
otherwise inflate the total number of turns.

## Documentation of the visual representation

The `--visual` flag opens a 2D [pygame](https://www.pygame.org/) window that
replays the computed solution:

- **Zones** are drawn as colored circles (custom color if set in the map file,
  otherwise a default white color), with a small inner marker colored by zone type (normal /
  priority / restricted / blocked), so the map's structure and constraints are
  visible at a glance.
- **Links** are drawn as lines between connected zones.
- **Drones** are animated sprites that move smoothly between zones — interpolated
  frame-by-frame rather than snapping turn-to-turn — so the flow of traffic across
  the map is actually readable instead of a discrete slideshow.
- **Hover tooltips**: hovering the mouse over a zone or link shows its details
  (name/type/capacity for zones, linked zones/capacity for links).
- **Live dashboard**: current turn, number of drones delivered so far, and
  play/pause state are always shown on screen.
- **Playback controls**: `SPACE` play/pause, `R` restart, arrow keys pan the camera.
- **Camera**: pans over the map so larger maps remain fully explorable.

This turns an otherwise abstract list of `(drone, zone, time)` triples into a
readable, at-a-glance simulation of drone traffic, and makes it easy to spot
bottlenecks, priority routing, and capacity effects visually.

## Learning journey

This project meant building a working understanding of graph theory and
multi-agent pathfinding essentially from scratch:

1. **Path**: graph theory → graph traversal (BFS, DFS) → shortest path (Dijkstra,
   A*) → Multi-Agent Path Finding (MAPF) → Space-Time A* → Conflict-Based Search
   (CBS) → Time-Expanded Graphs. CBS was implemented first, then dropped once it
   became clear it doesn't fit a problem where every agent shares the same start
   and goal. A Time-Expanded Graph was attempted next and worked, but its
   time/memory/hardware cost was too high given the project's constraints. The
   project ultimately settled on **Prioritized Cooperative Space-Time A\***, using
   a reservation table, as described above.
2. **Visuals**: the initial plan was PyOpenGL + GLFW, but the rendering learning
   curve cost too much time for too little payoff without prior graphics
   experience, so the project switched to **pygame** instead.
3. **Complexity**: the exact time complexity of the solver isn't fully pinned down;
   observed behavior sits somewhere between `O(n)` and `O(n log n)` in practice
   (see above).
4. **Result**: the bonus objective (43 turns) was reached, and priority-zone
   weighting lets the solver find a close-to-minimal turn count on nearly every
   provided map.

## Resources

- A* Documentation: https://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
- Flow Network in Graph Theory: https://en.wikipedia.org/wiki/Flow_network
- CBS: https://ktiml.mff.cuni.cz/~bartak/ui_seminar/talks/2022LS/Conflict%20Based%20Search.pdf
- Time expanded graph: http://strategic.mit.edu/docs/2_16_SE_10_2_TDN.pdf
- Pygame: https://www.pygame.org/docs/
- GLFW Documentation: https://www.glfw.org/docs/latest/
- OpenGL Kiwi Documentation: https://wikis.khronos.org/opengl/Main_Page
### AI usage

AI was use for this project, especially on my learning journey to help me understand
concepts, precise point and give me lesson on graph theory, MAPF

- **ChatGPT**: use as a guide during the project's development, especially regarding the roadmap
- **ClaudeAI**: use for generating lesson, grammar corrector on my docstrings and README.

---

<div align="center">

### Fly-in

created by [trakotoz](mailto:trakotoz@student.42antananarivo.mg)

42 antananarivo

<img src="./src/fly_in/resources/images/42_tana_logo.png" width="120" />

</div>

