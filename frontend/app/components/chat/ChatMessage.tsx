'use client';

import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';
import { cn, getRelativeTime } from '@/lib/utils';
import { ChatMessage as ChatMessageType } from '@/types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ChatMessageProps {
    message: ChatMessageType;
}

export function ChatMessageBubble({ message }: ChatMessageProps) {
    const isUser = message.role === 'user';
    const { content, timestamp } = message;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.3 }}
            className={cn(
                'flex w-full mb-4',
                isUser ? 'justify-end' : 'justify-start'
            )}
        >
            <div className={cn('flex flex-col max-w-[90%]', isUser ? 'items-end' : 'items-start')}>
                <div className="flex items-start gap-3">
                    {!isUser && (
                        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0 mt-1">
                            <Bot className="w-5 h-5 text-blue-600" />
                        </div>
                    )}

                    <div className="py-2 overflow-hidden">
                        <div className={cn(
                            "text-sm leading-relaxed break-words prose prose-sm max-w-none",
                            isUser ? "text-slate-800 font-medium prose-p:text-slate-800" : "text-slate-600 prose-p:text-slate-600",
                            "prose-headings:font-semibold prose-headings:text-slate-800 prose-headings:mb-2 prose-headings:mt-4 first:prose-headings:mt-0",
                            "prose-p:my-2 first:prose-p:mt-0 last:prose-p:mb-0",
                            "prose-a:text-blue-600 prose-a:no-underline hover:prose-a:underline",
                            "prose-strong:font-semibold prose-strong:text-slate-900",
                            "prose-ul:list-disc prose-ul:pl-4 prose-ul:my-2",
                            "prose-ol:list-decimal prose-ol:pl-4 prose-ol:my-2",
                            "prose-li:my-0.5",
                            "prose-code:px-1 prose-code:py-0.5 prose-code:bg-slate-100 prose-code:rounded prose-code:text-slate-800 prose-code:text-xs prose-code:font-mono prose-code:before:content-none prose-code:after:content-none",
                            "prose-pre:bg-slate-900 prose-pre:text-slate-50 prose-pre:p-3 prose-pre:rounded-lg prose-pre:my-2",
                            "prose-table:w-full prose-table:my-2 prose-table:border-collapse prose-table:text-xs",
                            "prose-th:text-left prose-th:p-2 prose-th:bg-slate-50 prose-th:border prose-th:border-slate-200 prose-th:font-semibold prose-th:text-slate-700",
                            "prose-td:p-2 prose-td:border prose-td:border-slate-200 prose-td:text-slate-600"
                        )}>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {content}
                            </ReactMarkdown>
                        </div>
                    </div>

                    {isUser && (
                        <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center flex-shrink-0 mt-1">
                            <User className="w-5 h-5 text-slate-600" />
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
}
