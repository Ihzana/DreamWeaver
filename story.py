# main.py
# Backend for DreamScript AI using FastAPI and LangChain
# Run with: uvicorn main:app --reload

import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel as V1BaseModel
from langchain_core.output_parsers.pydantic import PydanticOutputParser

# --- 1. Define Data Models (The Blueprint & Outline) ---
# These Pydantic models ensure the AI returns structured, predictable data.

class DreamBlueprint(V1BaseModel):
    """The structured analysis of the user's dream."""
    title_suggestion: str = Field(description="A creative, fitting title for the story.")
    setting_description: str = Field(description="A detailed description of the dream's environment.")
    characters: list[str] = Field(description="A list of key characters, e.g., 'Protagonist', 'Mysterious Guide'.")
    key_objects: list[str] = Field(description="Important objects or symbols in the dream.")
    emotional_arc: str = Field(description="The primary emotional journey, e.g., 'Confusion -> Urgency -> Resolution'.")
    core_theme: str = Field(description="The central theme or message interpreted from the dream.")

class StoryOutput(V1BaseModel):
    """The final generated short story and analysis."""
    title: str = Field(description="The final title of the story.")
    story_text: str = Field(description="The full text of the generated short story (500-1500 words).")
    analyst_corner: str = Field(description="A brief analysis explaining the creative choices made based on the dream's symbols.")

# --- 2. Initialize the AI Model ---

# TODO: Add your OpenAI API key to your environment variables
# For example: export OPENAI_API_KEY="sk-..."
llm = ChatOpenAI(model="gpt-4o", temperature=0.8)

# --- 3. Define the AI Agent Chain ---
# We use LangChain Expression Language (LCEL) to pipe the output of one step to the next.

# Agent 1: The Analyst
# Takes the user's raw dream text and creates the structured DreamBlueprint.
analyst_parser = PydanticOutputParser(pydantic_object=DreamBlueprint)
analyst_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a brilliant dream analyst and storyteller. Your job is to analyze the user's dream description and structure it into a detailed blueprint for a short story. Extract the core elements as specified in the output format instructions."),
    ("human", "Here is my dream: {dream_description}\n\n{format_instructions}")
])
analyst_chain = analyst_prompt | llm | analyst_parser

# Agent 2: The Storyteller
# Takes the detailed blueprint and writes the full story.
storyteller_parser = PydanticOutputParser(pydantic_object=StoryOutput)
storyteller_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a master prose stylist. Your task is to take a story blueprint and write a complete, compelling, and evocative short story based on it. You must also write an 'Analyst's Corner' explaining how the theme was woven into the narrative. Follow the output format instructions precisely."),
    ("human", "Here is the story blueprint: {blueprint}\n\nWrite the full story and the analysis. {format_instructions}")
])
storyteller_chain = storyteller_prompt | llm | storyteller_parser

# The Complete DreamScript Chain
# This chains the two agents together. The output of the analyst becomes the input for the storyteller.
def create_story_from_blueprint(blueprint: DreamBlueprint):
    """Function to invoke the storyteller chain with the blueprint."""
    return storyteller_chain.invoke({
        "blueprint": blueprint.model_dump_json(),
        "format_instructions": storyteller_parser.get_format_instructions()
    })

full_chain = analyst_chain | create_story_from_blueprint

# --- 4. Create the API Server ---
# We use FastAPI to create a web endpoint that the frontend can call.

app = FastAPI(
    title="DreamScript AI",
    description="API for turning dream descriptions into short stories.",
)

class DreamInput(BaseModel):
    dream_description: str = Field(
        ...,
        min_length=10,
        example="I was in an old, dusty library where the shelves held ticking clocks instead of books."
    )

@app.post("/generate-story", response_model=StoryOutput)
async def generate_story(dream_input: DreamInput):
    """
    Takes a dream description and returns a fully-formed short story.
    """
    print("Received request to generate story...")
    
    # Invoke the full AI chain with the user's input
    story_result = full_chain.invoke({
        "dream_description": dream_input.dream_description,
        "format_instructions": analyst_parser.get_format_instructions()
    })
    
    print("Story generation complete.")
    return story_result

# To test this API, you would run `uvicorn main:app --reload`
# and then send a POST request using a tool like curl or a web frontend.
#
# Example curl command:
# curl -X POST "http://127.0.0.1:8000/generate-story" \
# -H "Content-Type: application/json" \
# -d '{"dream_description": "I was in a forest where the trees were made of glass and whispered secrets when the wind blew."}'
