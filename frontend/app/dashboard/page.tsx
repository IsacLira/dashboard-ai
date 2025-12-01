'use client';

import { useState, useEffect } from 'react';

import { Header } from '@/components/Header';
import { MetricCard } from '@/components/MetricCard';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/Card';
import { Chart } from '@/components/Chart';
import { useDashboardData } from '@/lib/hooks/useDashboardData'; // This import was in the original but not in the provided snippet, keeping it as per instruction to keep pre-existing comments/empty lines that are not explicitly removed by the change.
import { Loader2, RefreshCw, TrendingUp, Users, DollarSign, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

// Mock data for demonstration
const mockMetrics = [
    { id: '1', label: 'Total de Usuários', value: 12543, change: 12.5, trend: 'up' as const, color: 'primary' as const },
    { id: '2', label: 'Receita Mensal', value: 'R$ 45.2K', change: 8.3, trend: 'up' as const, color: 'success' as const },
    { id: '3', label: 'Taxa de Conversão', value: '3.24%', change: -2.1, trend: 'down' as const, color: 'warning' as const },
    { id: '4', label: 'Engajamento', value: '68.5%', change: 5.7, trend: 'up' as const, color: 'secondary' as const },
];

const mockChartData = [
    { name: 'Jan', value: 4000, usuarios: 2400 },
    { name: 'Fev', value: 3000, usuarios: 1398 },
    { name: 'Mar', value: 2000, usuarios: 9800 },
    { name: 'Abr', value: 2780, usuarios: 3908 },
    { name: 'Mai', value: 1890, usuarios: 4800 },
    { name: 'Jun', value: 2390, usuarios: 3800 },
    { name: 'Jul', value: 3490, usuarios: 4300 },
];

const mockRecentActivity = [
    { id: '1', title: 'Novo usuário registrado', description: 'João Silva criou uma conta', timestamp: new Date(Date.now() - 1000 * 60 * 5), type: 'info' as const },
    { id: '2', title: 'Análise concluída', description: 'Relatório de vendas Q2 2024', timestamp: new Date(Date.now() - 1000 * 60 * 15), type: 'success' as const },
    { id: '3', title: 'Alerta de performance', description: 'Tempo de resposta acima do normal', timestamp: new Date(Date.now() - 1000 * 60 * 30), type: 'warning' as const },
];

export default function DashboardPage() {
    // In production, this would fetch real data
    // const { data, isLoading, error, refetch } = useDashboardData();

    const [mounted, setMounted] = useState(false);
    const [data, setData] = useState<{
        metrics: typeof mockMetrics;
        chartData: typeof mockChartData;
        recentActivity: typeof mockRecentActivity;
    } | null>(null);

    useEffect(() => {
        setMounted(true);
        setData({
            metrics: mockMetrics,
            chartData: mockChartData,
            recentActivity: mockRecentActivity,
        });
    }, []);

    if (!mounted || !data) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    return (
        <>
            <Header title="Dashboard" subtitle="Visão geral das suas métricas" />

            <main className="flex-1 overflow-y-auto p-8 bg-slate-50/50">
                <div className="max-w-7xl mx-auto space-y-8">
                    {/* Metrics Grid */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
                    >
                        {data.metrics.map((metric, index) => (
                            <motion.div
                                key={metric.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                            >
                                <MetricCard metric={metric} />
                            </motion.div>
                        ))}
                    </motion.div>

                    {/* Charts Section */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.4 }}
                        >
                            <Card className="h-full border-slate-100 shadow-sm">
                                <CardHeader>
                                    <CardTitle className="text-slate-800">Receita ao Longo do Tempo</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <Chart data={data.chartData} type="area" dataKey="value" height={300} color="#6366f1" />
                                </CardContent>
                            </Card>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.5 }}
                        >
                            <Card className="h-full border-slate-100 shadow-sm">
                                <CardHeader>
                                    <CardTitle className="text-slate-800">Crescimento de Usuários</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <Chart data={data.chartData} type="bar" dataKey="usuarios" height={300} color="#3b82f6" />
                                </CardContent>
                            </Card>
                        </motion.div>
                    </div>

                    {/* Recent Activity */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.6 }}
                    >
                        <Card className="border-slate-100 shadow-sm">
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <CardTitle className="text-slate-800">Atividade Recente</CardTitle>
                                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1 transition-colors">
                                        <RefreshCw className="w-4 h-4" />
                                        Atualizar
                                    </button>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-1">
                                    {data.recentActivity.map((activity) => {
                                        const iconMap = {
                                            info: Activity,
                                            success: TrendingUp,
                                            warning: Activity,
                                            error: Activity,
                                        };
                                        const Icon = iconMap[activity.type];

                                        const colorMap = {
                                            info: 'bg-blue-50 text-blue-600',
                                            success: 'bg-emerald-50 text-emerald-600',
                                            warning: 'bg-orange-50 text-orange-600',
                                            error: 'bg-red-50 text-red-600',
                                        };

                                        return (
                                            <div key={activity.id} className="flex items-center gap-4 p-4 rounded-xl hover:bg-slate-50 transition-colors duration-200 group">
                                                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${colorMap[activity.type]}`}>
                                                    <Icon className="w-5 h-5" />
                                                </div>
                                                <div className="flex-1 min-w-0">
                                                    <p className="text-sm font-semibold text-slate-900">{activity.title}</p>
                                                    <p className="text-sm text-slate-500 truncate">{activity.description}</p>
                                                </div>
                                                <span className="text-xs font-medium text-slate-400 group-hover:text-slate-600 transition-colors whitespace-nowrap px-2">
                                                    {new Date(activity.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                                                </span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </CardContent>
                        </Card>
                    </motion.div>
                </div>
            </main>
        </>
    );
}
