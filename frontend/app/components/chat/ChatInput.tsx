'use client';

import { useState, KeyboardEvent } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface ChatInputProps {
    onSend: (message: string) => void;
    isTyping: boolean;
    disabled?: boolean;
}

export function ChatInput({ onSend, isTyping, disabled = false }: ChatInputProps) {
    const [message, setMessage] = useState('');

    const handleSend = () => {
        if (message.trim() && !disabled && !isTyping) {
            onSend(message.trim());
            setMessage('');
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="border-t border-slate-200/60 py-26 px-26 bg-white/80">
            {isTyping && (
                <div className="flex items-center gap-2 text-sm text-slate-500 mb-3">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>Agente está digitando...</span>
                </div>
            )}

            <div className="flex gap-2 items-end">
                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder=".    Digite sua mensagem..."
                    disabled={disabled || isTyping}
                    rows={1}
                    className="w-96 h-16 flex-1 resize-none bg-slate-50 text-slate-900 text-sm placeholder-slate-400 rounded-xl px-4 py-3 pl-12 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed max-h-32"
                    style={{ minHeight: '48px' }}
                />

                <motion.button
                    onClick={handleSend}
                    disabled={!message.trim() || disabled || isTyping}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex-shrink-0 w-16 h-16 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    aria-label="Enviar mensagem"
                >
                    <Send className="w-5 h-5 text-white" />
                </motion.button>
            </div>

        </div>
    );
}
