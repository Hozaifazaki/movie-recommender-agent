from crewai import LLM


class LLMService:
    def __init__(self, model_config: dict, selected_model: str):
        self.model_config = model_config
        self.selected_model = selected_model
        self.llm_model = self._initialize_llm()

    def _initialize_llm(self):
        llm = LLM(**self.model_config[self.selected_model])
        return llm
