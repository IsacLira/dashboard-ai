'use client';

import { LineChart, Line, BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import type { ChartDataPoint } from '@/types';

interface ChartProps {
    data: ChartDataPoint[];
    type?: 'line' | 'bar' | 'area';
    dataKey: string;
    xAxisKey?: string;
    height?: number;
    color?: string;
}

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        return (
            <div className="glass rounded-lg p-3 shadow-xl">
                <p className="text-sm font-medium text-[var(--foreground)] mb-1">{label}</p>
                {payload.map((entry: any, index: number) => (
                    <p key={index} className="text-sm text-[var(--foreground-secondary)]">
                        {entry.name}: <span className="font-semibold" style={{ color: entry.color }}>{entry.value}</span>
                    </p>
                ))}
            </div>
        );
    }
    return null;
};

export function Chart({ data, type = 'line', dataKey, xAxisKey = 'name', height = 300, color }: ChartProps) {
    const chartColor = color || '#2563eb'; // Blue-600

    const commonProps = {
        data,
        margin: { top: 10, right: 10, left: 0, bottom: 0 },
    };

    const axisStyle = { fontSize: '10px', fill: '#64748b' }; // Slate-500

    const renderChart = () => {
        switch (type) {
            case 'bar':
                return (
                    <BarChart {...commonProps}>
                        <XAxis
                            dataKey={xAxisKey}
                            axisLine={false}
                            tickLine={false}
                            tick={axisStyle}
                            dy={10}
                        />
                        <Tooltip
                            cursor={{ fill: '#f1f5f9' }}
                            content={<CustomTooltip />}
                        />
                        <Bar
                            dataKey={dataKey}
                            fill={chartColor}
                            radius={[4, 4, 0, 0]}
                            maxBarSize={50}
                        />
                    </BarChart>
                );

            case 'area':
                return (
                    <AreaChart {...commonProps}>
                        <defs>
                            <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={chartColor} stopOpacity={0.3} />
                                <stop offset="95%" stopColor={chartColor} stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <XAxis
                            dataKey={xAxisKey}
                            axisLine={false}
                            tickLine={false}
                            tick={axisStyle}
                            dy={10}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={axisStyle}
                            dx={-10}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Area
                            type="monotone"
                            dataKey={dataKey}
                            stroke={chartColor}
                            strokeWidth={3}
                            fillOpacity={1}
                            fill="url(#colorGradient)"
                        />
                    </AreaChart>
                );

            default:
                return (
                    <LineChart {...commonProps}>
                        <XAxis
                            dataKey={xAxisKey}
                            axisLine={false}
                            tickLine={false}
                            tick={axisStyle}
                            dy={10}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={axisStyle}
                            dx={-10}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Line
                            type="monotone"
                            dataKey={dataKey}
                            stroke={chartColor}
                            strokeWidth={3}
                            dot={{ fill: 'white', stroke: chartColor, strokeWidth: 2, r: 4 }}
                            activeDot={{ r: 6, strokeWidth: 0 }}
                        />
                    </LineChart>
                );
        }
    };

    return (
        <ResponsiveContainer width="100%" height={height}>
            {renderChart()}
        </ResponsiveContainer>
    );
}
