import React from 'react';

export default function Loader({ size = 'md', text = 'Loading...' }) {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div className="flex flex-col items-center justify-center py-10 gap-3">
      <div
        className={`${sizeClasses[size]} border-blue-500/20 border-t-[#0f62fe] rounded-full animate-spin`}
      />
      {text && <span className="text-xs text-slate-400 font-mono tracking-wider">{text}</span>}
    </div>
  );
}
