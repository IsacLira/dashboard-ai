import type { ChatMessage, ChatResponse, DashboardData } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    private async request<T>(
        endpoint: string,
        options?: RequestInit
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options?.headers,
                },
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Chat endpoints
    async sendMessage(message: string): Promise<ChatResponse> {
        return this.request<ChatResponse>('/api/chat', {
            method: 'POST',
            body: JSON.stringify({ message }),
        });
    }

    async getChatHistory(): Promise<ChatMessage[]> {
        const response = await this.request<{ messages: ChatMessage[] }>('/api/chat/history');
        return response.messages;
    }

    // Dashboard endpoints
    async getDashboardData(): Promise<DashboardData> {
        return this.request<DashboardData>('/api/dashboard/metrics');
    }

    // WebSocket connection for real-time chat
    createChatWebSocket(
        onMessage: (message: ChatMessage) => void,
        onError?: (error: Event) => void
    ): WebSocket {
        const wsUrl = this.baseUrl.replace('http', 'ws');
        const ws = new WebSocket(`${wsUrl}/ws/chat`);

        ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data) as ChatMessage;
                onMessage(message);
            } catch (error) {
                console.error('Failed to parse WebSocket message:', error);
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            onError?.(error);
        };

        return ws;
    }
}

export const apiClient = new ApiClient(API_BASE_URL);
