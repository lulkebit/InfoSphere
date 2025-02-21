import React from 'react';

function Sidebar() {
  const navigation = [
    { name: 'Dashboard', icon: '📊' },
    { name: 'Messages', icon: '📫' },
    { name: 'Categories', icon: '🏷️' },
    { name: 'Settings', icon: '⚙️' },
  ];

  return (
    <aside className="w-64 bg-white shadow-md">
      <div className="p-6">
        <h2 className="text-2xl font-bold text-gray-900">InfoSphere</h2>
      </div>
      <nav className="mt-4">
        {navigation.map((item) => (
          <a
            key={item.name}
            href="#"
            className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 transition-colors"
          >
            <span className="mr-3">{item.icon}</span>
            <span>{item.name}</span>
          </a>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar; 