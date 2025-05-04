> XPilot-Inspired Python Game – Phase 1

This repository contains **Phase 1** of a 2D space shooter game inspired by the classic XPilot, developed in Python using **Pygame** and **Pymunk**. The goal is to simulate a physics-based environment where autonomous agents can navigate and interact with the world through a REST API.

> Features implemented in Phase 1

- Single agent controlled via API (FastAPI)
- Physics-based movement: thrust, rotation, and collisions
- Grid-based map with static walls
- Health system:
  - Damage from collisions
  - Healing pickups scattered in the arena
- On-screen HUD with health bar, score, and game over screen
- Radar-like sensors that detect distances to nearby walls
- Dummy client bot that sends simple actions to the API

> Technologies used

- Python 3.10+
- Pygame
- Pymunk
- FastAPI
- Uvicorn

> Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
