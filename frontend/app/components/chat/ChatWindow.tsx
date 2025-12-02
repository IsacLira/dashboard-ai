'use client';

import { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Bot, Minimize2, Maximize2 } from 'lucide-react';
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
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="fixed inset-0 bg-black/10 backdrop-blur-sm z-30"
                        onClick={onClose}
                    />

                    {/* Chat Window */}
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                        transition={{
                            duration: 0.3,
                            type: "spring",
                            stiffness: 300,
                            damping: 30
                        }}
                        className="fixed bottom-24 right-6 z-40 w-[480px] h-[700px] flex flex-col rounded-2xl overflow-hidden shadow-2xl border border-slate-200/60"
                        style={{
                            background: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(20px)',
                        }}
                    >
                        {/* Header */}
                        <div className="flex items-center justify-between p-6 border-b border-slate-200/60 bg-gradient-to-r from-blue-50/80 to-indigo-50/80">
                            <div className="flex items-center gap-3">
                                <div className="relative">
                                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg">
                                        <Bot className="w-5 h-5 text-white" />
                                    </div>
                                    {/* Online indicator */}
                                    <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-500 rounded-full border-2 border-white shadow-sm" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-slate-900">Analytics Agent</h3>
                                    <p className="text-xs text-emerald-600 font-medium">Online</p>
                                </div>
                            </div>

                            <button
                                onClick={onClose}
                                className="w-8 h-8 rounded-lg hover:bg-slate-100 flex items-center justify-center transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 hover:scale-105"
                                aria-label="Fechar chat"
                            >
                                <X className="w-5 h-5 text-slate-600" />
                            </button>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-slate-50/50 to-white">
                            {messages.length === 0 ? (
                                <div className="flex flex-col items-center justify-center h-full text-center px-4">
                                    <motion.div
                                        initial={{ scale: 0.8, opacity: 0 }}
                                        animate={{ scale: 1, opacity: 1 }}
                                        transition={{ delay: 0.1 }}
                                        className="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center mb-6 shadow-xl"
                                    >
                                        <Bot className="w-10 h-10 text-white" />
                                    </motion.div>
                                    <motion.h4
                                        initial={{ y: 10, opacity: 0 }}
                                        animate={{ y: 0, opacity: 1 }}
                                        transition={{ delay: 0.2 }}
                                        className="text-xl font-bold text-slate-900 mb-3"
                                    >
                                        Olá! 👋
                                    </motion.h4>
                                    <motion.p
                                        initial={{ y: 10, opacity: 0 }}
                                        animate={{ y: 0, opacity: 1 }}
                                        transition={{ delay: 0.3 }}
                                        className="text-sm text-slate-600 max-w-xs leading-relaxed"
                                    >
                                        I'm your analytics agent. I can help you analyze data, generate insights, and answer questions about the dataset.
                                    </motion.p>
                                    <motion.div
                                        initial={{ y: 10, opacity: 0 }}
                                        animate={{ y: 0, opacity: 1 }}
                                        transition={{ delay: 0.4 }}
                                        className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-100"
                                    >
                                        <p className="text-xs text-blue-700 font-medium">
                                            💡 You can ask about sales, customers, or products!
                                        </p>
                                    </motion.div>
                                </div>
                            ) : (
                                <>
                                    {messages.map((message) => (
                                        <ChatMessageBubble key={message.id} message={message} />
                                    ))}
                                    {isTyping && (
                                        <motion.div
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            className="flex items-start gap-3 mb-4"
                                        >
                                            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0 mt-1">
                                                <Bot className="w-5 h-5 text-blue-600" />
                                            </div>
                                            <div className="flex gap-1 items-center p-3 bg-white rounded-2xl shadow-sm border border-slate-100">
                                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                            </div>
                                        </motion.div>
                                    )}
                                    <div ref={messagesEndRef} />
                                </>
                            )}
                        </div>

                        {/* Input */}
                        <ChatInput onSend={onSendMessage} isTyping={isTyping} />
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
