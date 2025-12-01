from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import datetime
import json
from analytics_agent import get_analytics_response

app = FastAPI(title="Dashboard AI API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    message: str
    timestamp: str

class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str

class MetricData(BaseModel):
    id: str
    label: str
    value: Union[str, int]
    change: Optional[float] = None
    trend: Optional[str] = None
    color: Optional[str] = None

class ChartDataPoint(BaseModel):
    name: str
    value: int
    usuarios: Optional[int] = None

class ActivityItem(BaseModel):
    id: str
    title: str
    description: str
    timestamp: str
    type: str

class DashboardData(BaseModel):
    metrics: List[MetricData]
    chartData: List[ChartDataPoint]
    recentActivity: List[ActivityItem]

# In-memory storage (replace with database in production)
chat_history: List[ChatMessage] = []
active_connections: List[WebSocket] = []

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Dashboard AI API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Chat endpoints
@app.post("/api/chat", response_model=ChatMessageResponse)
async def send_chat_message(request: ChatMessageRequest):
    """Send a message to the analytics agent"""
    user_message = ChatMessage(
        id=str(len(chat_history) + 1),
        role="user",
        content=request.message,
        timestamp=datetime.now().isoformat()
    )
    chat_history.append(user_message)
    
    # Get response from LLM agent
    agent_response_content = get_analytics_response(request.message)
    
    agent_message = ChatMessage(
        id=str(len(chat_history) + 1),
        role="agent",
        content=agent_response_content,
        timestamp=datetime.now().isoformat()
    )
    chat_history.append(agent_message)
    
    # Broadcast to WebSocket connections
    for connection in active_connections:
        try:
            await connection.send_json(agent_message.dict())
        except:
            pass
    
    return ChatMessageResponse(
        message=agent_response_content,
        timestamp=agent_message.timestamp
    )

@app.get("/api/chat/history")
def get_chat_history():
    """Get chat message history"""
    return {"messages": chat_history}

# Dashboard endpoints
@app.get("/api/dashboard/metrics", response_model=DashboardData)
def get_dashboard_metrics():
    """Get dashboard metrics and data"""
    return DashboardData(
        metrics=[
            MetricData(
                id="1",
                label="Total de Usuários",
                value=12543,
                change=12.5,
                trend="up",
                color="primary"
            ),
            MetricData(
                id="2",
                label="Receita Mensal",
                value="R$ 45.2K",
                change=8.3,
                trend="up",
                color="success"
            ),
            MetricData(
                id="3",
                label="Taxa de Conversão",
                value="3.24%",
                change=-2.1,
                trend="down",
                color="warning"
            ),
            MetricData(
                id="4",
                label="Engajamento",
                value="68.5%",
                change=5.7,
                trend="up",
                color="secondary"
            ),
        ],
        chartData=[
            ChartDataPoint(name="Jan", value=4000, usuarios=2400),
            ChartDataPoint(name="Fev", value=3000, usuarios=1398),
            ChartDataPoint(name="Mar", value=2000, usuarios=9800),
            ChartDataPoint(name="Abr", value=2780, usuarios=3908),
            ChartDataPoint(name="Mai", value=1890, usuarios=4800),
            ChartDataPoint(name="Jun", value=2390, usuarios=3800),
            ChartDataPoint(name="Jul", value=3490, usuarios=4300),
        ],
        recentActivity=[
            ActivityItem(
                id="1",
                title="Novo usuário registrado",
                description="João Silva criou uma conta",
                timestamp=datetime.now().isoformat(),
                type="info"
            ),
            ActivityItem(
                id="2",
                title="Análise concluída",
                description="Relatório de vendas Q2 2024",
                timestamp=datetime.now().isoformat(),
                type="success"
            ),
            ActivityItem(
                id="3",
                title="Alerta de performance",
                description="Tempo de resposta acima do normal",
                timestamp=datetime.now().isoformat(),
                type="warning"
            ),
        ]
    )

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back or process as needed
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
