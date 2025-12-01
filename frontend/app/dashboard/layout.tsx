import { Sidebar } from '@/components/Sidebar';
import { ChatProvider } from '@/components/chat/ChatProvider';
import type { ReactNode } from 'react';

export default function DashboardLayout({ children }: { children: ReactNode }) {
    return (
        <div className="flex h-screen overflow-hidden bg-[var(--background)]">
            <Sidebar />
            <div className="flex-1 flex flex-col overflow-hidden">
                {children}
            </div>
            <ChatProvider />
        </div>
    );
}
