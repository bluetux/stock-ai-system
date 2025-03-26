import React, { useState } from "react";
import {
  Globe,
  ChevronLeft,
  ChevronRight,
  Flag,
} from "lucide-react";
import * as LucideIcons from "lucide-react";
import classNames from "classnames";

// 아이콘 이름 변환 함수
const toPascalCase = (str) =>
  str
    .split(/[-_]/g)
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join("");

const SidebarOne = ({ groups, selectedRegion, setSelectedRegion, setSelectedGroup }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const regions = Object.keys(groups);

  const toggleSidebar = () => setIsExpanded(!isExpanded);

  return (
    <div
      className={classNames(
        "relative flex flex-col bg-main border-r border-gray-300 h-full transition-all",
        {
          "w-52": isExpanded,
          "w-[56px]": !isExpanded,
        }
      )}
    >
      {/* 상단 제목 */}
      <div className="flex items-center px-4 py-3 h-12 cursor-pointer hover:text-blue-600">
        <Globe className="w-5 h-5 mr-2 flex-shrink-0" />
        <span
          className={classNames("font-semibold text-base", {
            "text-black": isExpanded,
            "text-transparent": !isExpanded, // 줄간격 유지
          })}
        >
          주식 분석 시스템
        </span>
      </div>

      {/* 지역 + 그룹 리스트 */}
      <div className="flex-1 overflow-y-auto">
        {regions.map((region) => (
          <div key={region}>
            {/* 지역 줄 */}
            <div
              className="flex items-center px-4 py-3 h-12 cursor-pointer"
              onClick={() => setSelectedRegion(region)}
            >
              <Flag className="w-5 h-5 mr-2 flex-shrink-0" />
              <span
                className={classNames("font-semibold", {
                  "text-black": isExpanded,
                  "text-white": !isExpanded,
                })}
              >
                {region}주식
              </span>
            </div>

            {/* 그룹 줄들 */}
            {Object.entries(groups[region] || {}).map(([groupId, group]) => {
              const iconName = toPascalCase(group.icon || "folder");
              const IconComponent = LucideIcons[iconName] || LucideIcons.Folder;

              return (
                <div
                  key={groupId}
                  onClick={() => setSelectedGroup({ region, groupId })}
                  className="flex items-center px-4 py-3 h-12 cursor-pointer hover:text-blue-600"
                >
                  <IconComponent className="w-5 h-5 mr-2 flex-shrink-0" />
                  <span
                    className={classNames("", {
                      "text-black": isExpanded,
                      "text-white": !isExpanded,
                    })}
                  >
                    {group.name}
                  </span>
                </div>
              );
            })}
          </div>
        ))}
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

export default SidebarOne;