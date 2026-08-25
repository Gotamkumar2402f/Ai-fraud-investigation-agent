from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.config import LLM_PROVIDER, LLM_MODEL, OPENAI_API_KEY, GROQ_API_KEY, OLLAMA_BASE_URL
from src.tools.transaction_tools import get_transaction, get_customer_transactions, search_transactions_by_merchant
from src.tools.customer_tools import get_customer_profile, get_customer_velocity
from src.tools.risk_tools import check_ip_risk, check_merchant_risk, calculate_simple_risk_score
from src.tools.knowledge_tools import find_similar_past_cases

def get_llm():
    if LLM_PROVIDER == "groq":
        return ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=0)
    elif LLM_PROVIDER == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
    else:
        return ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=0)

TOOLS = [
    get_transaction,
    get_customer_transactions,
    search_transactions_by_merchant,
    get_customer_profile,
    get_customer_velocity,
    check_ip_risk,
    check_merchant_risk,
    calculate_simple_risk_score,
    find_similar_past_cases,
]

SYSTEM_PROMPT = """You are an expert Fraud Investigation Agent working for a financial institution.
Your job is to thoroughly investigate a suspicious transaction and produce a clear, structured, auditable report.

Process:
1. Always start by fetching the transaction details.
2. Fetch the customer profile and recent transaction history / velocity.
3. Check IP risk and merchant risk.
4. Look for similar past cases.
5. Calculate an overall risk score using the calculate_simple_risk_score tool.
6. Reason step-by-step about the evidence.
7. Give a final recommendation: APPROVE / REVIEW / BLOCK
8. Write a professional investigation summary that a human analyst can act on.

Be precise, cite the evidence you found, and never invent data.
If information is missing, say so clearly.
"""

def create_investigator_agent():
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True, handle_parsing_errors=True, max_iterations=12)
    return executor

def investigate(transaction_id: str) -> str:
    agent = create_investigator_agent()
    query = f"""Investigate transaction {transaction_id} thoroughly.
Produce a final structured report with:
- Transaction summary
- Customer profile summary
- Key risk signals found
- Risk score and level
- Similar past cases
- Final recommendation (APPROVE / REVIEW / BLOCK)
- Detailed reasoning
"""
    result = agent.invoke({"input": query})
    return result["output"]