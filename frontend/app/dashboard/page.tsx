'use client';

import { useState, useEffect } from 'react';

import { Header } from '@/components/Header';
import { MetricCard } from '@/components/MetricCard';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/Card';
import { Chart } from '@/components/Chart';
import { DataTable } from '@/components/DataTable';
import { Loader2, RefreshCw, TrendingUp, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

const API_BASE_URL = 'http://localhost:8000';

export default function DashboardPage() {
    const [mounted, setMounted] = useState(false);
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState<any>(null);

    // Data preview state
    const [previewData, setPreviewData] = useState<any[]>([]);
    const [previewColumns, setPreviewColumns] = useState<string[]>([]);
    const [previewTotal, setPreviewTotal] = useState(0);
    const [previewPage, setPreviewPage] = useState(1);
    const [previewLoading, setPreviewLoading] = useState(true);
    const pageSize = 10;

    useEffect(() => {
        setMounted(true);
        fetchDashboardData();
        fetchPreviewData(1);
    }, []);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            const response = await fetch(`${API_BASE_URL}/api/dashboard/metrics`);
            const result = await response.json();
            setData(result);
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchPreviewData = async (page: number) => {
        try {
            setPreviewLoading(true);
            const skip = (page - 1) * pageSize;
            const response = await fetch(`${API_BASE_URL}/api/dashboard/preview?skip=${skip}&limit=${pageSize}`);
            const result = await response.json();

            if (!result.error) {
                setPreviewData(result.data);
                setPreviewColumns(result.columns);
                setPreviewTotal(result.total);
                setPreviewPage(page);
            }
        } catch (error) {
            console.error('Error fetching preview data:', error);
        } finally {
            setPreviewLoading(false);
        }
    };

    const handlePageChange = (page: number) => {
        fetchPreviewData(page);
    };

    if (!mounted || loading) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (!data) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <p className="text-slate-600">Failed to load dashboard data</p>
            </div>
        );
    }

    return (
        <>
            <Header title="Dashboard" subtitle="All Metrics" />

            <main className="flex-1 overflow-y-auto p-8 bg-gradient-to-br from-slate-50 via-white to-blue-50/30">
                <div className="max-w-7xl mx-auto space-y-16">
                    {/* Metrics Grid */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
                    >
                        {data.metrics.map((metric: any, index: number) => (
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
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.4 }}
                        >
                            <Card className="h-full border-slate-200/60 shadow-lg hover:shadow-xl transition-all duration-300 bg-white/80 backdrop-blur-sm">
                                <CardHeader>
                                    <CardTitle className="text-slate-800 flex items-center gap-2">
                                        <div className="w-2 h-2 rounded-full bg-blue-500" />
                                        Revenue Over Time
                                    </CardTitle>
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
                            <Card className="h-full border-slate-200/60 shadow-lg hover:shadow-xl transition-all duration-300 bg-white/80 backdrop-blur-sm">
                                <CardHeader>
                                    <CardTitle className="text-slate-800 flex items-center gap-2">
                                        <div className="w-2 h-2 rounded-full bg-indigo-500" />
                                        Unique Customers per Month
                                    </CardTitle>
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
                        <Card className="border-slate-200/60 shadow-lg bg-white/80 backdrop-blur-sm">
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <CardTitle className="text-slate-800 flex items-center gap-2">
                                        <div className="w-2 h-2 rounded-full bg-emerald-500" />
                                        Recent Activities
                                    </CardTitle>
                                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1 transition-colors hover:scale-105 transform duration-200">
                                        <RefreshCw className="w-4 h-4" />
                                        Update
                                    </button>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-2">
                                    {data.recentActivity.map((activity) => {
                                        const iconMap = {
                                            info: Activity,
                                            success: TrendingUp,
                                            warning: Activity,
                                            error: Activity,
                                        };
                                        const Icon = iconMap[activity.type];

                                        const colorMap = {
                                            info: 'bg-blue-50 text-blue-600 border-blue-100',
                                            success: 'bg-emerald-50 text-emerald-600 border-emerald-100',
                                            warning: 'bg-orange-50 text-orange-600 border-orange-100',
                                            error: 'bg-red-50 text-red-600 border-red-100',
                                        };

                                        return (
                                            <div key={activity.id} className="flex items-center gap-4 p-4 rounded-xl hover:bg-slate-50/80 transition-all duration-200 group cursor-pointer border border-transparent hover:border-slate-200">
                                                <div className={`w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 border ${colorMap[activity.type]} group-hover:scale-110 transition-transform duration-200`}>
                                                    <Icon className="w-5 h-5" />
                                                </div>
                                                <div className="flex-1 min-w-0">
                                                    <p className="text-sm font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">{activity.title}</p>
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

                    {/* Data Preview Section */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.7 }}
                    >
                        <DataTable
                            data={previewData}
                            columns={previewColumns}
                            total={previewTotal}
                            currentPage={previewPage}
                            pageSize={pageSize}
                            onPageChange={handlePageChange}
                            loading={previewLoading}
                        />
                    </motion.div>
                </div>
            </main>
        </>
    );
}
