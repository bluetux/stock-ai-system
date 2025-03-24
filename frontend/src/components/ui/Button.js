// 📁 frontend/src/components/ui/Button.js
import React from "react";

const Button = ({ children, onClick }) => {
  return (
    <button
      className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default Button;
