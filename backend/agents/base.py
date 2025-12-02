"""Simplified base agent using LangChain's native capabilities.

This module provides a minimal base class that leverages LangChain's
built-in agent functionality instead of reimplementing features.
"""

from typing import List, Optional
import logging
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent


class SimpleAgent:
    """Simplified agent that uses LangGraph's create_react_agent.
    
    This class wraps LangGraph's create_react_agent providing a clean
    interface for agent invocation with proper output handling.
    
    Attributes:
        llm: The language model instance.
        tools: List of tools available to the agent.
        system_prompt: System prompt defining agent behavior.
        agent: The LangGraph agent instance.
        logger: Logger for the agent.
    """
    
    def __init__(
        self,
        llm,
        system_prompt: str,
        tools: Optional[List] = None,
        template: Optional[str] = None
    ):
        """Initialize the agent.
        
        Args:
            llm: Language model instance.
            system_prompt: System prompt for the agent.
            tools: Optional list of tools.
            template: Optional prompt template string.
        """
        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Process template if provided
        if template:
            # Format tools for the template
            tool_strings = []
            for tool in self.tools:
                args_schema = str(tool.args) if hasattr(tool, 'args') else ""
                tool_strings.append(f"{tool.name}: {tool.description}, args: {args_schema}")
            formatted_tools = "\n".join(tool_strings)
            tool_names = ", ".join([t.name for t in self.tools])
            
            # Replace placeholders
            # We replace {input} and {agent_scratchpad} with generic instructions
            # because LangGraph handles the actual conversation state
            final_prompt = template.replace("{tools}", formatted_tools)
            final_prompt = final_prompt.replace("{tool_names}", tool_names)
            final_prompt = final_prompt.replace("{input}", "the user's request")
            final_prompt = final_prompt.replace("{agent_scratchpad}", "")
            
            # Combine with system prompt if needed, or override
            # self.system_prompt = f"{system_prompt}\n\n{final_prompt}"
            self.system_prompt = f"{final_prompt}"
        # Create agent using LangGraph
        # We don't pass system_prompt here because we prepend it as a SystemMessage in invoke()
        # This avoids compatibility issues with different langgraph versions (state_modifier vs messages_modifier)
        self.agent = create_react_agent(self.llm, self.tools)
        
        self.logger.info(
            f"Initialized {self.__class__.__name__} with {len(self.tools)} tools"
        )
    
    def invoke(self, user_message: str) -> str:
        """Invoke the agent with a user message.
        
        Args:
            user_message: The user's query.
            
        Returns:
            The agent's response as a string.
        """
        try:
            # Prepare messages with system prompt
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_message)
            ]
            
            # Invoke agent
            result = self.agent.invoke(
                {"messages": messages},
                config={"recursion_limit": 50}
            )
            
            # Extract last message content
            messages_list = result.get("messages", [])
            if not messages_list:
                return "Desculpe, não consegui processar sua solicitação."
            
            # Get last message with content
            content = None
            for msg in reversed(messages_list):
                msg_content = getattr(msg, 'content', '')
                if msg_content and msg_content != "None" and msg_content.strip():
                    content = msg_content
                    break
            
            # If no content found, force agent to generate final response
            if not content:
                self.logger.warning("Agent stopped without final response, forcing continuation...")
                messages_list.append(
                    HumanMessage(content="Por favor, gere uma resposta final em texto para o usuário com base nos resultados das ferramentas.")
                )
                
                # Invoke again
                result = self.agent.invoke(
                    {"messages": messages_list},
                    config={"recursion_limit": 50}
                )
                
                # Try to extract content again
                new_messages = result.get("messages", [])
                for msg in reversed(new_messages):
                    msg_content = getattr(msg, 'content', '')
                    if msg_content and msg_content != "None" and msg_content.strip():
                        content = msg_content
                        break
            
            return content if content else "Desculpe, não consegui gerar uma resposta."
            
        except Exception as e:
            self.logger.error(f"Error invoking agent: {str(e)}")
            return f"Erro ao processar: {str(e)}"
