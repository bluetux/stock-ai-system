// 📁 frontend/src/components/ui/Card.js
import React from "react";

const Card = ({ title, children, onClick }) => {
  return (
    <div
      className="bg-white shadow-md rounded p-4 hover:shadow-lg cursor-pointer"
      onClick={onClick}
    >
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <div>{children}</div>
    </div>
  );
};

export default Card;
