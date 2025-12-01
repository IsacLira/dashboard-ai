'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { LayoutDashboard, BarChart3, Settings, HelpCircle } from 'lucide-react';

const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Configurações', href: '/settings', icon: Settings },
    { name: 'Ajuda', href: '/help', icon: HelpCircle },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="w-64 h-screen bg-[var(--background-secondary)] border-r border-[var(--glass-border)] flex flex-col">
            {/* Logo */}
            <div className="p-6 border-b border-[var(--glass-border)]">
                <h1 className="text-2xl font-bold text-gradient">Dashboard AI</h1>
                <p className="text-xs text-[var(--foreground-secondary)] mt-1">Analytics Platform</p>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-1">
                {navigation.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;

                    return (
                        <Link
                            key={item.name}
                            href={item.href}
                            className={cn(
                                'relative flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group',
                                isActive
                                    ? 'bg-blue-50 text-blue-600'
                                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
                            )}
                        >
                            {isActive && (
                                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-blue-600 rounded-r-full" />
                            )}

                            <Icon
                                className={cn(
                                    'w-5 h-5 transition-transform duration-200 group-hover:scale-110',
                                    isActive ? 'text-blue-600' : 'text-slate-400 group-hover:text-slate-600'
                                )}
                            />
                            <span className="font-medium">{item.name}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-[var(--glass-border)]">
                <div className="glass rounded-lg p-3">
                    <p className="text-xs text-[var(--foreground-secondary)]">
                        Powered by <span className="text-gradient font-semibold">Google Gemini</span>
                    </p>
                </div>
            </div>
        </aside>
    );
}
