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
    """Get dashboard metrics and data from real CSV analysis"""
    import pandas as pd
    import os
    from datetime import datetime, timedelta
    
    # Load CSV
    data_path = '../data/train.csv'
    if not os.path.exists(data_path):
        # Fallback to mock data if CSV not found
        return get_mock_dashboard_data()
    
    try:
        df = pd.read_csv(data_path)
        
        # Parse dates
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
        
        # Calculate real metrics
        total_sales = df['Sales'].sum()
        total_orders = df['Order ID'].nunique()
        total_customers = df['Customer ID'].nunique()
        avg_order_value = df.groupby('Order ID')['Sales'].sum().mean()
        
        # Calculate growth (compare last 6 months vs previous 6 months)
        df_sorted = df.sort_values('Order Date')
        cutoff_date = df_sorted['Order Date'].max() - timedelta(days=180)
        recent_sales = df[df['Order Date'] >= cutoff_date]['Sales'].sum()
        old_sales = df[df['Order Date'] < cutoff_date]['Sales'].sum()
        sales_growth = ((recent_sales - old_sales) / old_sales * 100) if old_sales > 0 else 0
        
        # Customer growth
        recent_customers = df[df['Order Date'] >= cutoff_date]['Customer ID'].nunique()
        old_customers = df[df['Order Date'] < cutoff_date]['Customer ID'].nunique()
        customer_growth = ((recent_customers - old_customers) / old_customers * 100) if old_customers > 0 else 0
        
        # Monthly sales trend
        df['YearMonth'] = df['Order Date'].dt.to_period('M')
        monthly_sales = df.groupby('YearMonth').agg({
            'Sales': 'sum',
            'Customer ID': 'nunique'
        }).reset_index()
        monthly_sales = monthly_sales.tail(12)  # Last 12 months for better visualization
        
        # Month names in Portuguese
        month_names = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        
        chart_data = []
        for _, row in monthly_sales.iterrows():
            period = row['YearMonth']
            month_num = period.month
            year = period.year
            month_label = f"{month_names[month_num]}/{str(year)[-2:]}"  # e.g., "Jan/17"
            
            chart_data.append(ChartDataPoint(
                name=month_label,
                value=int(row['Sales']),
                usuarios=int(row['Customer ID'])
            ))
        
        # Top categories
        category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        top_category = category_sales.index[0] if len(category_sales) > 0 else "N/A"
        
        # Recent activity (based on recent orders)
        recent_orders = df.nlargest(3, 'Order Date')
        activities = []
        for idx, row in recent_orders.iterrows():
            activities.append(ActivityItem(
                id=str(idx),
                title=f"Order #{row['Order ID'][:8]}",
                description=f"{row['Category']} - {row['Sub-Category']} (R$ {row['Sales']:.2f})",
                timestamp=row['Order Date'].isoformat() if pd.notna(row['Order Date']) else datetime.now().isoformat(),
                type="success"
            ))
        
        return DashboardData(
            metrics=[
                MetricData(
                    id="1",
                    label="Total Sales",
                    value=f"R$ {total_sales/1000:.1f}K",
                    change=round(sales_growth, 1),
                    trend="up" if sales_growth > 0 else "down",
                    color="primary"
                ),
                MetricData(
                    id="2",
                    label="Total of Customers",
                    value=total_customers,
                    change=round(customer_growth, 1),
                    trend="up" if customer_growth > 0 else "down",
                    color="success"
                ),
                MetricData(
                    id="3",
                    label="Average Order Value",
                    value=f"R$ {avg_order_value:.2f}",
                    change=0,
                    trend="up",
                    color="warning"
                ),
                MetricData(
                    id="4",
                    label="Total of Orders",
                    value=total_orders,
                    change=0,
                    trend="up",
                    color="secondary"
                ),
            ],
            chartData=chart_data,
            recentActivity=activities
        )
    
    except Exception as e:
        import traceback
        print(f"="*80)
        print(f"ERROR generating dashboard data: {str(e)}")
        print(f"Traceback:")
        traceback.print_exc()
        print(f"="*80)
        return get_mock_dashboard_data()

def get_mock_dashboard_data():
    """Fallback mock data"""
    return DashboardData(
        metrics=[
            MetricData(
                id="1",
                label="Total of Users",
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

@app.get("/api/dashboard/preview")
def get_data_preview(skip: int = 0, limit: int = 10):
    """Get paginated preview of the dataset"""
    import pandas as pd
    import os
    
    # Load CSV
    data_path = '../data/train.csv'
    if not os.path.exists(data_path):
        return {
            "error": "Dataset not found",
            "data": [],
            "total": 0,
            "columns": [],
            "dtypes": {}
        }
    
    try:
        df = pd.read_csv(data_path)
        
        # Get paginated slice
        df_preview = df.iloc[skip:skip+limit]
        
        # Convert to records (list of dicts)
        records = df_preview.to_dict('records')
        
        # Convert datetime/timestamp columns to strings
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.isoformat()
        
        return {
            "data": records,
            "total": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "skip": skip,
            "limit": limit
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "data": [],
            "total": 0,
            "columns": [],
            "dtypes": {}
        }

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
