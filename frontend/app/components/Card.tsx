import { cn } from '@/lib/utils';
import type { ReactNode } from 'react';

interface CardProps {
    children: ReactNode;
    className?: string;
    variant?: 'default' | 'glass' | 'gradient';
    hover?: boolean;
}

export function Card({ children, className, variant = 'default', hover = true }: CardProps) {
    return (
        <div
            className={cn(
                'rounded-xl p-6 transition-all duration-300',
                variant === 'default' && 'bg-[var(--background-secondary)] border border-[var(--glass-border)]',
                variant === 'glass' && 'glass',
                variant === 'gradient' && 'gradient-primary',
                hover && 'hover:shadow-lg hover:-translate-y-1',
                className
            )}
        >
            {children}
        </div>
    );
}

interface CardHeaderProps {
    children: ReactNode;
    className?: string;
}

export function CardHeader({ children, className }: CardHeaderProps) {
    return (
        <div className={cn('mb-4', className)}>
            {children}
        </div>
    );
}

interface CardTitleProps {
    children: ReactNode;
    className?: string;
}

export function CardTitle({ children, className }: CardTitleProps) {
    return (
        <h3 className={cn('text-lg font-semibold text-[var(--foreground)]', className)}>
            {children}
        </h3>
    );
}

interface CardContentProps {
    children: ReactNode;
    className?: string;
}

export function CardContent({ children, className }: CardContentProps) {
    return (
        <div className={cn(className)}>
            {children}
        </div>
    );
}
