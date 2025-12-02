'use client';

import { Bell } from 'lucide-react';
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
            </div>
        </header>
    );
}
