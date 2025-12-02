'use client';

import { Card, CardHeader, CardTitle, CardContent } from './Card';
import { ChevronLeft, ChevronRight, Database } from 'lucide-react';
import { motion } from 'framer-motion';

interface DataTableProps {
    data: any[];
    columns: string[];
    total: number;
    currentPage: number;
    pageSize: number;
    onPageChange: (page: number) => void;
    loading?: boolean;
}

export function DataTable({
    data,
    columns,
    total,
    currentPage,
    pageSize,
    onPageChange,
    loading = false
}: DataTableProps) {
    const totalPages = Math.ceil(total / pageSize);
    const startRow = (currentPage - 1) * pageSize + 1;
    const endRow = Math.min(currentPage * pageSize, total);

    if (loading) {
        return (
            <Card className="border-slate-200/60 shadow-lg bg-white/80 backdrop-blur-sm">
                <CardHeader>
                    <CardTitle className="text-slate-800 flex items-center gap-2">
                        <Database className="w-5 h-5 text-blue-500" />
                        Data Visualization
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center justify-center py-12">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                    </div>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="border-slate-200/60 shadow-lg bg-white/80 backdrop-blur-sm">
            <CardHeader>
                <div className="flex items-center justify-between">
                    <CardTitle className="text-slate-800 flex items-center gap-2">
                        <Database className="w-5 h-5 text-blue-500" />
                        Data Visualization
                    </CardTitle>
                    <span className="text-sm text-slate-500">
                        {total.toLocaleString()} Total Rows
                    </span>
                </div>
            </CardHeader>
            <CardContent>
                {/* Table */}
                <div className="overflow-x-auto rounded-lg border border-slate-200">
                    <table className="w-full text-sm">
                        <thead className="bg-slate-50 border-b border-slate-200">
                            <tr>
                                {columns.map((col, idx) => (
                                    <th
                                        key={idx}
                                        className="px-4 py-3 text-left font-semibold text-slate-700 whitespace-nowrap"
                                    >
                                        {col}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {data.map((row, rowIdx) => (
                                <motion.tr
                                    key={rowIdx}
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: rowIdx * 0.05 }}
                                    className="hover:bg-slate-50/50 transition-colors"
                                >
                                    {columns.map((col, colIdx) => (
                                        <td
                                            key={colIdx}
                                            className="px-4 py-3 text-slate-600 whitespace-nowrap"
                                        >
                                            {row[col] !== null && row[col] !== undefined
                                                ? String(row[col])
                                                : <span className="text-slate-400 italic">null</span>
                                            }
                                        </td>
                                    ))}
                                </motion.tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Pagination */}
                <div className="flex items-center justify-between mt-4 pt-4 border-t border-slate-200">
                    <div className="text-sm text-slate-600">
                        Showing <span className="font-semibold">{startRow}</span> to{' '}
                        <span className="font-semibold">{endRow}</span> of{' '}
                        <span className="font-semibold">{total.toLocaleString()}</span> linhas
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => onPageChange(currentPage - 1)}
                            disabled={currentPage === 1}
                            className="px-3 py-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-1"
                        >
                            <ChevronLeft className="w-4 h-4" />
                            Previous
                        </button>

                        <div className="flex items-center gap-1">
                            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                                let pageNum;
                                if (totalPages <= 5) {
                                    pageNum = i + 1;
                                } else if (currentPage <= 3) {
                                    pageNum = i + 1;
                                } else if (currentPage >= totalPages - 2) {
                                    pageNum = totalPages - 4 + i;
                                } else {
                                    pageNum = currentPage - 2 + i;
                                }

                                return (
                                    <button
                                        key={i}
                                        onClick={() => onPageChange(pageNum)}
                                        className={`px-3 py-2 rounded-lg border transition-colors ${currentPage === pageNum
                                            ? 'bg-blue-500 text-white border-blue-500'
                                            : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                                            }`}
                                    >
                                        {pageNum}
                                    </button>
                                );
                            })}
                        </div>

                        <button
                            onClick={() => onPageChange(currentPage + 1)}
                            disabled={currentPage === totalPages}
                            className="px-3 py-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-1"
                        >
                            Next
                            <ChevronRight className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
