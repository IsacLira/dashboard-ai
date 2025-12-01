'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import type { ChatMessage, ChatState } from '@/types';
import { apiClient } from '@/lib/api';

export function useChat() {
    const [state, setState] = useState<ChatState>({
        messages: [],
        isOpen: false,
        isTyping: false,
        hasUnread: false,
    });

    const wsRef = useRef<WebSocket | null>(null);

    // Load chat history on mount
    useEffect(() => {
        const loadHistory = async () => {
            try {
                const messages = await apiClient.getChatHistory();
                setState((prev) => ({ ...prev, messages }));
            } catch (error) {
                console.error('Failed to load chat history:', error);
            }
        };

        loadHistory();
    }, []);

    // Setup WebSocket connection
    useEffect(() => {
        const handleMessage = (message: ChatMessage) => {
            setState((prev) => ({
                ...prev,
                messages: [...prev.messages, message],
                isTyping: false,
                hasUnread: !prev.isOpen,
            }));
        };

        wsRef.current = apiClient.createChatWebSocket(handleMessage);

        return () => {
            wsRef.current?.close();
        };
    }, []);

    const sendMessage = useCallback(async (content: string) => {
        const userMessage: ChatMessage = {
            id: Date.now().toString(),
            role: 'user',
            content,
            timestamp: new Date(),
        };

        setState((prev) => ({
            ...prev,
            messages: [...prev.messages, userMessage],
            isTyping: true,
        }));

        try {
            const response = await apiClient.sendMessage(content);

            const agentMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                role: 'agent',
                content: response.message,
                timestamp: new Date(response.timestamp),
            };

            setState((prev) => ({
                ...prev,
                messages: [...prev.messages, agentMessage],
                isTyping: false,
            }));
        } catch (error) {
            console.error('Failed to send message:', error);
            setState((prev) => ({ ...prev, isTyping: false }));
        }
    }, []);

    const toggleChat = useCallback(() => {
        setState((prev) => ({
            ...prev,
            isOpen: !prev.isOpen,
            hasUnread: prev.isOpen ? prev.hasUnread : false,
        }));
    }, []);

    const closeChat = useCallback(() => {
        setState((prev) => ({ ...prev, isOpen: false }));
    }, []);

    return {
        ...state,
        sendMessage,
        toggleChat,
        closeChat,
    };
}
