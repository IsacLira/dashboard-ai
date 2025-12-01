'use client';

import { Bell, Search, User } from 'lucide-react';
import { motion } from 'framer-motion';

interface HeaderProps {
    title: string;
    subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
    return (
        <header className="h-16 bg-[var(--background-secondary)] border-b border-[var(--glass-border)] px-8 flex items-center justify-between">
            {/* Title */}
            <div>
                <h2 className="text-xl font-bold text-[var(--foreground)]">{title}</h2>
                {subtitle && (
                    <p className="text-sm text-[var(--foreground-secondary)]">{subtitle}</p>
                )}
            </div>

            {/* Actions */}
            <div className="flex items-center gap-4">
                {/* Search */}
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--foreground-tertiary)]" />
                    <input
                        type="text"
                        placeholder="Buscar..."
                        className="w-64 pl-10 pr-4 py-2 bg-[var(--background-tertiary)] text-[var(--foreground)] placeholder-[var(--foreground-tertiary)] rounded-lg border border-[var(--glass-border)] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] focus:border-transparent transition-all duration-200"
                    />
                </div>

                {/* Notifications */}
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="relative w-10 h-10 rounded-lg bg-[var(--background-tertiary)] hover:bg-[var(--background)] border border-[var(--glass-border)] flex items-center justify-center transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))]"
                    aria-label="Notificações"
                >
                    <Bell className="w-5 h-5 text-[var(--foreground-secondary)]" />
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-[hsl(var(--error))] rounded-full border-2 border-[var(--background-secondary)]" />
                </motion.button>

                {/* User Profile */}
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex items-center gap-3 px-3 py-2 rounded-lg bg-[var(--background-tertiary)] hover:bg-[var(--background)] border border-[var(--glass-border)] transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))]"
                >
                    <div className="w-8 h-8 rounded-full gradient-primary flex items-center justify-center">
                        <User className="w-4 h-4 text-white" />
                    </div>
                    <div className="text-left">
                        <p className="text-sm font-medium text-[var(--foreground)]">Usuário</p>
                        <p className="text-xs text-[var(--foreground-secondary)]">Admin</p>
                    </div>
                </motion.button>
            </div>
        </header>
    );
}
