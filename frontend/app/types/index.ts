// Chat Types
export interface ChatMessage {
    id: string;
    role: 'user' | 'agent';
    content: string;
    timestamp: Date;
    isTyping?: boolean;
}

export interface ChatState {
    messages: ChatMessage[];
    isOpen: boolean;
    isTyping: boolean;
    hasUnread: boolean;
}

// Dashboard Types
export interface MetricData {
    id: string;
    label: string;
    value: number | string;
    change?: number;
    trend?: 'up' | 'down' | 'neutral';
    icon?: string;
    color?: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
}

export interface ChartDataPoint {
    name: string;
    value: number;
    [key: string]: string | number;
}

export interface DashboardData {
    metrics: MetricData[];
    chartData: ChartDataPoint[];
    recentActivity: ActivityItem[];
}

export interface ActivityItem {
    id: string;
    title: string;
    description: string;
    timestamp: Date;
    type: 'info' | 'success' | 'warning' | 'error';
}

// API Response Types
export interface ApiResponse<T> {
    data: T;
    error?: string;
    status: number;
}

export interface ChatResponse {
    message: string;
    timestamp: string;
}

export interface ChatHistoryResponse {
    messages: ChatMessage[];
}
