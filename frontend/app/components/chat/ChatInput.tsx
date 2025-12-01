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
        <div className="border-t border-[var(--glass-border)] p-4 bg-[var(--background-secondary)]">
            {isTyping && (
                <div className="flex items-center gap-2 text-sm text-[var(--foreground-secondary)] mb-2">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>Agente está digitando...</span>
                </div>
            )}

            <div className="flex gap-2 items-end">
                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Digite sua mensagem..."
                    disabled={disabled || isTyping}
                    rows={1}
                    className="flex-1 resize-none bg-[var(--background-tertiary)] text-[var(--foreground)] placeholder-[var(--foreground-tertiary)] rounded-lg px-4 py-2.5 border border-[var(--glass-border)] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] focus:border-transparent transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed max-h-32"
                    style={{ minHeight: '42px' }}
                />

                <motion.button
                    onClick={handleSend}
                    disabled={!message.trim() || disabled || isTyping}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex-shrink-0 w-10 h-10 rounded-lg gradient-primary flex items-center justify-center transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] focus:ring-offset-2 focus:ring-offset-[var(--background-secondary)]"
                    aria-label="Enviar mensagem"
                >
                    <Send className="w-4 h-4 text-white" />
                </motion.button>
            </div>

            <p className="text-xs text-[var(--foreground-tertiary)] mt-2">
                Pressione Enter para enviar, Shift+Enter para nova linha
            </p>
        </div>
    );
}
