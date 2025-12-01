'use client';

import { MessageCircle, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ChatButtonProps {
    isOpen: boolean;
    hasUnread: boolean;
    onClick: () => void;
}

export function ChatButton({ isOpen, hasUnread, onClick }: ChatButtonProps) {
    return (
        <motion.button
            onClick={onClick}
            className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full gradient-primary shadow-xl flex items-center justify-center transition-all duration-300 hover:shadow-2xl hover:scale-110 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] focus:ring-offset-2 focus:ring-offset-[var(--background)]"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            aria-label={isOpen ? 'Fechar chat' : 'Abrir chat'}
        >
            <AnimatePresence mode="wait">
                {isOpen ? (
                    <motion.div
                        key="close"
                        initial={{ rotate: -90, opacity: 0 }}
                        animate={{ rotate: 0, opacity: 1 }}
                        exit={{ rotate: 90, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                    >
                        <X className="w-6 h-6 text-white" />
                    </motion.div>
                ) : (
                    <motion.div
                        key="open"
                        initial={{ rotate: 90, opacity: 0 }}
                        animate={{ rotate: 0, opacity: 1 }}
                        exit={{ rotate: -90, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                    >
                        <MessageCircle className="w-6 h-6 text-white" />
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Unread indicator */}
            <AnimatePresence>
                {hasUnread && !isOpen && (
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        exit={{ scale: 0 }}
                        className="absolute -top-1 -right-1 w-4 h-4 bg-[hsl(var(--error))] rounded-full border-2 border-[var(--background)] animate-pulse"
                    />
                )}
            </AnimatePresence>
        </motion.button>
    );
}
