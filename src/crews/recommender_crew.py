from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.tools.retriver_tool import RetrieverTool
from src.utils.path_util import PathUtil
from src.utils.yaml_loader import read_yaml


@CrewBase
class RecommenderCrew:
    def __init__(self, vector_store, llm_service):
        self.vector_store = vector_store
        self.llm = llm_service.llm_model

    #### Agents
    @agent
    def movie_matcher(self) -> Agent:
        agent_config = read_yaml(PathUtil.get_agent_config_path("movie_matcher.yaml"))
        agent = Agent(
            config=agent_config["movie_matcher"],
            verbose=True,
            tools=[RetrieverTool(vector_store=self.vector_store, k=3)],
            llm=self.llm,
        )
        return agent

    @agent
    def preference_analyst(self) -> Agent:
        agent_config = read_yaml(PathUtil.get_agent_config_path("preference_analyst.yaml"))
        agent = Agent(
            config=agent_config["preference_analyst"],
            verbose=True,
            # tools=[RetrieverTool(vector_store=self.vector_store, k=3)],
            llm=self.llm
        )
        return agent

    @agent
    def recommendation_generator(self) -> Agent:
        agent_config = read_yaml(PathUtil.get_agent_config_path("recommendation_generator.yaml"))
        agent = Agent(
            config=agent_config["recommendation_generator"],
            verbose=True,
            # tools=[RetrieverTool(vector_store=self.vector_store, k=3)],
            llm=self.llm
        )
        return agent
    
    #### Tasks
    @task
    def analyze_preferences_task(self) -> Task:
        task_config = read_yaml(PathUtil.get_tasks_config_path("analyze_preferences.yaml"))
        task = Task(
            config=task_config["analyze_preferences_task"],
            agent=self.preference_analyst(),
        )
        return task
    
    @task
    def match_movie_task(self) -> Task:
        task_config = read_yaml(PathUtil.get_tasks_config_path("match_movies.yaml"))
        task = Task(
            config=task_config["match_movies_task"],
            agent=self.movie_matcher(),
        )
        return task
    
    @task
    def generate_recommendation_task(self) -> Task:
        task_config = read_yaml(PathUtil.get_tasks_config_path("generate_recommendation.yaml"))
        task = Task(
            config=task_config["generate_recommendation_task"],
            agent=self.recommendation_generator(),
        )
        return task
    
    #### Crews
    @crew
    def crew(self) -> Crew:
        recommender_crew = Crew(
            agents=[self.preference_analyst(), self.movie_matcher(), self.recommendation_generator()],
            tasks=[self.analyze_preferences_task(), self.match_movie_task(), self.generate_recommendation_task()],
            process=Process.sequential,
            verbose=True,
        )
        return recommender_crew
