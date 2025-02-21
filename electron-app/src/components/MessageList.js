import React from 'react';

function MessageList({ messages }) {
  return (
    <div className="grid gap-6">
      {messages.map((message) => (
        <article key={message.id} className="bg-white rounded-lg shadow-md p-6 transition-transform hover:scale-[1.01]">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">{message.title}</h2>
            <span className="text-sm text-gray-500">{new Date(message.created_at).toLocaleDateString()}</span>
          </div>
          <p className="text-gray-600 mb-4">{message.content}</p>
          {message.tags && (
            <div className="flex flex-wrap gap-2">
              {message.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </article>
      ))}
    </div>
  );
}

export default MessageList; 