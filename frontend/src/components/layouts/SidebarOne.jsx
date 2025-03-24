import React, { useState } from "react";
import { FiChevronRight } from "react-icons/fi";

const SidebarOne = ({ selectedRegion, setSelectedRegion, groups }) => {
  const [expanded, setExpanded] = useState(true);
  const toggleExpanded = () => setExpanded(!expanded);

  return (
    <div className={`bg-[#1a1f2b] ${expanded ? "w-32" : "w-16"} transition-all duration-300`}>
      <div className="p-2 flex flex-col items-center gap-2 mt-4">
        {Object.entries(groups).map(([region, groupList]) => (
          <button
            key={region}
            onClick={() => setSelectedRegion(region)}
            className={`w-full text-white flex flex-col items-center gap-1 p-2 rounded hover:bg-[#2a2f3a] ${
              selectedRegion === region ? "bg-[#2a2f3a]" : ""
            }`}
          >
            <span className="text-2xl">{region === "한국" ? "🇰🇷" : "🇺🇸"}</span>
            {expanded && <span className="text-xs">{region}</span>}
          </button>
        ))}
      </div>

      {/* 👇 토글 버튼 */}
      <div className="flex justify-center mt-4">
        <button onClick={toggleExpanded} className="text-white text-xs">
          <FiChevronRight className={`${expanded ? "rotate-180" : ""} transition-transform`} />
        </button>
      </div>
    </div>
  );
};

export default SidebarOne;
