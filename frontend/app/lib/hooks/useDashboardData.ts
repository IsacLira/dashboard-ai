'use client';

import { useState, useEffect } from 'react';
import type { DashboardData } from '@/types';
import { apiClient } from '@/lib/api';

export function useDashboardData() {
    const [data, setData] = useState<DashboardData | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                const dashboardData = await apiClient.getDashboardData();
                setData(dashboardData);
                setError(null);
            } catch (err) {
                setError(err as Error);
                console.error('Failed to fetch dashboard data:', err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();

        // Refresh data every 30 seconds
        const interval = setInterval(fetchData, 30000);

        return () => clearInterval(interval);
    }, []);

    const refetch = async () => {
        try {
            setIsLoading(true);
            const dashboardData = await apiClient.getDashboardData();
            setData(dashboardData);
            setError(null);
        } catch (err) {
            setError(err as Error);
        } finally {
            setIsLoading(false);
        }
    };

    return { data, isLoading, error, refetch };
}
