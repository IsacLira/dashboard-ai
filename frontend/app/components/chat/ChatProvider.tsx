'use client';

import { ChatButton } from './ChatButton';
import { ChatWindow } from './ChatWindow';
import { useChat } from '@/lib/hooks/useChat';

export function ChatProvider() {
    const { messages, isOpen, isTyping, hasUnread, sendMessage, toggleChat, closeChat } = useChat();

    return (
        <>
            <ChatWindow
                isOpen={isOpen}
                messages={messages}
                isTyping={isTyping}
                onClose={closeChat}
                onSendMessage={sendMessage}
            />
            <ChatButton isOpen={isOpen} hasUnread={hasUnread} onClick={toggleChat} />
        </>
    );
}
