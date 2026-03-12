from langgraph.graph import add_messages,END,START,StateGraph
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_core.tools import Tool,tool
from langchain_openai import ChatOpenAI
from langgraph.graph.message import Annotated,add_messages,TypedDict
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
import os
import base64

load_dotenv(override=True)
class State(TypedDict):
            messages : Annotated[list,add_messages]
            img : str
            type_img : str
            summary : str

class Agentic_ai:
    def main(self ,img: str , type_img : str):
        with open(img , "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        converted_img = f"data:image/jpeg;base64,{image_base64}"
        llm = ChatOpenAI(
            model = "gemini-2.5-flash",
            base_url=os.getenv("GEMINI_BASE_URL"),
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature = 0.0
        )
        graph_builder = StateGraph(State)


        def explainable_ai(state : State):
            instruction = [
            SystemMessage(
                content="""
                You are an explainable medical AI assistant and also a Brain specialist doctor.  Your task is to provide a structured, plain-text justification for an MRI image.

                REPORT STRUCTURE:
                1.TYPE :Describe and say  Which type of Tumor It is
                2. LOCATION: Describe the specific area where the mass is situated and locate the mass like it is in center or left to or right to something.
                3. SHAPE/APPEARANCE: Describe the visual form and brightness of the mass.
                4. STRUCTURAL IMPACT: Mention how the mass affects the surrounding brain areas.


                RULES:
                - Use PLAIN TEXT ONLY. Do not use Markdown (no asterisks, hashes, or bolding).
                -Needed detailed explanation for 10 to 15 points not in 5 points and should talk like doctor
                - Use indentation (spaces) to make the report look neat.
                - Use cautious language (may indicate, might suggest, could be related).
                - Keep the response between 8 and 12 lines total.
                - Do NOT provide a diagnosis or confirm the disease.
                - End with exactly: 
                "This is an AI-based explanation and not a medical diagnosis. Please consult a qualified neurologist."
                """
                    ),

                    HumanMessage(
                        content=[
                            {
                                "type": "text",
                                "text": f"""
                The user provided disease type: {state['type_img']}.

                Analyze the MRI image and explain why visual patterns in the image may justify this disease type.
                """
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": state["img"]
                                }
                            }
                        ]
                    )
            ]
            result = llm.invoke(instruction)
            print(result.content)
            return {
                "messages"  : [result], 
                "summary" : result.content
            }
        graph_builder.add_node("question_agent", explainable_ai)
        graph_builder.add_edge(START,"question_agent")
        graph_builder.add_edge("question_agent",END)

        graph = graph_builder.compile()

        current_state = {"messages" : [] , "img" : converted_img , "type_img" : type_img , "summary" : ""}

        output = graph.invoke(current_state)
        return output["summary"]