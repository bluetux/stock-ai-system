import React from "react";
import { useNavigate } from "react-router-dom";

const SidebarTwo = ({ selectedRegion, groups }) => {
  const navigate = useNavigate();

  if (!selectedRegion) return null;

  return (
    <div className="bg-[#222733] w-48 p-2">
      {Object.entries(groups[selectedRegion] || {}).map(([groupId, group]) => (
        <div key={groupId} className="mb-4">
          <div className="text-white text-sm font-bold mb-1">
            {group.icon ? group.icon + " " : ""} {group.name}
          </div>
          <div className="flex flex-col gap-1 ml-2">
            {group.stocks.map((stock) => (
              <button
                key={stock.ticker}
                onClick={() => navigate(`/dashboard/stocks/${stock.ticker}`)}
                className="text-white text-xs hover:underline text-left"
              >
                {stock.alias}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default SidebarTwo;
