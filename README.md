
# Movie Recommendation Agent with CrewAI and Redis

This project implements a movie recommendation agent using [CrewAI](https://github.com/joaomdmoura/crewAI) and [Redis](https://redis.io/) as a caching layer to optimize performance. The agent leverages AI models to generate personalized movie recommendations based on user input and stores results in Redis to reduce redundant computations.

## Features

- **Personalized Recommendations**: Generates movie suggestions tailored to user preferences.
- **Redis Caching**: Stores recommendation results in Redis to improve response times for repeated queries.
- **CrewAI Agents**: Utilizes CrewAI's agent framework to orchestrate the recommendation process.
- **Scalable Design**: Easily extendable to handle additional features or larger datasets.