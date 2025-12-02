'use client';

import { MessageCircle, X, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ChatButtonProps {
    isOpen: boolean;
    hasUnread: boolean;
    onClick: () => void;
}

export function ChatButton({ isOpen, hasUnread, onClick }: ChatButtonProps) {
    return (
        <div className="fixed bottom-6 right-6 z-50">
            {/* Tooltip */}
            <AnimatePresence>
                {!isOpen && (
                    <motion.div
                        initial={{ opacity: 0, x: 10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 10 }}
                        className="absolute bottom-full right-0 mb-2 px-3 py-2 bg-slate-900 text-white text-sm rounded-lg shadow-lg whitespace-nowrap pointer-events-none"
                    >
                        Pergunte ao Analytics AI
                        <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-slate-900" />
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Pulse ring for unread */}
            <AnimatePresence>
                {hasUnread && !isOpen && (
                    <motion.div
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.5, 0.2, 0.5]
                        }}
                        exit={{ scale: 0.8, opacity: 0 }}
                        transition={{
                            duration: 2,
                            repeat: Infinity,
                            ease: "easeInOut"
                        }}
                        className="absolute inset-0 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600"
                    />
                )}
            </AnimatePresence>

            {/* Main button */}
            <motion.button
                onClick={onClick}
                className="relative w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 shadow-xl flex items-center justify-center transition-all duration-300 hover:shadow-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/50"
                whileHover={{ scale: 1.05, rotate: isOpen ? 0 : 5 }}
                whileTap={{ scale: 0.95 }}
                aria-label={isOpen ? 'Fechar chat' : 'Abrir chat'}
                style={{
                    boxShadow: '0 10px 40px -10px rgba(59, 130, 246, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.1) inset'
                }}
            >
                <AnimatePresence mode="wait">
                    {isOpen ? (
                        <motion.div
                            key="close"
                            initial={{ rotate: -90, opacity: 0, scale: 0.8 }}
                            animate={{ rotate: 0, opacity: 1, scale: 1 }}
                            exit={{ rotate: 90, opacity: 0, scale: 0.8 }}
                            transition={{ duration: 0.2 }}
                        >
                            <X className="w-7 h-7 text-white" strokeWidth={2.5} />
                        </motion.div>
                    ) : (
                        <motion.div
                            key="open"
                            initial={{ rotate: 90, opacity: 0, scale: 0.8 }}
                            animate={{ rotate: 0, opacity: 1, scale: 1 }}
                            exit={{ rotate: -90, opacity: 0, scale: 0.8 }}
                            transition={{ duration: 0.2 }}
                            className="relative"
                        >
                            <MessageCircle className="w-7 h-7 text-white" strokeWidth={2.5} />
                            {hasUnread && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="absolute -top-1 -right-1"
                                >
                                    <Sparkles className="w-4 h-4 text-yellow-300" fill="currentColor" />
                                </motion.div>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Unread badge */}
                <AnimatePresence>
                    {hasUnread && !isOpen && (
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            exit={{ scale: 0 }}
                            className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full border-2 border-white shadow-lg flex items-center justify-center"
                        >
                            <span className="text-[10px] font-bold text-white">1</span>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.button>
        </div>
    );
}
