import { type ClassValue, clsx } from 'clsx';

export function cn(...inputs: ClassValue[]) {
    return clsx(inputs);
}

export function formatNumber(num: number): string {
    if (num >= 1000000) {
        return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
        return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
}

export function formatPercentage(value: number): string {
    const sign = value > 0 ? '+' : '';
    return `${sign}${value.toFixed(1)}%`;
}

export function getRelativeTime(date: Date | string): string {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000);

    if (diffInSeconds < 60) {
        return 'agora mesmo';
    }

    const diffInMinutes = Math.floor(diffInSeconds / 60);
    if (diffInMinutes < 60) {
        return `${diffInMinutes}min atrás`;
    }

    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) {
        return `${diffInHours}h atrás`;
    }

    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) {
        return `${diffInDays}d atrás`;
    }

    return dateObj.toLocaleDateString('pt-BR');
}
