import React, { useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import * as LucideIcons from "lucide-react";
import classNames from "classnames";
import { useNavigate } from "react-router-dom";

// 아이콘 이름 변환 유틸
const toPascalCase = (str) =>
  str
    .split(/[-_]/g)
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join("");

const SidebarTwo = ({ selectedGroup, groups }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const navigate = useNavigate();

  if (!selectedGroup) return null;

  const { region, groupId } = selectedGroup;
  const group = groups?.[region]?.[groupId];
  const stocks = group?.stocks || [];

  const toggleSidebar = () => setIsExpanded(!isExpanded);

  const IconComponent =
    LucideIcons[toPascalCase(group.icon || "folder")] || LucideIcons.Folder;

  return (
    <div
      className={classNames(
        "flex flex-col border-r border-gray-300 bg-white h-full transition-all",
        {
          "w-64": isExpanded,
          "w-[56px]": !isExpanded,
        }
      )}
    >
      {/* 그룹 타이틀 */}
      <div className="flex items-center px-4 py-3 h-12 font-semibold text-base">
        <IconComponent className="w-5 h-5 mr-2 flex-shrink-0" />
        {isExpanded && <span>{group?.name || "선택된 그룹 없음"}</span>}
      </div>

      {/* 종목 리스트 */}
      <div className="flex-1 overflow-y-auto">
        {stocks.map((stock) => {
          const IconComponent =
            LucideIcons[toPascalCase(stock.icon || "activity")] || LucideIcons.Activity;

          return (
            <div
              key={stock.ticker}
              onClick={() => navigate(`/dashboard/stocks/${stock.ticker}`)}
              className="flex items-center gap-2 px-4 py-2 text-sm cursor-pointer hover:text-blue-600"
            >
              <IconComponent className="w-4 h-4 flex-shrink-0" />
              {isExpanded && <span>{stock.alias}</span>}
            </div>
          );
        })}
      </div>

      {/* 접기/펼치기 버튼 */}
      <div className="relative">
        <div className="absolute bottom-2 right-2">
          <button
            className="p-1 border rounded bg-gray-100 hover:bg-gray-200 text-gray-600"
            onClick={toggleSidebar}
          >
            {isExpanded ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SidebarTwo;