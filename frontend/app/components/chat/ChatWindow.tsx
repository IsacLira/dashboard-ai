'use client';

import { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Bot } from 'lucide-react';
import { ChatMessageBubble } from './ChatMessage';
import { ChatInput } from './ChatInput';
import type { ChatMessage } from '@/types';

interface ChatWindowProps {
    isOpen: boolean;
    messages: ChatMessage[];
    isTyping: boolean;
    onClose: () => void;
    onSendMessage: (message: string) => void;
}

export function ChatWindow({ isOpen, messages, isTyping, onClose, onSendMessage }: ChatWindowProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: 20, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 20, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                    className="fixed bottom-24 right-6 z-40 w-96 h-[600px] flex flex-col glass rounded-2xl overflow-hidden shadow-2xl"
                >
                    {/* Header */}
                    <div className="flex items-center justify-between p-4 border-b border-[var(--glass-border)] bg-[var(--background-secondary)]">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full gradient-primary flex items-center justify-center">
                                <Bot className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-[var(--foreground)]">Agente Analytics</h3>
                                <p className="text-xs text-[var(--foreground-secondary)]">Online</p>
                            </div>
                        </div>

                        <button
                            onClick={onClose}
                            className="w-8 h-8 rounded-lg hover:bg-[var(--background-tertiary)] flex items-center justify-center transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))]"
                            aria-label="Fechar chat"
                        >
                            <X className="w-5 h-5 text-[var(--foreground-secondary)]" />
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 bg-[var(--background)]">
                        {messages.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-full text-center">
                                <div className="w-16 h-16 rounded-full gradient-secondary flex items-center justify-center mb-4">
                                    <Bot className="w-8 h-8 text-white" />
                                </div>
                                <h4 className="text-lg font-semibold text-[var(--foreground)] mb-2">
                                    Olá! 👋
                                </h4>
                                <p className="text-sm text-[var(--foreground-secondary)] max-w-xs">
                                    Sou seu agente de analytics. Como posso ajudar você hoje?
                                </p>
                            </div>
                        ) : (
                            <>
                                {messages.map((message) => (
                                    <ChatMessageBubble key={message.id} message={message} />
                                ))}
                                <div ref={messagesEndRef} />
                            </>
                        )}
                    </div>

                    {/* Input */}
                    <ChatInput onSend={onSendMessage} isTyping={isTyping} />
                </motion.div>
            )}
        </AnimatePresence>
    );
}
