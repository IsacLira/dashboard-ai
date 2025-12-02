import { cn, formatNumber, formatPercentage } from '@/lib/utils';
import type { MetricData } from '@/types';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface MetricCardProps {
    metric: MetricData;
    className?: string;
}

export function MetricCard({ metric, className }: MetricCardProps) {
    const { label, value, change, trend } = metric;

    const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus;

    const trendColor = trend === 'up' ? 'text-emerald-600' : trend === 'down' ? 'text-red-600' : 'text-gray-500';
    const trendBg = trend === 'up' ? 'bg-emerald-50' : trend === 'down' ? 'bg-red-50' : 'bg-gray-100';

    return (
        <div
            className={cn(
                'relative overflow-hidden rounded-2xl p-6 transition-all duration-300',
                'bg-white border border-slate-100 shadow-sm hover:shadow-md',
                className
            )}
        >
            <div className="flex items-start justify-between mb-4">
                <p className="text-sm font-medium text-slate-500">{label}</p>
                <div className={cn('p-1.5 rounded-full', trendBg)}>
                    <TrendIcon className={cn('w-4 h-4', trendColor)} />
                </div>
            </div>

            <div className="flex flex-col items-center justify-center gap-2 mt-2">
                <h3 className="text-lg font-bold text-slate-900">
                    {typeof value === 'number' ? formatNumber(value) : value}
                </h3>

                {change !== undefined && (
                    <span className={cn('text-sm font-semibold', trendColor)}>
                        {trend === 'up' ? '+' : ''}{formatPercentage(change)}
                    </span>
                )}
            </div>
        </div>
    );
}
