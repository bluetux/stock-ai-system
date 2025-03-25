import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import {
  ChevronLeft,
  ChevronRight,
  ClipboardList,
  FolderCog
} from "lucide-react";
import classNames from "classnames";

const SettingsSidebar = () => {
  const [isExpanded, setIsExpanded] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleSidebar = () => setIsExpanded(!isExpanded);

  const menuItems = [
    {
      label: "관심종목 관리",
      icon: ClipboardList,
      path: "/dashboard/settings/watchlist",
    },
    {
      label: "그룹 관리",
      icon: FolderCog,
      path: "/dashboard/settings/groups",
    },
  ];

  return (
    <div
      className={classNames(
        "flex flex-col min-h-screen text-white transition-all",
        {
          "w-52": isExpanded,
          "w-16": !isExpanded,
          "bg-settings": true,
        }
      )}
    >
      {/* 상단 타이틀 */}
      <div className="flex items-center px-4 py-3 h-12 font-semibold text-base">
        <span className={classNames("truncate", { "text-white": isExpanded, "text-transparent": !isExpanded })}>
          시스템 설정
        </span>
      </div>

      {/* 메뉴 항목 */}
      <div className="flex-1 overflow-y-auto">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <div
              key={item.label}
              className={classNames(
                "flex items-center px-4 py-3 h-12 cursor-pointer hover:bg-white hover:bg-opacity-10",
                { "bg-white bg-opacity-10": isActive }
              )}
              onClick={() => navigate(item.path)}
            >
              <item.icon className="w-5 h-5 mr-2 flex-shrink-0" />
              {isExpanded && <span>{item.label}</span>}
            </div>
          );
        })}
      </div>

      {/* 접기/펼치기 버튼 */}
      <div className="flex justify-center border-t border-white border-opacity-20 p-2">
        <button
          className="text-white hover:text-gray-300"
          onClick={toggleSidebar}
        >
          {isExpanded ? <ChevronLeft /> : <ChevronRight />}
        </button>
      </div>
    </div>
  );
};

export default SettingsSidebar;